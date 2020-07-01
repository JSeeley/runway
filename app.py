from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
import mysql.connector  
from wtforms import Form, StringField, IntegerField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import calculate

app = Flask(__name__)

# Config MySQL
cnx = mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    password='qweedle2',
    database='runway',
    buffered=True)

# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')

# Register Form Class
class RegisterForm(Form):
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = cnx.cursor(dictionary=True)

        # Execute query
        cur.execute("INSERT INTO email(email, password) VALUES( %s, %s)", (email, password))

        # Commit to DB
        cnx.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form['email']
        password_candidate = request.form['password']

        # Create cursor
        cur = cnx.cursor(dictionary=True)

        # Get user by username and fetch it from the database
        cur.execute("SELECT * FROM email WHERE email = %s", [email])
        data = cur.fetchone()

        # True if the username is found in the database
        if data != None:
            # Get stored hash
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email

                flash('You are now logged in', 'success')
                return redirect(url_for('runway'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        
        # Close connection
            cur.close()

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Your Runway
@app.route('/runway')
@is_logged_in
def runway():
        
    # Create cursor
    cur = cnx.cursor()

    # Ugly query to turn the users email into email_id so it can be used in the insert function. REALLY needs refactor.
    user_list = [session['email']]
    user = user_list[0]
    cur.execute("SELECT email_id FROM email WHERE email=%s", [user])
    user_email_dict = str(cur.fetchall())
    user_email = ''.join(i for i in user_email_dict if i.isdigit())

    # Show runway only from the user logged in
    cur.execute("SELECT item_type_id, item_name_id, amount FROM items WHERE email_id=%s", [user_email])

    # Query for grabbing every item a user has ever input 
    # cur.execute("SELECT * FROM items JOIN email ON email.email_id = items.email_id JOIN item_name ON items.item_name_id = item_name.item_name_id JOIN item_type ON items.item_type_id = item_type.item_type_id WHERE email = %s", [session['email']])

    # Get runway if the user has one or send them to the build runway landing page
    items = cur.fetchall()

    cur.execute("SELECT * FROM to_do WHERE email_id=%s", [user_email])

    to_do = cur.fetchall()

    if items != []:
        runway_calc = calculate.runway_length(items)
        return render_template('runway.html', runway_calc=runway_calc, to_do=to_do)
    else:
        return render_template('build_runway.html')
    # Close connection
    cur.close()

# Add Expenses Form Class
class ExpensesForm(Form):
    rent = IntegerField('Rent', [validators.NumberRange(min=0, max=99999999999)])
    utilities = IntegerField('Utilities', [validators.NumberRange(min=0, max=99999999999)])
    food = IntegerField('Food and Toiletries', [validators.NumberRange(min=0, max=99999999999)])
    income_expenses = IntegerField('Income Earning Expenses', [validators.NumberRange(min=0, max=99999999999)])
    insurance = IntegerField('Insurance and Healthcare', [validators.NumberRange(min=0, max=99999999999)])
    other = IntegerField('All Other Expenses', [validators.NumberRange(min=0, max=99999999999)])

# Add Expenses
@app.route('/add_expenses', methods=['GET', 'POST'])
@is_logged_in
def add_expenses():
    form = ExpensesForm(request.form)
    if request.method == 'POST' and form.validate():
        rent = form.rent.data
        utilities = form.utilities.data
        food = form.food.data
        income_expenses = form.income_expenses.data
        insurance = form.insurance.data
        other = form.other.data

        # Expenses has item_type_id of 1 in the DB. This value is used in the SQL function.
        item_type_id = 1

        # Create cursor
        cur = cnx.cursor(dictionary=True)

        # Ugly query to turn the users email into email_id so it can be used in the insert function. REALLY needs refactor.
        user_list = [session['email']]
        user = user_list[0]
        cur.execute("SELECT email_id FROM email WHERE email=%s", [user])
        user_email_dict = str(cur.fetchall())
        user_email = ''.join(i for i in user_email_dict if i.isdigit())
        

        # Insert form values into DB
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 1, item_type_id, rent, 0))
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 2, item_type_id, utilities, 0))
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 3, item_type_id, food, 0))
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 12, item_type_id, income_expenses, 0))
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 4, item_type_id, insurance, 0))
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 5, item_type_id, other, 0))
        
        # Commit to DB
        cnx.commit()

        #Close connection
        cur.close()

        flash('Expenses Saved', 'success')

        return redirect(url_for('add_assets'))

    return render_template('add_expenses.html', form=form)

# Add Assets Form Class
class AssetsForm(Form):
    cash = IntegerField('Cash', [validators.NumberRange(min=0, max=99999999999)])
    investments = IntegerField('Value of Investments', [validators.NumberRange(min=0, max=99999999999)])
    assets = IntegerField('Value of Assets', [validators.NumberRange(min=0, max=99999999999)])

