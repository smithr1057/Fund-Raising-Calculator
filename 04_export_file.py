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
    print()
    print(f"**** {heading} Costs ****")
    print(frame)
    print()
    print(f"{heading} Costs: {currency(subtotal)}")
    return ''


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


# Main Routine
# Lists
yn_list = ['yes', 'no']

variable_dict = {
    'Item': ['Mugs', 'Printing', 'packaging'],
    'Quantity': [300, 300, 50],
    'Price': [1, .5, .75]
}

fixed_dict = {
    "Item": ['Rent', 'Artwork', 'Advertising'],
    'Price': [25, 35, 10]
}

variable_frame = pandas.DataFrame(variable_dict)
fixed_frame = pandas.DataFrame(fixed_dict)

product_name = 'Custom Mugs'
profit_target = '$100.00'
required_sales = "$200.00"
recommended_price = '$5.00'

print(variable_frame)

# Change dataframe to string
variable_txt = pandas.DataFrame.to_string(variable_frame)

# Write to file...
# create file to hold data (add .txt extension
file_name = f'{product_name}.txt'
text_file = open(file_name, 'w+')

# Heading
text_file.write(f"***** Fund Raising - {product_name} *****\n\n")

text_file.write(variable_txt)

# close file
text_file.close()

