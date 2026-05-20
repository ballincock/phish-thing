import csv
from io import StringIO
from datetime import datetime, timedelta
from flask import Blueprint, render_template, request, session, abort, Response
from app.models.user import db, User  
from analytics.models import UserVisit
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__, template_folder='templates')

def get_current_user_id():
    return session.get('user_id')

@analytics_bp.before_app_request
def track_visitor():
    if request.endpoint in ['static', 'analytics.dashboard', 'analytics.export_csv'] or not request.endpoint:
        return

    user_id = get_current_user_id()
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_addr and ',' in ip_addr:
        ip_addr = ip_addr.split(',')[0].strip()

    visit = UserVisit(
        user_id=user_id,
        endpoint=request.endpoint,
        ip_address=ip_addr,
        user_agent=request.user_agent.string[:255]
    )
    db.session.add(visit)
    db.session.commit()

@analytics_bp.route('/admin/statistics')
def dashboard():
    if get_current_user_id() != 1:
        abort(403)

    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    UserVisit.query.filter(UserVisit.timestamp < thirty_days_ago).delete()
    db.session.commit()

    total_page_views = UserVisit.query.count()
    unique_ips = db.session.query(func.count(UserVisit.ip_address.distinct())).scalar() or 0
    logged_in_clicks = UserVisit.query.filter(UserVisit.user_id.isnot(None)).count()
    
    top_endpoints = db.session.query(
        UserVisit.endpoint, func.count(UserVisit.endpoint).label('qty')
    ).group_by(UserVisit.endpoint).order_by(db.text('qty DESC')).limit(5).all()

    recent_visits = UserVisit.query.order_by(UserVisit.timestamp.desc()).limit(20).all()

    return render_template(
        'analytics/dashboard.html',
        total_views=total_page_views,
        unique_visitors=unique_ips,
        member_clicks=logged_in_clicks,
        top_pages=top_endpoints,
        recent_logs=recent_visits
    )

@analytics_bp.route('/admin/statistics/export')
def export_csv():
    if get_current_user_id() != 1:
        abort(403)

    all_logs = UserVisit.query.order_by(UserVisit.timestamp.desc()).all()

    def generate():
        data = StringIO()
        writer = csv.writer(data)
        
        writer.writerow(['Log ID', 'User ID', 'Username', 'Target Route', 'IP Address', 'Browser Agent', 'Timestamp UTC'])
        yield data.getvalue()
        data.seek(0)
        data.truncate(0)

        for log in all_logs:
            username = log.user.username if log.user_id else 'Guest'
            writer.writerow([
                log.id, 
                log.user_id if log.user_id else 'N/A', 
                username, 
                log.endpoint, 
                log.ip_address, 
                log.user_agent, 
                log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
            yield data.getvalue()
            data.seek(0)
            data.truncate(0)

    response = Response(generate(), mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename=f"traffic_report_{datetime.utcnow().strftime('%Y%m%d')}.csv")
    return response