# Add Assets
@app.route('/add_assets', methods=['GET', 'POST'])
@is_logged_in
def add_assets():
    form = AssetsForm(request.form)
    if request.method == 'POST' and form.validate():
        cash = form.cash.data
        investments = form.investments.data
        assets = form.assets.data

        # Assets has item_type_id of 2 in the DB. This value is used in the SQL function.
        item_type_id = 2

        # Create cursor
        cur = cnx.cursor(dictionary=True)

        # Ugly query to turn the users email into email_id so it can be used in the insert function. REALLY needs refactor.
        user_list = [session['email']]
        user = user_list[0]
        cur.execute("SELECT email_id FROM email WHERE email=%s", [user])
        user_email_dict = str(cur.fetchall())
        user_email = ''.join(i for i in user_email_dict if i.isdigit())
        

        # Insert form values into DB
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 6, item_type_id, cash, 0))
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 7, item_type_id, investments, 0))
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 8, item_type_id, assets, 0))
        
        # Commit to DB
        cnx.commit()

        #Close connection
        cur.close()

        flash('Assets Saved', 'success')

        return redirect(url_for('add_debt'))

    return render_template('add_assets.html', form=form)

# Add Debt Form Class
class DebtForm(Form):
    no_interest = IntegerField('0% Interest Debt', [validators.NumberRange(min=0, max=99999999999)])
    low_interest = IntegerField('.1 to 5% Interest Debt', [validators.NumberRange(min=0, max=99999999999)])
    high_interest = IntegerField('5%+ Interest Debt', [validators.NumberRange(min=0, max=99999999999)])

# Add Debt
@app.route('/add_debt', methods=['GET', 'POST'])
@is_logged_in
def add_debt():
    form = DebtForm(request.form)
    if request.method == 'POST' and form.validate():
        no_interest = form.no_interest.data
        low_interest = form.low_interest.data
        high_interest = form.high_interest.data

        # Assets has item_type_id of 2 in the DB. This value is used in the SQL function.
        item_type_id = 3

        # Create cursor
        cur = cnx.cursor(dictionary=True)

        # Ugly query to turn the users email into email_id so it can be used in the insert function. REALLY needs refactor.
        user_list = [session['email']]
        user = user_list[0]
        cur.execute("SELECT email_id FROM email WHERE email=%s", [user])
        user_email_dict = str(cur.fetchall())
        user_email = ''.join(i for i in user_email_dict if i.isdigit())
        

        # Insert form values into DB
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 9, item_type_id, no_interest, 0))
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 10, item_type_id, low_interest, 0))
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 11, item_type_id, high_interest, 0))
        
        # Commit to DB
        cnx.commit()

        #Close connection
        cur.close()

        flash('Debt Saved', 'success')

        return redirect(url_for('add_income'))

    return render_template('add_debt.html', form=form)

# Add Income Form Class
class IncomeForm(Form):
    income = IntegerField('Monthly Income', [validators.NumberRange(min=0, max=99999999999)])

# Add Income
@app.route('/add_income', methods=['GET', 'POST'])
@is_logged_in
def add_income():
    form = IncomeForm(request.form)
    if request.method == 'POST' and form.validate():
        income = form.income.data

        # Assets has item_type_id of 2 in the DB. This value is used in the SQL function.
        item_type_id = 4

        # Create cursor
        cur = cnx.cursor(dictionary=True)

        # Ugly query to turn the users email into email_id so it can be used in the insert function. REALLY needs refactor.
        user_list = [session['email']]
        user = user_list[0]
        cur.execute("SELECT email_id FROM email WHERE email=%s", [user])
        user_email_dict = str(cur.fetchall())
        user_email = ''.join(i for i in user_email_dict if i.isdigit())
        

        # Insert form values into DB
        cur.execute("INSERT INTO items(email_id, item_name_id, item_type_id, amount, percentage) VALUES( %s, %s, %s, %s, %s)", (user_email, 1, item_type_id, income, 0))
        
        # Commit to DB
        cnx.commit()

        #Close connection
        cur.close()

        return redirect(url_for('runway'))

    return render_template('add_income.html', form=form)

# # Edit Article
# @app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
# @is_logged_in
# def edit_article(id):
#     # Create cursor
#     cur = cnx.cursor(dictionary=True)

#     # Get article by id
#     cur.execute("SELECT * FROM articles WHERE id = %s", [id])

#     article = cur.fetchone()
#     cur.close()
#     # Get form
#     form = ArticleForm(request.form)

#     # Populate article form fields
#     form.title.data = article['title']
#     form.body.data = article['body']

#     if request.method == 'POST' and form.validate():
#         title = request.form['title']
#         body = request.form['body']

#         # Create Cursor
#         cur = cnx.cursor(dictionary=True)
#         app.logger.info(title)
#         # Execute
#         cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
#         # Commit to DB
#         cnx.commit()

#         #Close connection
#         cur.close()

#         flash('Article Updated', 'success')

#         return redirect(url_for('dashboard'))

#     return render_template('edit_article.html', form=form)

# # Delete Article
# @app.route('/delete_article/<string:id>', methods=['POST'])
# @is_logged_in
# def delete_article(id):
#     # Create cursor
#     cur = cnx.cursor(dictionary=True)

#     # Execute
#     cur.execute("DELETE FROM articles WHERE id = %s", [id])

#     # Commit to DB
#     cnx.commit()

#     #Close connection
#     cur.close()

#     flash('Article Deleted', 'success')

#     return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
