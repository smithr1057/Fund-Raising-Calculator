# Functions

# Currency formatting function
def currency(x):
    return f"${x:.2f}"


# checks user answers with valid answer
def string_checker(question, num_letters, valid_list):

    error = f"Please choose {valid_list[0]} or {valid_list[1]}"

    while True:

        # Ask user for choice (and put it in lowercase)
        response = input(question).lower()

        # iterates through list and if response is an item
        # in the list (or the first letter of an item), the
        # full item name is returned

        for i in valid_list:
            if response == i[:num_letters] or response == i:
                return i

        # output error if item not in list
        print(error)
        print()


def profit_goal(total_costs):

    # Initialise variable and error message
    error = "Please enter a valid profit goal\n"

    valid = False
    while not valid:

        # Ask for profit goal...
        response = input("What is your profit goal (eg $500 or 50%) ")

        # Check if first character is $...
        if response[0] == '$':
            profit_type = '$'
            # Get amount (everything after the $)
            amount = response[1:]

        # Check if last character is %
        elif response[-1] == '%':
            profit_type = '%'
            # Get amount (everything before the %)
            amount = response[:-1]

        else:
            # Set response to amount for now
            profit_type = 'unknown'
            amount = response

        try:
            # Check amount is a number more than zero...
            amount = float(amount)
            if amount <= 0:
                print(error)
                continue

        except ValueError:
            print(error)
            continue

        if profit_type == "unknown" and amount >= 100:
            dollar_type = string_checker(f'Do you mean {currency(amount)}. '
                                         f'ie {amount:.2f} dollars? '
                                         f'(y / n): ', 1, y_n_list)

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = '$'
            else:
                profit_type = '%'

        elif profit_type == 'unknown' and amount < 100:
            percent_type = string_checker(f'Do you mean {amount}% (y / n): '
                                          , 1, y_n_list)
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = '$'

        # return profit goal to main routine
        if profit_type == '$':
            return amount
        else:
            goal = (amount / 100) * total_costs
            return goal


# Main Routine
# Lists
y_n_list = ['yes', 'no']

all_costs = 200

# loop for quick testing
for item in range(0, 6):
    profit_target = profit_goal(all_costs)
    print(f"Profit Target: {currency(profit_target)}")
    print(f"Total Sales: {currency(all_costs + profit_target)}")
    print()
