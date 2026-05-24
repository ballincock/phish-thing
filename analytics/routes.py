"""
From the necessities of the dashboard and session dashboard necessities, use this file to do so.
Other variables and table that are likely to need to be constructed are stuff like:
    > user favorite activities based on page visit duration
    > use data from within those pages (where they placed spot pins, etc), to make even more detailed and advanced recommendations to user in question.

Models file will be the means by which all of these tables are created, and all handling will be done here via REST
"""

import csv
import uuid
from io import StringIO
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, session, abort, Response
from app.models.user import db, User
from analytics.models import UserVisit, UserSession
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__, template_folder='templates')

def get_current_user_id():
    return session.get('user_id')

@analytics_bp.before_app_request
def track_visitor_and_session():
    if request.endpoint in ['static', 'analytics.dashboard', 'analytics.session_dashboard', 'analytics.export_csv'] or not request.endpoint:
        return

    user_id = get_current_user_id()
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr) or request.remote_addr
    if ip_addr and ',' in ip_addr:
        ip_addr = ip_addr.split(',')[0].strip()

    visit = UserVisit(
        user_id=user_id, endpoint=request.endpoint, 
        ip_address=ip_addr, user_agent=request.user_agent.string[:255]
    )
    db.session.add(visit)

    if 'analytics_session_id' not in session:
        session['analytics_session_id'] = str(uuid.uuid4())

    s_key = session['analytics_session_id']
    now = datetime.utcnow()

    user_sess = UserSession.query.filter_by(session_key=s_key).first()

    if not user_sess:
        new_sess = UserSession(
            session_key=s_key, user_id=user_id, 
            ip_address=ip_addr, user_agent=request.user_agent.string[:255]
        )
        db.session.add(new_sess)
    else:
        time_delta = (now - user_sess.last_activity).total_seconds()
        
        if time_delta < 1800: 
            user_sess.duration_seconds += int(time_delta)
        
        user_sess.page_views += 1
        user_sess.last_activity = now
        if user_id and not user_sess.user_id:
            user_sess.user_id = user_id 

    db.session.commit()

@analytics_bp.route('/admin/statistics')
def dashboard():
    if get_current_user_id() != 1: abort(403)
    
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    UserVisit.query.filter(UserVisit.timestamp < thirty_days_ago).delete()
    db.session.commit()

    total_page_views = UserVisit.query.count()
    unique_ips = db.session.query(func.count(UserVisit.ip_address.distinct())).scalar() or 0
    logged_in_clicks = UserVisit.query.filter(UserVisit.user_id.isnot(None)).count()
    
    top_pages = db.session.query(
        UserVisit.endpoint, func.count(UserVisit.endpoint).label('qty')
    ).group_by(UserVisit.endpoint).order_by(db.text('qty DESC')).limit(5).all()

    recent_logs = UserVisit.query.order_by(UserVisit.timestamp.desc()).limit(20).all()

    return render_template(
        'analytics/dashboard.html', total_views=total_page_views, 
        unique_visitors=unique_ips, member_clicks=logged_in_clicks, 
        top_pages=top_pages, recent_logs=recent_logs
    )

@analytics_bp.route('/admin/statistics/sessions')
def session_dashboard():
    if get_current_user_id() != 1: abort(403)

    total_sessions = UserSession.query.count()
    
    avg_duration = db.session.query(func.avg(UserSession.duration_seconds)).scalar() or 0
    avg_pages = db.session.query(func.avg(UserSession.page_views)).scalar() or 0
    max_duration = db.session.query(func.max(UserSession.duration_seconds)).scalar() or 0

    five_mins_ago = datetime.utcnow() - timedelta(minutes=5)
    active_count = UserSession.query.filter(UserSession.last_activity >= five_mins_ago).count()

    recent_sessions = UserSession.query.order_by(UserSession.last_activity.desc()).limit(20).all()

    return render_template(
        'analytics/session_dashboard.html',
        total_sessions=total_sessions,
        avg_duration=round(avg_duration / 60, 1), 
        avg_pages=round(avg_pages, 1),
        max_duration=round(max_duration / 60, 1),
        active_count=active_count,
        sessions_logs=recent_sessions
    )

@analytics_bp.route('/admin/statistics/export')
def export_csv():
    if get_current_user_id() != 1: abort(403)
    all_logs = UserVisit.query.order_by(UserVisit.timestamp.desc()).all()
    def generate():
        data = StringIO()
        writer = csv.writer(data)
        writer.writerow(['Log ID', 'User ID', 'Username', 'Target Route', 'IP Address', 'Browser Agent', 'Timestamp UTC'])
        yield data.getvalue()
        data.seek(0); data.truncate(0)
        for log in all_logs:
            username = log.user.username if log.user_id else 'Guest'
            writer.writerow([log.id, log.user_id or 'N/A', username, log.endpoint, log.ip_address, log.user_agent, log.timestamp])
            yield data.getvalue()
            data.seek(0); data.truncate(0)
    response = Response(generate(), mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="traffic_report.csv")
    return response

from flask import jsonify

@analytics_bp.route('/api/recommendations')
def get_recommendations():
    user_id = get_current_user_id()
    
    try:
        fallback_recommendations = [
            {"title": "Trending Support Portal", "url": url_for('tickets.portal'), "reason": "Manage active operational support streams."},
            {"title": "Main Platform Dashboard", "url": url_for('dash.index'), "reason": "Return back to your primary workstation room."},
            {"title": "Hydrology Calculators", "url": url_for('calcs.hydrology-calcs'), "reason": "Use our hydrology services that encompass a wide scope of hydrology probleming solving calculators."}
        ]
    except Exception:
        fallback_recommendations = [
            {"title": "Trending Support Portal", "url": "/tickets", "reason": "Manage active operational support streams."},
            {"title": "Main Platform Dashboard", "url": "/", "reason": "Return back to your primary workstation room."},
            {"title": "Hydrology Services", "url": "/hydrology-calcs", "reason": "Use our hydrology services that encompass a wide scope of hydrology probleming solving calculators."}
        ]
    
    if not user_id:
        return jsonify(fallback_recommendations)

    top_user_views = db.session.query(
        UserVisit.endpoint, func.count(UserVisit.endpoint).label('hits')
    ).filter(UserVisit.user_id == user_id)\
     .group_by(UserVisit.endpoint)\
     .order_by(db.text('hits DESC')).limit(3).all()

    if not top_user_views:
        return jsonify(fallback_recommendations)

    recommendations = []
    
    for view in top_user_views:
        endpoint_name = view.endpoint
        
        if 'analytics' in endpoint_name or endpoint_name == request.endpoint:
            continue
            
        try:
            real_url = url_for(endpoint_name)
            
            display_title = endpoint_name.split('.')[-1].replace('_', ' ').title()
            
            recommendations.append({
                "title": f"Open {display_title}",
                "url": real_url,
                "reason": "Based on your frequent activity patterns in this space."
            })
        except Exception:
            continue

    final_output = recommendations if recommendations else fallback_recommendations
    return jsonify(final_output[:3]) 
