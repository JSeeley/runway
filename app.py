from flask import Flask, request, render_template
from calculation import calculate_runway

# TO-DO:
# Have the dictionary be saved to a database
#   - Need to finish michigan courses first.
#   - Connecting SQLAlchemy and Cloud SQL: https://docs.sqlalchemy.org/en/13/dialects/mysql.html#module-sqlalchemy.dialects.mysql.mysqldb
# Add an authentication layer and the ability to save values to a user
#   - Checkout Flask-Login (https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login)
#   - Checout SQLAlchemy
#   - Flask-Bootstrap + WTF Forms (https://www.youtube.com/watch?v=S7ZLiUabaEo)
#   - All of the above wrapped into one (https://www.youtube.com/watch?v=8aTnmsDMldY)
#   - To-Do list app: https://www.youtube.com/watch?v=4kD-GRF5VPs&pbjreload=101
#   - FULL BLOG APP on CLOUDSQL and has login/auth: https://medium.com/@zainqasmi/build-and-deploy-a-python-flask-application-on-google-cloud-using-app-engine-and-cloud-sql-a3c5bde5ef4a
# Allow the user to edit their values and re-calculate their runway
# Give a wider range of suggestions 
# Make it pretty
# Share it with people
# Add entertainment expense and "boring life" runway option


# LEARNING TO-DO:
# Finish michigan course on web data

# Original starter code from: https://blog.pythonanywhere.com/169/
# Look into wtforms for forms? Does this replace "request" from Flask? Need to understand this difference more.

# db_user = os.environ.get('CLOUD_SQL_USERNAME')
# db_password = os.environ.get('CLOUD_SQL_PASSWORD')
# db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
# db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

app = Flask(__name__)
app.config["DEBUG"] = True

expenses = dict()
assets = dict()
debt = dict()

@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == "POST":
        expenses.clear()
        expenses['shelter'] = float(request.form["shelter"])
        expenses['utilities'] = float(request.form["utilities"])
        expenses['food'] = float(request.form["food"])
        expenses['insurance'] = float(request.form["insurance"])
        expenses['other'] = float(request.form["other"])
        assets['cash'] = float(request.form["cash"])
        assets['investments'] = float(request.form["investments"])
        assets['assets'] = float(request.form["assets"])
        debt['credit'] = float(request.form["credit"])
        debt['low-interest'] = float(request.form["low-interest"])
        debt['high-interest'] = float(request.form["high-interest"])

        if request.form["action"] == "Calculate Runway":
            total_expenses = sum(expenses.values())
            total_assets = sum(assets.values())
            total_debt = sum(debt.values())     
            runway_text = calculate_runway(expenses, assets, debt)
            return render_template("calculate.html", total_expenses=total_expenses, total_assets=total_assets, runway_text=runway_text, total_debt=total_debt)


    return render_template("index.html")


@app.route('/about', methods=["GET", "POST"])

def about():
    output = "hello"

    return render_template("index.html", output=output)

if __name__ == '__main__':
    app.run(debug=True)