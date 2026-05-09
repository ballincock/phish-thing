from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from app.models.community import PublicCatch, LikeRecord, Comment, db
from app.services.gallery_service import GalleryService
from sqlalchemy import func
from datetime import datetime

community_bp = Blueprint('community', __name__)

@community_bp.route('/community-gallery')
def gallery():
    uid = session.get('user_id')
    if not uid: return jsonify({"error": "Unauthorized"}), 401
    db.session.expire_all() 
    sort = request.args.get('sort', 'new')
    query = PublicCatch.query
    
    if sort == 'top': 
        query = query.order_by(PublicCatch.likes.desc())
    elif sort == 'hot': 
        query = query.order_by((PublicCatch.likes - PublicCatch.dislikes).desc())
    elif sort == 'random': 
        query = query.order_by(func.random())
    else: 
        query = query.order_by(PublicCatch.created_at.desc())

    all_posts = query.all()
    posts_data = []
    
    for p in all_posts:
        if p.author: 
            posts_data.append({
                'id': p.id,
                'username': p.author.username,
                'display_name': p.author.display_name or p.author.username,
                'pfp': p.author.profile_picture if p.author.profile_picture else "https://ui-avatars.com" + p.author.username,
                'image_path': p.image_path,
                'species': p.species or 'Unknown',
                'lure_used': p.lure_used or 'N/A',
                'temp': p.temperature or '?',
                'pressure': p.pressure or 'N/A',
                'time': p.time_of_day or 'N/A',
                'moon': p.moon_cycle or 'N/A',
                'notes': p.notes or '',
                'likes': p.likes or 0,
                'dislikes': p.dislikes or 0
            })

    print(f"DEBUG: Found {len(posts_data)} posts for the gallery.") 
            
    return render_template('community_gallery.html', posts=posts_data, sort=sort)

@community_bp.route('/community/upload', methods=['POST'])
def public_upload():
    uid = session.get('user_id')
    if not uid: return jsonify({"error": "Unauthorized"}), 401
    
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({"error": "No image selected"}), 400

    path = GalleryService.save_image(file, session['user_id'])
    
    if path:
        try:
            new_post = PublicCatch(
                user_id=session['user_id'],
                image_path=path,
                species=request.form.get('species'),
                lure_used=request.form.get('lure_used'),
                time_of_day=request.form.get('time_of_day'),
                temperature=float(request.form.get('temperature')) if request.form.get('temperature') else None,
                pressure=float(request.form.get('pressure')) if request.form.get('pressure') else None,
                cloud_cover=request.form.get('cloud_cover'),
                moon_cycle=request.form.get('moon_cycle'),
                notes=request.form.get('notes')
            )
            db.session.add(new_post)
            db.session.commit()
            return jsonify({"success": True})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "File save failed"}), 500

@community_bp.route('/community/comment', methods=['POST'])
def post_comment():
    data = request.json
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401

    new_comment = Comment(
        post_id=data['post_id'],
        user_id=session['user_id'],
        parent_id=data.get('parent_id'), 
        text=data['text']
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({"success": True})

@community_bp.route('/community/get-comments/<int:post_id>')
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id, parent_id=None).order_by(Comment.created_at.desc()).all()
    return render_template('partials/comments.html', comments=comments, post_id=post_id)

@community_bp.route('/community/vote', methods=['POST'])
def vote():
    data = request.json
    uid = session.get('user_id')
    if not uid: return jsonify({"error": "Login required"}), 401
    
    post = PublicCatch.query.get(data['post_id'])
    existing = LikeRecord.query.filter_by(user_id=uid, post_id=post.id).first()
    new_vote = int(data['vote']) 
    
    if existing:
        if existing.status == new_vote: db.session.delete(existing)
        else: existing.status = new_vote
    else:
        db.session.add(LikeRecord(user_id=uid, post_id=post.id, status=new_vote))
    
    db.session.commit()
    post.likes = LikeRecord.query.filter_by(post_id=post.id, status=1).count()
    post.dislikes = LikeRecord.query.filter_by(post_id=post.id, status=-1).count()
    db.session.commit()
    return jsonify({"likes": post.likes, "dislikes": post.dislikes})
