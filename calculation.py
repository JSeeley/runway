import statistics
from flask import Flask, request, render_template

# if assets - debt < 0: Focus on reducing expenses, selling assets, and paying down debt
# if assets - debt < $10,000: Focus on building an emergency fund.
# if assets - debt <


def calculate_runway(expenses, assets, debt):
    total_expenses = sum(expenses.values())
    total_assets = sum(assets.values())
    total_debt = sum(debt.values())
    net_assets = total_assets - total_debt
    runway = (total_assets - total_debt) / total_expenses
    runway_response = "You can make it " + str(runway) + " months without any income before you reach your $10,000 emergency fund"
    runway_response_2 = "You can only make it " + str(runway) + "months without any income before reaching $10,000 in emergency funds. We recommend cutting some of your non-essential expenses, paying off any debt, and increasing your assets to extend your runway."
    runway_response_3 = "Because your total assets are under $10,000, we recommend cutting some non-essential expenses and working to build your assets to over $10,000 to protect you against financial emergencies."
    if net_assets > 10000 and runway > 2:
        runway_text = runway_response
        return runway_text
    elif net_assets > 10000 and runway <= 2:
        runway_text = runway_response_2
        return runway_text
    else:
        runway_text = runway_response_3
        return runway_text
        
    