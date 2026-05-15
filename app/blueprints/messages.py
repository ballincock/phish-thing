from datetime import datetime
from flask import Blueprint, render_template, request, session, jsonify
from sqlalchemy import or_, and_
from app.models.user import User, db
from app.models.message import Message
from app.models.block import BlockList

messages_bp = Blueprint('messages', __name__, template_folder='../templates')

def update_user_activity(uid, typing_target=0):
    user = User.query.get(uid)
    if user:
        user.last_seen = datetime.datetime.utcnow()
        user.is_typing_target = typing_target
        db.session.commit()

@messages_bp.route('/messages', methods=['GET'])
def messages_view():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user = User.query.get(session['user_id'])
    update_user_activity(user.id)
    return render_template('messages.html', user=user)

@messages_bp.route('/api/messages/sidebar', methods=['GET'])
def get_sidebar_threads():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    uid = session['user_id']
    update_user_activity(uid)
    
    msgs = Message.query.filter(or_(Message.sender_id == uid, Message.receiver_id == uid)).order_by(Message.sent_at.desc()).all()
    interacted_uids = []
    seen = set()
    for m in msgs:
        other = m.receiver_id if m.sender_id == uid else m.sender_id
        if other not in seen:
            interacted_uids.append(other)
            seen.add(other)

    threads = []
    now = datetime.datetime.utcnow()
    for other_id in interacted_uids:
        other_user = User.query.get(other_id)
        if not other_user: continue
        
        is_blocked = BlockList.query.filter(
            or_(
                and_(BlockList.blocker_id == uid, BlockList.blocked_id == other_id),
                and_(BlockList.blocker_id == other_id, BlockList.blocked_id == uid)
            )
        ).first() is not None
        
        last_msg = Message.query.filter(
            or_(
                and_(Message.sender_id == uid, Message.receiver_id == other_id),
                and_(Message.sender_id == other_id, Message.receiver_id == uid)
            )
        ).order_by(Message.sent_at.desc()).first()
        
        unread_count = Message.query.filter_by(sender_id=other_id, receiver_id=uid, is_read=False).count()
        
        is_online = False
        if other_user.last_seen:
            is_online = (now - other_user.last_seen).total_seconds() <= 15
            
        is_typing = other_user.is_typing_target == uid if is_online else False
        
        threads.append({
            "user_id": other_user.id,
            "username": other_user.username,
            "display_name": other_user.display_name or other_user.username,
            "profile_picture": other_user.profile_picture or 'uploads/profiles/default.png',
            "preview": last_msg.body if last_msg else "",
            "last_date": last_msg.sent_at.strftime('%Y-%m-%d %H:%M') if last_msg else "",
            "unread": unread_count,
            "blocked": is_blocked,
            "online": is_online,
            "typing": is_typing
        })
    return jsonify({"threads": threads})

@messages_bp.route('/api/messages/thread/<int:other_id>', methods=['GET'])
def get_message_thread(other_id):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    uid = session['user_id']
    
    typing_state = int(request.args.get('typing', 0))
    update_user_activity(uid, typing_target=other_id if typing_state == 1 else 0)
    
    unread = Message.query.filter_by(sender_id=other_id, receiver_id=uid, is_read=False).all()
    for m in unread: m.is_read = True
    db.session.commit()
    
    msgs = Message.query.filter(
        or_(
            and_(Message.sender_id == uid, Message.receiver_id == other_id),
            and_(Message.sender_id == other_id, Message.receiver_id == uid)
        )
    ).order_by(Message.sent_at.asc()).all()
    
    now = datetime.datetime.utcnow()
    thread_data = []
    for m in msgs:
        time_diff = (now - m.sent_at).total_seconds()
        thread_data.append({
            "id": m.id,
            "sender_id": m.sender_id,
            "body": m.body,
            "time": m.sent_at.strftime('%H:%M'),
            "deletable": (m.sender_id == uid and time_diff <= 600)
        })
        
    other_user = User.query.get(other_id)
    other_online = (now - other_user.last_seen).total_seconds() <= 15 if other_user and other_user.last_seen else False
    other_typing = other_user.is_typing_target == uid if other_user and other_online else False
    
    return jsonify({
        "messages": thread_data,
        "other_online": other_online,
        "other_typing": other_typing
    })

@messages_bp.route('/api/messages/send', methods=['POST'])
def send_message():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    uid = session['user_id']
    data = request.get_json() or {}
    receiver_id = data.get('receiver_id')
    body = data.get('body', '').strip()
    
    if not receiver_id or not body: return jsonify({"error": "Bad Request"}), 400
    
    if len(body) > 250:
        return jsonify({"error": "Message body exceeds maximum 250 character limits."}), 400
    
    blocked = BlockList.query.filter(
        or_(
            and_(BlockList.blocker_id == uid, BlockList.blocked_id == receiver_id),
            and_(BlockList.blocker_id == receiver_id, BlockList.blocked_id == uid)
        )
    ).first()
    if blocked: return jsonify({"error": "Message blocked by filtering rules."}), 403
    
    m = Message(sender_id=uid, receiver_id=receiver_id, body=body)
    db.session.add(m)
    db.session.commit()
    
    update_user_activity(uid, typing_target=0)
    return jsonify({"success": True})

@messages_bp.route('/api/messages/search-users', methods=['GET'])
def search_global_usernames():
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    query = request.args.get('q', '').strip()
    if not query: return jsonify({"users": []})
    users = User.query.filter(User.username.like(f"%{query}%")).filter(User.id != session['user_id']).limit(10).all()
    return jsonify({"users": [{"id": u.id, "username": u.username, "display_name": u.display_name or u.username, "avatar": u.profile_picture or 'uploads/profiles/default.png'} for u in users]})

@messages_bp.route('/api/messages/delete/<int:msg_id>', methods=['DELETE'])
def delete_message(msg_id):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    m = Message.query.get(msg_id)
    if not m or m.sender_id != session['user_id']: return jsonify({"error": "Forbidden"}), 403
    if (datetime.datetime.utcnow() - m.sent_at).total_seconds() > 600:
        return jsonify({"error": "Grace period expired."}), 400
    db.session.delete(m)
    db.session.commit()
    return jsonify({"success": True})

@messages_bp.route('/api/messages/block/<int:other_id>', methods=['POST'])
def toggle_block_user(other_id):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    uid = session['user_id']
    existing = BlockList.query.filter_by(blocker_id=uid, blocked_id=other_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return jsonify({"success": True, "status": "unblocked"})
    b = BlockList(blocker_id=uid, blocked_id=other_id)
    db.session.add(b)
    db.session.commit()
    return jsonify({"success": True, "status": "blocked"})

@messages_bp.route('/api/messages/delete-chat/<int:other_id>', methods=['DELETE'])
def delete_chat(other_id):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    uid = session['user_id']
    Message.query.filter(or_(and_(Message.sender_id == uid, Message.receiver_id == other_id), and_(Message.sender_id == other_id, Message.receiver_id == uid))).delete(synchronize_session=False)
    db.session.commit()
    return jsonify({"success": True})
