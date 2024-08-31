from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Armen2004@localhost/Finance'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    total_balance = db.Column(db.Integer)
    income = db.Column(db.Integer)
    expenses = db.Column(db.Integer)
    savings = db.Column(db.Integer)
    houseBills = db.Column(db.Integer)
    taxes = db.Column(db.Integer)
    car_loan = db.Column(db.Integer)
    education_loan = db.Column(db.Integer)
    medical_loan = db.Column(db.Integer)
    personal_loan = db.Column(db.Integer)



class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer)
    receiver_id = db.Column(db.Integer)
    money = db.Column(db.Integer)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('start'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id 
            return redirect(url_for('main'))
        else:
            return render_template('userAuth.html', error="Invalid username or password")

    return render_template('userAuth.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmed = request.form.get('confirm_password')

        if password != confirmed:
            return render_template('signup.html', error="Passwords don't match")

        if User.query.filter_by(username=username).first():
            return render_template('signup.html', error="User already exists")

        if User.query.filter_by(email=email).first():
            return render_template('signup.html', error="Email already exists")

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('start'))

    return render_template('signup.html')

@app.route('/main', methods=['GET'])
@login_required
def main():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('start'))

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('start'))

    return render_template('index.html', user=user)

@app.route('/transactions', methods=['GET', 'POST'])
@login_required
def transactions():
    if request.method == 'POST':
        sender_id = session.get('user_id')
        receiver_id = request.form.get('receiver_id')
        money = request.form.get('money')
        
        if not sender_id or not receiver_id or not money:
            return render_template('transactions.html', error="All fields are required")
        
        try:
            money = int(money)  
            if money <= 0:
                return render_template('transactions.html', error="Amount must be greater than zero")
        except ValueError:
            return render_template('transactions.html', error="Invalid amount")

        result, message = handling_transactions(sender_id, receiver_id, money)
        if result:
            new_transaction = Transactions(sender_id=sender_id, receiver_id=receiver_id, money=money)
            try:
                db.session.add(new_transaction)
                db.session.commit()
                return render_template('transactions.html', success="Transaction has been made")
            except Exception as e:
                db.session.rollback()
                return render_template('transactions.html', error="Transaction failed: " + str(e))
        else:
            return render_template('transactions.html', error=message)

    return render_template('transactions.html')

def handling_transactions(sender_id, receiver_id, money):
    try:
        user1 = User.query.get(sender_id)
        user2 = User.query.get(receiver_id)
        if not user1 or not user2:
            return False, "Invalid user ID(s)"
        if user1.total_balance < money:
            return False, "Insufficient funds"
        
        user1.total_balance -= money
        user2.total_balance += money
        
        db.session.commit()
        return True, "Transaction successful"
    except Exception as e:
        db.session.rollback()
        return False, f"An error occurred: {e}"
    



@app.route('/pay-house-bills', methods=['GET', 'POST'])
@login_required
def houseBills():
    if request.method == 'POST':
        input_money = request.form.get('money')
        user_id = session['user_id']

        user = User.query.get(user_id)
        if not user:
            return render_template('pay-house-bills.html', error="User not found")

        try:
            input_money = int(input_money)
            if input_money <= 0:
                return render_template('pay-house-bills.html', error="Amount must be greater than zero")
        except ValueError:
            return render_template('pay-house-bills.html', error="Invalid amount")

        if user.total_balance < input_money:
            return render_template('pay-house-bills.html', error="Insufficient funds")

        user.total_balance -= input_money
        user.houseBills -= input_money 
        if user.houseBills <= 0:
            user.houseBills = 0
            return render_template('pay-house-bills.html', success = "You payed your bill")  # <----- test this feature
        try:
            db.session.commit()
            return render_template('pay-house-bills.html', success="House bill payment successful")
        except Exception as e:
            db.session.rollback()
            return render_template('pay-house-bills.html', error="Transaction failed: " + str(e))
    
    return render_template('pay-house-bills.html')

@app.route('/taxes', methods = ['GET', 'POST'])
@login_required
def taxes():
    if request.method == 'POST':
        input_money = request.form.get('money')
        user_id = session['user_id']

        user = User.query.get(user_id)
        if not user:
            return render_template('taxes.html', error="User not found")

        try:
            input_money = int(input_money)
            if input_money <= 0:
                return render_template('taxes.html', error="Amount must be greater than zero")
        except ValueError:
            return render_template('taxes.html', error="Invalid amount")

        if user.total_balance < input_money:
            return render_template('taxes.html', error="Insufficient funds")

        user.total_balance -= input_money
        user.taxes -= input_money 
        if user.taxes <= 0:
            user.taxes = 0
            return render_template('taxes.html', success = "You payed your bill")  # <----- test this feature
        try:
            db.session.commit()
            return render_template('taxes.html', success="Taxes  payment successful")
        except Exception as e:
            db.session.rollback()
            return render_template('taxes.html', error="Transaction failed: " + str(e))
    
    return render_template('taxes.html')


