from flask import Blueprint, render_template, session, redirect, url_for
from app.models.user import User
from app.models.message import Message

dash_bp = Blueprint('dash', __name__)

@dash_bp.route('/')
def index():
    if 'user_id' not in session:
        return render_template('auth.html')
    
    from app.models.user import User
    user = User.query.get(session['user_id'])

    uid = session['user_id']
    
    if not user:
        session.clear() 
        return render_template('auth.html')

    unread_count = Message.query.filter_by(receiver_id=uid, is_read=False).count()
        
    return render_template('dashboard.html', user=user, unread_count=unread_count)

@dash_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dash.index'))
