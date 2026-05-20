from flask import Blueprint, request, jsonify, session
from app.models.user import User, db
from app.services.crypto import CryptoService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    mnemonic = CryptoService.generate_mnemonic()
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=CryptoService.hash_value(data['password']),
        security_question=data['question'],
        security_answer_hash=CryptoService.hash_value(data['answer']),
        backup_email=data.get('backup_email'),
        mnemonic=mnemonic
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"mnemonic": mnemonic})

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and CryptoService.verify_value(user.password_hash, data.get('password')):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({"success": True})
        
        return jsonify({"error": "Invalid credentials"}), 401
        
    except Exception as e:
        print(f"DEBUG LOGIN ERROR: {str(e)}") 
        return jsonify({"error": str(e)}), 500
