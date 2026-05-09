from flask import Blueprint, render_template, request, session, jsonify, redirect, url_for
from app.models.user import User, db
from app.services.crypto import CryptoService

security_bp = Blueprint('security', __name__)

@security_bp.route('/settings/security')
def settings():
    if 'user_id' not in session: return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    return render_template('security_settings.html', user=user)

@security_bp.route('/settings/update-field', methods=['POST'])
def update_field():
    data = request.json
    user = User.query.get(session['user_id'])
    
    if user.mnemonic != data.get('mnemonic'):
        return jsonify({"error": "Mnemonic verification failed."}), 403
    
    field_type = data.get('type')
    
    try:
        if field_type == 'password':
            if data['val'] != data['confirm']: return jsonify({"error": "Passwords do not match."}), 400
            user.password_hash = CryptoService.secure_hash(data['val'])
            
        elif field_type == 'email':
            if User.query.filter(User.email == data['email'], User.id != user.id).first():
                return jsonify({"error": "Email already in use."}), 400
            user.email = data['email']
            user.backup_email = data['backup']
            
        elif field_type == 'qa':
            user.security_question = data['question']
            user.security_answer_hash = CryptoService.secure_hash(data['answer'])

        db.session.commit()
        return jsonify({"success": True, "message": f"{field_type.capitalize()} updated."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@security_bp.route('/settings/delete-account', methods=['POST'])
def delete_account():
    data = request.json
    user = User.query.get(session['user_id'])
    
    if user.username != data.get('confirm_user') or user.mnemonic != data.get('mnemonic'):
        return jsonify({"error": "Mnemonic or Username confirmation failed."}), 400
        
    db.session.delete(user)
    db.session.commit()
    session.clear()
    return jsonify({"success": True})