@app.route('/carLoan', methods = ['GET', 'POST'])
@login_required
def carLoan():
    if request.method == 'POST':
        input_money = request.form.get('money')
        user_id = session['user_id']

        user = User.query.get(user_id)
        if not user:
            return render_template('carLoan.html', error="User not found")

        try:
            input_money = int(input_money)
            if input_money <= 0:
                return render_template('carLoan.html', error="Amount must be greater than zero")
        except ValueError:
            return render_template('carLoan.html', error="Invalid amount")

        if user.total_balance < input_money:
            return render_template('carLoan.html', error="Insufficient funds")

        user.total_balance -= input_money
        user.car_loan -= input_money 
        if user.car_loan <= 0:
            user.car_loan = 0
            return render_template('carLoan.html', success = "You payed your bill")  # <----- test this feature
        try:
            db.session.commit()
            return render_template('carLoan.html', success="Car Loan payment successful")
        except Exception as e:
            db.session.rollback()
            return render_template('carLoan.html', error="Transaction failed: " + str(e))
    
    return render_template('carLoan.html')

@app.route('/educationLoan', methods = ['GET', 'POST'])
@login_required
def educationLoan():
    if request.method == 'POST':
        input_money = request.form.get('money')
        user_id = session['user_id']

        user = User.query.get(user_id)
        if not user:
            return render_template('educationLoan.html', error="User not found")

        try:
            input_money = int(input_money)
            if input_money <= 0:
                return render_template('educationLoan.html', error="Amount must be greater than zero")
        except ValueError:
            return render_template('educationLoan.html', error="Invalid amount")

        if user.total_balance < input_money:
            return render_template('educationLoan.html', error="Insufficient funds")

        user.total_balance -= input_money
        user.education_loan -= input_money 
        if user.education_loan <= 0:
            user.education_loan = 0
            return render_template('educationLoan.html', success = "You payed your bill")  # <----- test this feature
        try:
            db.session.commit()
            return render_template('educationLoan.html', success="Education Loan payment successful")
        except Exception as e:
            db.session.rollback()
            return render_template('educationLoan.html', error="Transaction failed: " + str(e))
    
    return render_template('educationLoan.html')

@app.route('/personalLoan', methods = ['GET', 'POST'])
@login_required
def personalLoan():
    if request.method == 'POST':
        input_money = request.form.get('money')
        user_id = session['user_id']

        user = User.query.get(user_id)
        if not user:
            return render_template('personalLoan.html', error="User not found")

        try:
            input_money = int(input_money)
            if input_money <= 0:
                return render_template('personalLoan.html', error="Amount must be greater than zero")
        except ValueError:
            return render_template('personalLoan.html', error="Invalid amount")

        if user.total_balance < input_money:
            return render_template('personalLoan.html', error="Insufficient funds")

        user.total_balance -= input_money
        user.personal_loan -= input_money 
        if user.personal_loan <= 0:
            user.personal_loan = 0
            return render_template('personalLoan.html', success = "You payed your bill")  # <----- test this feature
        try:
            db.session.commit()
            return render_template('personalLoan.html', success="Personal Loan payment successful")
        except Exception as e:
            db.session.rollback()
            return render_template('personalLoan.html', error="Transaction failed: " + str(e))
    
    return render_template('personalLoan.html')

@app.route('/medicalLoan', methods = ['GET', 'POST'])
@login_required
def medicalLoan():
    if request.method == 'POST':
        input_money = request.form.get('money')
        user_id = session['user_id']

        user = User.query.get(user_id)
        if not user:
            return render_template('medicalLoan.html', error="User not found")

        try:
            input_money = int(input_money)
            if input_money <= 0:
                return render_template('medicalLoan.html', error="Amount must be greater than zero")
        except ValueError:
            return render_template('medicalLoan.html', error="Invalid amount")

        if user.total_balance < input_money:
            return render_template('medicalLoan.html', error="Insufficient funds")

        user.total_balance -= input_money
        user.medical_loan -= input_money 
        if user.medical_loan <= 0:
            user.medical_loan = 0
            return render_template('medicalLoan.html', success = "You payed your bill")  # <----- test this feature
        try:
            db.session.commit()
            return render_template('medicalLoan.html', success="House bill payment successful")
        except Exception as e:
            db.session.rollback()
            return render_template('medicalLoan.html', error="Transaction failed: " + str(e))
    
    return render_template('medicalLoan.html')

@app.route('/loans', methods=['GET', 'POST'])
@login_required
def loans():
    return render_template('loans.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('start'))


@app.route('/payments', methods = ['GET', 'POST'])
@login_required
def payments():
    user_id = session['user_id']
    transactions = Transactions.query.filter_by(sender_id=user_id).all()
    return render_template('payments.html', transactions=transactions)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
