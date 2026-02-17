from tkinter import E
from flask import Flask, render_template, request, url_for, make_response, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-key'
db = SQLAlchemy(app)

class expense(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(120), nullable = False)
    amount = db.Column(db.Float(120), nullable = False)
    category = db.Column(db.String(50), nullable = False)
    date = db.Column(db.Date, nullable = False, default=date.today)

with app.app_context():
    db.create_all()

Categories = ['Food', 'Transport', 'Rent', 'Utilities', 'Health']

@app.route("/")
def index():

    expenses = expense.query.order_by(expense.date.desc(), expense.id.desc()).all()
    total = round(sum(e.amount for e in expenses))

    return render_template(
        "index.html", 
        expenses=expenses,
        categories=Categories,
        total=total
        )

@app.route("/add", methods=['post'])
def add(): 
    description = (request.form.get("description") or "").strip()
    amount_str = (request.form.get("amount") or "").strip()
    category = (request.form.get("category") or "").strip()
    date_str = (request.form.get("date") or "").strip()

    if not description or not amount_str or not category:
        flash("please fill description, amount, and category", "error")
        return redirect(url_for("index"))
    
    try:
        amount = float(amount_str)
        if amount < 0:
            raise ValueError
    except ValueError:
        flash("Amount must be positive number, greater than 0", "error")
        return redirect(url_for("index"))

    try:
        if date_str:
            d = datetime.strptime(date_str,"%Y-%m-%d").date()
        else:
            d = date.today()
    except ValueError:
        d = date.today()
    
    e = expense(description=description, amount=amount, category=category, date=d)
    db.session.add(e)
    db.session.commit()

    flash("Expense added", "success")

    print("form recieved", dict(request.form))
    return redirect(url_for("index"))

@app.route('/delete/<int:expense_id>',methods=['POST'])
def delete(expense_id):
    e = expense.query.get_or_404(expense_id)
    db.session.delete(e)
    db.session.commit()
    flash("Expense deleted", "success")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)