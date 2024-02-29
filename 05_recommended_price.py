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


# Currency formatting function
def currency(x):
    return f"${x:.2f}"


# rounding function
def round_up(amount, var_round_to):
    return int(math.ceil(amount / var_round_to)) * var_round_to


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


# Main Routine
how_many = num_check('How many items? ', 'int', 0)
total = num_check("Total Costs? ", 'float', 0)
profit_goal = num_check("Profit Goal? ", 'float', 0)
round_to = num_check("Round to nearest? ", 'int', 0)

sales_needed = total + profit_goal

print(f"Total: {currency(total)}")
print(f"Profit Goal: {currency(profit_goal)}")

selling_price = sales_needed / how_many
print(f"Selling Price (un-rounded): {currency(selling_price)}")

recommended_price = round_up(selling_price, round_to)
print(f"Recommended Price: {currency(recommended_price)}")

