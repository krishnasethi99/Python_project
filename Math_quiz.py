import random
import time

OPERATORS = ['+', '-', '*', '/']
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEM = 10

# Function to generate a problem and calculate the answer
def generateProblem(min_operand, max_operand):
    num1 = random.randint(min_operand, max_operand)
    num2 = random.randint(min_operand, max_operand)
    operators = random.choice(OPERATORS)
    
    if operators == '+':
        answer = num1 + num2
    elif operators == '-':
        answer = num1 - num2
    elif operators == '*':
        answer = num1 * num2
    elif operators == '/':
        # Ensure the denominator is not zero and limit to 2 decimal places
        while num2 == 0:
            num2 = random.randint(min_operand, max_operand)
        answer = round(num1 / num2, 2) 

    exp = f"{num1} {operators} {num2}"
    return exp, answer

# Function to get user input for configuration with validation
def get_user_config():
    while True:
        try:
            total_problem_input = int(input("Enter the number of problems (default is 10): "))
            if total_problem_input:
                total_problem = total_problem_input
            else:
                total_problem = TOTAL_PROBLEM

            min_operand_input = int(input("Enter the minimum operand (default is 3): "))
            if min_operand_input:
                min_operand = min_operand_input
            else:
                min_operand = MIN_OPERAND

            max_operand_input = int(input("Enter the maximum operand (default is 12): "))
            if max_operand_input:
                max_operand = max_operand_input
            else:
                max_operand = MAX_OPERAND

            # Ensure that min_operand is less than or equal to max_operand
            if min_operand > max_operand:
                print("Minimum operand cannot be greater than maximum operand. Please try again.")
                continue

            return total_problem, min_operand, max_operand

        except ValueError:
            print("Invalid input. Please enter a numeric value or press Enter to use the default value.")

# Main function to handle the quiz game
def play_quiz():
    correct_attempt = 0
    wrong_attempt = 0

    # Get user configuration for the quiz
    total_problem, min_operand, max_operand = get_user_config()

    print("Press Enter to start the game:")
    input()
    print("---------------------------------")

    # Start the timer
    start_time = time.time()

    # Loop through problems
    for i in range(total_problem):
        exp, answer = generateProblem(min_operand, max_operand)
        attempts = 0

        while True:
            try:
                guess_input = float(input(f"Problem #{i + 1}: {exp} = "))
                guess = guess_input
                attempts += 1

                if(guess == answer):
                    print(f"Correct! You got it in {attempts} attempts.")
                    correct_attempt += 1
                    break
                else:
                    print("Incorrect! Try again.")
                    wrong_attempt += 1

            except ValueError:
                print("Invalid input. Please enter a numeric value.")

    # End the timer
    end_time = time.time()
    # Calculate total time taken
    total_time = round(end_time - start_time, 2)

    # Display the results
    print("----------------------------------")
    print(f"Nice Work! You have completed this challenge in {total_time} seconds.")
    print(f"You answered {correct_attempt} out of {total_problem} problems correctly.")
    print(f"You made a total of {wrong_attempt} incorrect attempts.")
    print("----------------------------------")

# Main loop to ask if the user wants to play again
if  __name__ == "__main__":

    while True:
        play_quiz()
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again not in ['yes', 'y']:
            print("Thank you for playing! Goodbye.")
            break