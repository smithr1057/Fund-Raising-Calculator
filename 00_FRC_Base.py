import pandas


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
    item_name = ''
    while item_name.lower() != "xxx":

        # Ask user for item
        item_name = not_blank("Item name: ",
                              "The item name can't be blank.")
        if item_name.lower() == 'xxx':
            break

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
    print()
    print(f"**** {heading} Costs ****")
    print(frame)
    print()
    print(f"{heading} Costs: {currency(subtotal)}")
    return ''


# Main Routine
# Lists
yn_list = ['yes', 'no']

product_name = not_blank("Product name: ",
                         "The product name can't be blank.")
print()

print("Please enter your variable costs below...")

# Calculate variable costs
variable_expenses = get_expenses("variable")
variable_frame = variable_expenses[0]
variable_sub = variable_expenses[1]

fixed_frame = ''

# Ask user if they have fixed costs
fixed_costs = string_checker("Do you have fixed costs (y / n)? ", 1, yn_list)

if fixed_costs == 'yes':
    print("Please enter your fixed costs below...")
    # Calculate fixed costs
    fixed_expenses = get_expenses("fixed")
    fixed_frame = fixed_expenses[0]
    fixed_sub = fixed_expenses[1]
else:
    fixed_sub = 0

# *** Printing Area ***

print(f'Product: {product_name}')
print()

expense_print('Variable', variable_frame, variable_sub)

if fixed_costs == 'yes':
    expense_print('Fixed', fixed_frame[['Cost']], fixed_sub)
