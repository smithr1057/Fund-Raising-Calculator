import pandas
import math


# Functions
# Lets you change color of printed text easily
def color_text(text, color):
    # Code was found using chatGpt using prompt
    # "Python function that allows me to change the text color"
    # Code was changed a bit as some parts were unneeded

    # list of colors
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
    }

    # Prints text in specified color
    print(f"{colors[color]}{text}\033[0m")


# checks users enter an integer / float between a low and
# high number and allows 'xxx'
def num_check(question, num_type, low=None, high=None):
    # Used ChatGPT to allow the use of the letter 'x' used the prompt bellow
    # Make that function allow the letter 'x' to be used

    situation = ''
    if low is not None and high is not None:
        situation = "both"
    elif low is not None and high is None:
        situation = "low only"

    while True:
        try:
            if num_type == "int":
                # Ask the question
                response = input(question)

                # Convert the response to an integer
                response = int(response)
            else:
                # Ask the question
                response = input(question)

                # Convert the response to a float
                response = float(response)

            # Checks input is not too high or
            # too low if both upper and lower bounds are specified
            if situation == "both":
                if response < low or response > high:
                    color_text(f"Please enter a number between {low} and {high}", 'red')
                    continue

            # Checks input is not too low
            elif situation == "low only":
                if response <= low:
                    color_text(f"Please enter a number that is more than {low}", 'red')
                    continue

            return response

        except ValueError:
            color_text("Please enter an integer or 'xxx'", 'red')
            continue


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


# Currency formatting function
def currency(x):
    return f"${x:.2f}"


# Checks that users response is not blank
def not_blank(question, error):

    valid = False
    while not valid:
        response = input(question)

        if response == "":
            print(f"{error}. \nPlease try again.\n")
            continue

        else:
            return response


# Gets expenses, returns list which has
# the data frame and sub-total
def get_expenses(var_fixed):

    # Set up lists and dictionaries
    item_list = []
    quantity_list = []
    price_list = []

    variable_dict = {
        "Item": item_list,
        "Quantity": quantity_list,
        "Price": price_list
    }

    # Loop to get item, quantity and price
    while True:

        # Ask user for item
        item_name = not_blank("Item name: ",
                              "The item name can't be blank.")

        if item_name == 'xxx' and len(item_list) > 0:
            print()
            break
        elif item_name == 'xxx':
            print("You must enter at least ONE cost")
            continue

        if var_fixed == "variable":
            # Get the number of items
            quantity = num_check("Quantity: ", "int", 0)
        else:
            quantity = 1

        # Get price per item
        price = num_check("Price for a single item: $", "float", 0)
        print()

        # Add item, quantity and price to lists
        item_list.append(item_name)
        quantity_list.append(quantity)
        price_list.append(price)

    # Create the table frame for our data
    expense_frame = pandas.DataFrame(variable_dict)

    # set index
    expense_frame = expense_frame.set_index('Item')

    # Calculate the cost for each item
    expense_frame['Cost'] = expense_frame['Quantity'] * expense_frame['Price']

    # Calculate sub total
    sub_total = expense_frame['Cost'].sum()

    # Currency Formatting (using function)
    add_dollars = ['Price', 'Cost']
    for var_item in add_dollars:
        expense_frame[var_item] = expense_frame[var_item].apply(currency)

    return [expense_frame, sub_total]


# Prints out data
def expense_print(heading, frame, subtotal):
    return f'**** {heading} Costs ****\n ' \
           f'{frame}\n' \
           f'{heading} Costs: {currency(subtotal)}'


# Calculate the profit goal
def profit_goal(total_cost):

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
                                         f'(y / n): ', 1, yn_list)

            # Set profit type based on user answer above
            if dollar_type == "yes":
                profit_type = '$'
            else:
                profit_type = '%'

        elif profit_type == 'unknown' and amount < 100:
            percent_type = string_checker(f'Do you mean {amount}% (y / n): ',
                                          1, yn_list)
            if percent_type == "yes":
                profit_type = "%"
            else:
                profit_type = '$'

        # return profit goal to main routine
        if profit_type == '$':
            return amount
        else:
            goal = (amount / 100) * total_cost
            return goal


# rounding function
def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


# Main Routine
# Lists
yn_list = ['yes', 'no']

product_name = not_blank("Product name: ",
                         "The product name can't be blank.")
how_many = num_check('How many items will you be producing? ', 'int')
print()

print("Please enter your variable costs below...")

# Calculate variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

fixed_frame = ''

# Ask user if they have fixed costs
fixed_yn = string_checker("Do you have fixed costs (y / n)? ", 1, yn_list)
print()

if fixed_yn == 'yes':
    print("Please enter your fixed costs below...")
    # Calculate fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
else:
    fixed_sub = 0

# Work out total costs and profit target
all_costs = fixed_sub + variable_sub
profit_target = profit_goal(all_costs)

# Calculates total sales needed to reach goal
sales_needed = all_costs + profit_target

# ask user for rounding
round_to = num_check("Round to nearest...? $", 'int')

# Calculates recommended price
selling_price = sales_needed / how_many

recommended_price = round_up(selling_price, round_to)

print()

# *** Printing Area ***
fixed_txt = ''

product_heading = f'**** Fund Raising - {product_name} ****\n'

variable_txt = expense_print('Variable', variable_frame, variable_sub)

fixed_costs = ""

if fixed_yn == 'yes':
    fixed_txt = expense_print('Fixed', fixed_frame[['Cost']], fixed_sub)
    fixed_txt = pandas.DataFrame.to_string(fixed_frame)
    fixed_costs = f"Fixed Costs: {currency(fixed_sub)}"

# Change dataframes to strings
variable_txt = pandas.DataFrame.to_string(variable_frame)

variable_costs = f"Variable Costs {currency(variable_sub)}"


overall_costs = f"\n**** Total Costs: {currency(all_costs)} ****\n"


profit_target_sales = f'**** Profit & Sales Targets ****\n ' \
                      f'Profit Target: {currency(profit_target)}\n ' \
                      f'Total Sales: {currency(all_costs + profit_target)}\n'

pricing = f'**** Pricing ****\n ' \
          f'Minimum Price: {currency(selling_price)}\n ' \
          f'Recommended Price: {currency(recommended_price)}\n'

to_write = [product_heading, variable_txt, variable_costs, fixed_txt, fixed_costs, overall_costs,
            profit_target_sales, pricing]

# Write to file...
# create file to hold data (add .txt extension
file_name = f'{product_name}.txt'
text_file = open(file_name, 'w+')

# Heading
for item in to_write:
    print(item)
    print()
    text_file.write(item)
    text_file.write("\n\n")

# close file
text_file.close()
