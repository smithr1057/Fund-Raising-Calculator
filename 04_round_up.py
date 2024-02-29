import math


# Currency formatting function
def currency(x):
    return f"${x:.2f}"


# rounding function
def round_up(amount, round_to):
    return int(math.ceil(amount / round_to)) * round_to


# Main Routine
to_round = [2.75, 2.25, 2]

for item in to_round:
    rounded = round_up(item, 5)
    print(f"{currency(item)} --> {currency(rounded)}")
