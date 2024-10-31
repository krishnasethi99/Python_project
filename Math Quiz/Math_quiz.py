import random
import time
from tkinter import *
from tkinter import messagebox

# Operators and ranges
OPERATORS = ['+', '-', '*', '/']
MIN_OPERAND = 3
MAX_OPERAND = 12
TOTAL_PROBLEM = 10

# Function to generate a problem and calculate the answer
def generateProblem(min_operand, max_operand):
    num1 = random.randint(min_operand, max_operand)
    num2 = random.randint(min_operand, max_operand)
    operator = random.choice(OPERATORS)
    
    if operator == '+':
        answer = num1 + num2
    elif operator == '-':
        answer = num1 - num2
    elif operator == '*':
        answer = num1 * num2
    elif operator == '/':
        while num2 == 0:
            num2 = random.randint(min_operand, max_operand)
        answer = round(num1 / num2, 2)

    expression = f"{num1} {operator} {num2}"
    return expression, answer

# Function to handle quiz game start
def start_quiz():
    global current_problem, correct_attempt, wrong_attempt, start_time

    correct_attempt = 0
    wrong_attempt = 0
    current_problem = 0

    # Get the user input from Entry widgets
    try:
        total_problem = int(total_problems_entry.get())
        min_operand = int(min_operand_entry.get())
        max_operand = int(max_operand_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers!")
        return
    
    if min_operand > max_operand:
        messagebox.showerror("Input Error", "Minimum operand cannot be greater than maximum operand!")
        return

    # Start timer
    start_time = time.time()
    
    # Generate the first problem
    next_problem()
    
def next_problem():
    global current_problem, exp, answer

    if current_problem < int(total_problems_entry.get()):
        current_problem += 1
        problem_label.config(text=f"Problem #{current_problem}")
        
        # Generate problem
        exp, answer = generateProblem(int(min_operand_entry.get()), int(max_operand_entry.get()))
        expression_label.config(text=f"{exp} = ")
        answer_entry.delete(0, END)  # Clear input field
    else:
        end_quiz()

def check_answer():
    global correct_attempt, wrong_attempt
    
    try:
        guess = float(answer_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a numeric value!")
        return
    
    if guess == answer:
        correct_attempt += 1
        result_label.config(text="Correct!", fg="green", bg='#D3EE98', font="lucida 12 bold")

    else:
        wrong_attempt += 1
        result_label.config(text="Incorrect!", fg="red", bg='#D3EE98', font="lucida 12 bold")
    
    next_problem()

def end_quiz():
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
    
    # Display result in a messagebox
    result_message = (f"Nice Work! You have completed this challenge in {total_time} seconds.\n"
                      f"You answered {correct_attempt} out of {total_problems_entry.get()} problems correctly.\n"
                      f"You made a total of {wrong_attempt} incorrect attempts.")
    
    messagebox.showinfo("Quiz Completed", result_message)
    reset_quiz()

# Function to reset the GUI for a new game
def reset_quiz():
    total_problems_entry.delete(0, END)
    total_problems_entry.insert(0, TOTAL_PROBLEM)
    
    min_operand_entry.delete(0, END)
    min_operand_entry.insert(0, MIN_OPERAND)
    
    max_operand_entry.delete(0, END)
    max_operand_entry.insert(0, MAX_OPERAND)
    
    problem_label.config(text="Ready to start the quiz!")
    expression_label.config(text="")
    result_label.config(text="")
    answer_entry.delete(0, END)

# Tkinter GUI Setup
root = Tk()
root.title("Math Quiz Game")
root.geometry("550x425")    

# Labels and Entry fields for user configuration
Label(root, text="Enter the number of problems:", borderwidth=2, bg='#433878', fg='#e0e0e0',font="comicsansms 15", relief=RIDGE, padx=5, pady=5).grid(pady=5, row=0 , column=0)
total_problems_entry = Entry(root, borderwidth=2, bg='#e0e0e0', fg='#433878',font="comicsansms 15", relief=RIDGE)
total_problems_entry.grid(row=0, column=1, padx=10, ipadx=4, ipady=4)

Label(root, text="Enter the minimum operand:", borderwidth=2, bg='#433878', fg='#e0e0e0',font="comicsansms 15", relief=RIDGE, padx=5, pady=5).grid(pady=5, row=1 , column=0)
min_operand_entry = Entry(root, borderwidth=2, bg='#e0e0e0', fg='#433878',font="comicsansms 15", relief=RIDGE)
min_operand_entry.grid(row=1, column=1, padx=10, ipadx=4, ipady=4)

Label(root, text="Enter the maximum operand:", borderwidth=2, bg='#433878', fg='#e0e0e0',font="comicsansms 15", relief=RIDGE, padx=5, pady=5).grid(pady=5, row=2 , column=0)
max_operand_entry = Entry(root, borderwidth=2, bg='#e0e0e0', fg='#433878',font="comicsansms 15", relief=RIDGE)
max_operand_entry.grid(row=2, column=1, padx=10, ipadx=4, ipady=4)

# Problem label
problem_label = Label(root, text="Ready to start the quiz!", font="Helvetica 25", pady=10, bg='#7E60BF', fg='#FFE1FF')
problem_label.grid(row=3, columnspan=2, pady=15)

# Expression label
expression_label = Label(root, text="", font=("Helvetica", 14))
expression_label.grid(row=4, columnspan=2)

# Entry for answer
answer_entry = Entry(root, borderwidth=2, bg='#e0e0e0', fg='#433878',font="comicsansms 15", relief=RIDGE)
answer_entry.grid(row=5, columnspan=2, padx=10, ipadx=4, ipady=4)

# Result label
result_label = Label(root, text="", font=("Helvetica", 12))
result_label.grid(row=6, columnspan=2)

# Buttons to start the game and check answers
Button(root, text="Start Quiz", command=start_quiz, bg='#433878', fg='#e0e0e0', padx=5, pady=5).grid(row=7, column=0, pady=10)
Button(root, text="Submit Answer", command=check_answer, bg='#433878', fg='#e0e0e0', padx=5, pady=5).grid(row=7, column=1)

# Start the Tkinter event loop
reset_quiz()
root.mainloop()