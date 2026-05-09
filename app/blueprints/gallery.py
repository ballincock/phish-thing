from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from app.models.gallery import GalleryImage, db
from app.services.gallery_service import GalleryService

gallery_bp = Blueprint('gallery', __name__)

@gallery_bp.route('/personal-gallery')
def personal_gallery():
    if 'user_id' not in session:
        return redirect(url_for('dash.index'))
    
    images = GalleryImage.query.filter_by(user_id=session['user_id']).order_by(GalleryImage.upload_date.desc()).all()
    return render_template('gallery.html', images=images)

@gallery_bp.route('/gallery/upload', methods=['POST'])
def upload_image():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    user_id = session['user_id']
    file = request.files.get('file')
    
    if not file:
        return jsonify({"error": "No image file provided"}), 400

    path = GalleryService.save_image(file, user_id)

    if path:
        try:
            new_catch = GalleryImage(
                user_id=user_id,
                image_path=path,
                species=request.form.get('species'),
                lure_used=request.form.get('lure_used'),
                season=request.form.get('season'),
                time_of_day=request.form.get('time_of_day'),
                pressure=float(request.form.get('pressure')) if request.form.get('pressure') else None,
                temperature=float(request.form.get('temperature')) if request.form.get('temperature') else None,
                cloud_cover=request.form.get('cloud_cover'),
                moon_cycle=request.form.get('moon_cycle'),
                notes=request.form.get('notes')
            )
            db.session.add(new_catch)
            db.session.commit()
            return jsonify({"success": True, "path": path}), 200
            
        except Exception as e:
            db.session.rollback()
            GalleryService.delete_image(path) 
            return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({"error": "Failed to save file to server"}), 500

@gallery_bp.route('/gallery/details/<int:img_id>')
def image_details(img_id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    
    img = GalleryImage.query.get_or_404(img_id)
    
    if img.user_id != session['user_id']:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify({
        "image_path": img.image_path,
        "species": img.species,
        "lure_used": img.lure_used,
        "temperature": img.temperature,
        "pressure": img.pressure,
        "cloud_cover": img.cloud_cover,
        "moon_cycle": img.moon_cycle,
        "notes": img.notes
    })
