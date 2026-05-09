from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from app.models.user import User, db
from app.services.gallery_service import GalleryService

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile/<username>')
def view_profile(username):
    target_user = User.query.filter_by(username=username).first_or_404()
    
    is_owner = False
    if 'user_id' in session and session['user_id'] == target_user.id:
        is_owner = True
        
    return render_template('profile.html', user=target_user, is_owner=is_owner)

@user_bp.route('/profile/update', methods=['POST'])
def update_profile():
    if 'user_id' not in session: 
        return jsonify({"error": "Unauthorized"}), 401
    
    user = User.query.get(session['user_id'])
    
    user.display_name = request.form.get('display_name')
    user.bio = request.form.get('bio')
    user.favorite_species = request.form.get('favorite_species')
    user.favorite_pb = request.form.get('favorite_pb')
    user.fishing_region = request.form.get('fishing_region')
    
    user.reddit = request.form.get('reddit')
    user.twitter = request.form.get('twitter')
    user.instagram = request.form.get('instagram')
    user.youtube = request.form.get('youtube')
    user.facebook = request.form.get('facebook')
    
    if 'file' in request.files:
        file = request.files['file']
        path = GalleryService.save_image(file, user.id)
        if path:
            user.profile_picture = path

    db.session.commit()
    return jsonify({"success": True})
