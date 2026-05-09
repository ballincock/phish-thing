from flask import Blueprint, render_template, session, redirect, url_for

dash_bp = Blueprint('dash', __name__)

@dash_bp.route('/')
def index():
    if 'user_id' not in session:
        return render_template('auth.html')
    
    from app.models.user import User
    user = User.query.get(session['user_id'])
    
    if not user:
        session.clear() 
        return render_template('auth.html')
        
    return render_template('dashboard.html')

@dash_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('dash.index'))
