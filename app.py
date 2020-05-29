from flask import Flask, request, render_template
from calculation import calculate_runway

# TO-DO:
# BOOM BABY! DONE 1.) Accept the form values as a dictionary. 
# DONE. 2.) Prompt the user for asset values and save as a dictionary.
# DONE 3.) Write a function that takes in an expense dictionary and an asset dictionary and calculates basic runway.
# 4.) Print out full dictionary with the runway answer.
# 5.) Provide the user with an alternative runway if their investments grew at 7%
# 6.) Allow the user to edit their values and re-calculate their runway.
# 7.) Make it pretty
# 8.) Add entertainment expense and "boring life" runway option
# Original starter code from: https://blog.pythonanywhere.com/169/
# Look into wtforms for forms? Does this replace "request" from Flask? Need to understand this difference more.

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