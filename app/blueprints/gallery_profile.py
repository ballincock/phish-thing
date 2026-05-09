from flask import Blueprint, render_template, session, redirect, url_for
from app.models.user import User
from app.models.community import PublicCatch, Friendship, LikeRecord, db
from sqlalchemy import func

gallery_profile_bp = Blueprint('gallery_profile', __name__)

@gallery_profile_bp.route('/gallery-profile/<username>')
def view(username):
    user = User.query.filter_by(username=username).first_or_404()

    total_likes = db.session.query(func.sum(PublicCatch.likes)).filter(PublicCatch.user_id == user.id).scalar() or 0
    
    public_posts = PublicCatch.query.filter_by(user_id=user.id).order_by(PublicCatch.created_at.desc()).all()

    is_friend = False
    
    return render_template('gallery_profile.html', 
                           target_user=user, 
                           posts=public_posts, 
                           likes=total_likes,
                           is_friend=is_friend)

@gallery_profile_bp.route('/friend/add/<int:target_id>', methods=['POST'])
def add_friend(target_id):
    my_id = session.get('user_id')
    if not my_id: return jsonify({"error": "Login required"}), 401
    
    if my_id == target_id: return jsonify({"error": "Cannot friend yourself"}), 400

    existing = Friendship.query.filter_by(user_id=my_id, friend_id=target_id).first()
    if not existing:
        new_req = Friendship(user_id=my_id, friend_id=target_id, status='pending')
        db.session.add(new_req)
        db.session.commit()
        return jsonify({"success": True, "message": "Request Sent!"})
    
    return jsonify({"error": "Request already exists"})
