from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from app.models.user.user import db, User 
from app.models.user.ticket import Ticket, TicketMessage

tickets_bp = Blueprint('tickets', __name__, template_folder='../../templates')

def get_current_user_id():
    return session.get('user_id')

@tickets_bp.route('/tickets', methods=['GET', 'POST'])
def portal():
    user_id = get_current_user_id()
    if not user_id:
        flash("Please log in to access tickets.", "error")
        return redirect(url_for('auth.login')) 
        
    user = User.query.get_or_404(user_id)
    is_admin = (user_id == 1)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        message_text = request.form.get('message', '').strip()
        
        if not title or not message_text:
            flash("Title and message cannot be empty.", "warning")
        elif len(message_text) > 1000:
            flash("Message exceeds 1000 characters.", "warning")
        else:
            new_ticket = Ticket(client_id=user_id, title=title, status='Open')
            db.session.add(new_ticket)
            db.session.flush() 
            
            first_msg = TicketMessage(ticket_id=new_ticket.id, sender_id=user_id, message=message_text)
            db.session.add(first_msg)
            db.session.commit()
            flash("Ticket created successfully!", "success")
            return redirect(url_for('tickets.portal'))

    if is_admin:
        active_tickets = Ticket.query.filter_by(status='Open').order_by(Ticket.created_at.desc()).all()
        resolved_tickets = Ticket.query.filter_by(status='Resolved').order_by(Ticket.created_at.desc()).all()
    else:
        active_tickets = Ticket.query.filter_by(client_id=user_id, status='Open').order_by(Ticket.created_at.desc()).all()
        resolved_tickets = Ticket.query.filter_by(client_id=user_id, status='Resolved').order_by(Ticket.created_at.desc()).all()

    return render_template('tickets/portal.html', active_tickets=active_tickets, resolved_tickets=resolved_tickets, is_admin=is_admin)

@tickets_bp.route('/tickets/<int:ticket_id>', methods=['GET', 'POST'])
def view_ticket(ticket_id):
    user_id = get_current_user_id()
    if not user_id:
        abort(401)
        
    ticket = Ticket.query.get_or_404(ticket_id)
    is_admin = (user_id == 1)
    
    if not is_admin and ticket.client_id != user_id:
        abort(403)

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'toggle_status' and is_admin:
            ticket.status = 'Resolved' if ticket.status == 'Open' else 'Open'
            db.session.commit()
            flash(f"Ticket status marked as {ticket.status}.", "success")
            return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))

        message_text = request.form.get('message', '').strip()
        if not message_text:
            flash("Reply text cannot be empty.", "warning")
        elif len(message_text) > 1000:
            flash("Reply exceeds 1000 characters.", "warning")
        else:
            reply = TicketMessage(ticket_id=ticket.id, sender_id=user_id, message=message_text)
            db.session.add(reply)
            db.session.commit()
            flash("Reply sent successfully.", "success")
            return redirect(url_for('tickets.view_ticket', ticket_id=ticket.id))

    return render_template('tickets/view.html', ticket=ticket, is_admin=is_admin, current_user_id=user_id)

@tickets_bp.route('/tickets/admin-panel')
def admin_panel():
    user_id = get_current_user_id()
    if user_id != 1:
        abort(403)
        
    all_tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    return render_template('tickets/admin_panel.html', all_tickets=all_tickets)
