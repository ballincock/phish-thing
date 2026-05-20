from flask import Blueprint, render_template, request, session, abort
from app.models.user import db, User
from analytics.models import UserVisit
from sqlalchemy import func

analytics_bp = Blueprint('analytics', __name__, template_folder='templates')

def get_current_user_id():
    return session.get('user_id')

@analytics_bp.before_app_request
def track_visitor():
    if request.endpoint in ['static', 'statistics.dashboard'] or not request.endpoint:
        return

    user_id = get_current_user_id()
    
    ip_addr = request.headers.get('X-Forwarded-For', request.remote_addr)
    if ip_addr:
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
    user_id = get_current_user_id()
    if user_id != 1: 
        abort(403)

    total_page_views = UserVisit.query.count()
    unique_ips = db.session.query(func.count(UserVisit.ip_address.distinct())).scalar()
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
