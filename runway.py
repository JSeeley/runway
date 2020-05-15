"""
File: runway.py
----------------
"""

def main():
    welcome()
    total_expenses = get_expenses()
    liquid_assets = get_liquid_assets()
    calculate_runway(total_expenses, liquid_assets)

def welcome():
    print('Welcome! Personal Runway is a tool that calculates when you would run out of money if you did not have income.')
    input('Press enter to get started')

def get_expenses():
    shelter = int(input('How much is your rent or mortgage per month?'))
    food = int(input('About how much do you spend on food each month?'))
    utilities = int(input('About how much do you spend on insurance and utilities?'))
    other_expenses = int(input('About how much do you spend on all other monthly expenses?'))
    total_expenses = shelter + food + utilities + other_expenses
    input('Great! Your total monthly expenses are $' + str(total_expenses) + ". Let's move onto the $$$$....Press enter to continue.")
    return total_expenses

def get_liquid_assets():
    cash = int(input('How much cash do you have in your bank account?'))
    investments = int(input('What is the current value of your investments outside of your retirement investment accounts?'))
    assets = int(input('What is the value of any assets you may own? (For example: A house or car that is paid off.)'))
    liquid_assets = cash + investments + assets
    input('Great! Your total liquid assets are $' + str(liquid_assets) + ". Press enter to calculate your personal runway.")
    return liquid_assets

def calculate_runway(expenses, assets):
    runway = assets / expenses
    print('With monthly expenses of $' + str(expenses) + ' and assets of $' + str(assets) +
          ', you could live without income for ' + str(runway) + " months!")



if __name__ == '__main__':
    main()