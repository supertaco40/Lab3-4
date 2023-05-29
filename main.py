from flask import Flask, render_template, request
import re

app = Flask(__name__)

def int_to_currency(value):
    value = str(value)[::-1]
    value = re.sub('([^ ]{3})', r'\1 ', value)
    value = value.replace('  ', ' ')
    value = value[::-1] + ' ₽'
    return value

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/', methods=['post', 'get'])
def form():
    if request.method == 'POST':
        loan_amount = int(request.form.get('loan-amount'))
        loan_term = int(request.form.get('loan-term'))
        interest_rate = float(request.form.get('interest-rate'))

        monthly_interest_rate = interest_rate / (100 * 12)
        months = loan_term * 12

        monthly_payment = ((loan_amount * monthly_interest_rate) / (1 - (1 + monthly_interest_rate) ** (-months)))
        monthly_payment = round(monthly_payment)
        total_payout = round(monthly_payment * months)
        overpayment = round(total_payout - loan_amount)

        monthly_payment = int_to_currency(monthly_payment)
        overpayment = int_to_currency(overpayment)
        total_payout = int_to_currency(total_payout)

    return render_template('index.html', monthly_payment=monthly_payment, overpayment=overpayment,
                           total_payout=total_payout, loan_amount=loan_amount, loan_term=loan_term,
                           interest_rate=interest_rate)


if __name__ == "__main__":
    app.run(debug=True)