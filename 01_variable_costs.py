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
def not_blank(question, ):

    while True:
        response = input(question)

        if response == "":
            print("Sorry this can't be blank. Please try again")

        else:
            return response


# Main Routine

# Set up lists and dictionaries

component_list = []
quantity_list = []
price_list = []


variable_dict = {
    "Component": component_list,
    "Quantity": quantity_list,
    "Price": price_list
}

item_name = not_blank("Item name: ")
print()

while True:

    # Ask user for component
    component = not_blank("Component name (or 'xxx' to quit): ")

    # if user tries to quit before adding a component output error
    if component == 'xxx' and len(component_list) > 0:
        print()
        break
    elif component == 'xxx':
        print("You must add at least ONE component before quitting")
        continue

    # Get the number of components
    quantity = num_check("Quantity: ", "int", 0)

    # Get price per component
    price = num_check("Price for a single component: $", "float", 0)
    print()

    # Add component, quantity and price to lists
    component_list.append(component)
    quantity_list.append(quantity)
    price_list.append(price)

# Create the table frame for our data
variable_frame = pandas.DataFrame(variable_dict)

# set index
variable_frame = variable_frame.set_index('Component')

# Calculate the cost for each component
variable_frame['Cost'] = variable_frame['Quantity'] * variable_frame['Price']

# Calculate overall cost
total_cost = variable_frame['Cost'].sum()

# Currency Formatting (using function)
add_dollars = ['Price', 'Cost']
for var_item in add_dollars:
    variable_frame[var_item] = variable_frame[var_item].apply(currency)

print(f'Item Name: {item_name}')

print(variable_frame)
print()

# Output variable costs
print(f'Variable costs: {currency(total_cost)}')
