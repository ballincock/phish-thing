from flask import Blueprint, render_template, request

support = Blueprint('support', __name__, template_folder='templates')

@support.route('/donate', methods=['GET', 'POST'])
def donate():
    if request.method == 'POST':
        amount = request.form.get('amount')
        custom_amount = request.form.get('custom_amount')
        
        final_amount = custom_amount if custom_amount else amount
        
        # TODO: Handle payment processing here
        return f"Thank you for donating ${final_amount}!"
        
    return render_template('donate.html')
