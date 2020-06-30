def runway_length(items):

    # Calculating totals for each item_type
    total_expenses = sum(list([amount for (item_type_id, item_name_id, amount) in items if item_type_id == 1]))
    total_assets = sum(list([amount for (item_type_id, item_name_id, amount) in items if item_type_id == 2]))
    total_debt = sum(list([amount for (item_type_id, item_name_id, amount) in items if item_type_id == 3]))
    total_income = sum(list([amount for (item_type_id, item_name_id, amount) in items if item_type_id == 4]))
    cash = sum(list([amount for (item_type_id, item_name_id, amount) in items if item_type_id == 1 and item_name_id == 1]))
    other expenses = sum(list([amount for (item_type_id, item_name_id, amount) in items if item_type_id == 1 and item_name_id == 5]))

    # Using item_type totals to do simple runway length calculation
    runway_length = (total_assets - total_debt) / total_expenses

    # Income over expenses

    # if total_expenses - total_income > :
    #     if total_expenses - other_expenses - income > 0:
    #         goal1_text = "Focus on reducing your expenses to be less than "

    # SUPER Emergency Fund caculation

    if total_expenses > 1000:
        super_emergency_fund = total_expenses
    else:
        super_emergency_fund = 1000

    if super_emergency_fund > cash:
        if super_emergency_fund == 1000:
            super_emergency_fund_text = 'If you had a financial emergency, you would have $' + str(cash) + ' to cover it. Work to get your cash up to $1000.'
        else:
            super_emergency_fund_text = 'If you lost your income, you would not be able to pay one month of expenses. Try to get your cash up to to $' + str(super_emergency_fund)
    else:
        super_emergency_fund_text = 'Success! You are prepared! In the case of a short-term financial emergency, you have enough cash to cover one month of expenses.'

    # Emergency Fund caculation

    emergency_fund = total_expenses * 6

    if emergency_fund > cash:
        emergency_fund_text = 'You do not have enough cash to cover six months of your expenses. Consider saving $' + str(emergency_fund) + ' so you can make it through a longer term financial emergency.'
    else:
        emergency_fund_text = 'Success! You are prepared! Because you have more than $' + str(emergency_fund) + ' in cash, you could continue living the way you are now for six months if you lost your job.'

    # PLACEHOLDER FOR CALCULATING EMPLOYEE MATCH








    return total_expenses, total_assets, total_debt, total_income, runway_length, super_emergency_fund_text, emergency_fund_text