import random
import time
import tkinter as tk
from tkinter import messagebox

class TypingTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")

        # Initialize user stats
        self.total_tests = 0
        self.total_speed = 0
        self.best_speed = 0
        self.highest_accuracy = 0
        self.test_in_progress = False
        self.is_timed_test = False
        self.remaining_time = 60  # Default time limit
        self.time_limit = 60  # Default to 60 seconds for timed test
        self.difficulty_level = 'Easy'  # Default difficulty
        self.correct_count = 0
        self.incorrect_count = 0

        # Create GUI components
        self.label_test_phrase = tk.Label(root, text="Typing Speed Test", borderwidth=12, fg='#e0e0e0', bg='#433878',font="Arial 25 bold", relief="ridge", padx=5, pady=5)
        self.label_test_phrase.pack(pady=(10, 30), padx=20)

        # Difficulty selection
        self.difficulty_var = tk.StringVar(value="Easy")
        difficulty_frame = tk.Frame(root)
        self.easy_radio = tk.Radiobutton(difficulty_frame, text="Easy", variable=self.difficulty_var, value="Easy", borderwidth=5, bg='#e0e0e0', fg='#433878',font="comicsansms 15 bold", relief="ridge", padx=5, pady=5)
        self.medium_radio = tk.Radiobutton(difficulty_frame, text="Medium", variable=self.difficulty_var, value="Medium", borderwidth=5, bg='#e0e0e0', fg='#433878',font="comicsansms 15 bold", relief="ridge", padx=5, pady=5)
        self.hard_radio = tk.Radiobutton(difficulty_frame, text="Hard", variable=self.difficulty_var, value="Hard", borderwidth=5, bg='#e0e0e0', fg='#433878',font="comicsansms 15 bold", relief="ridge", padx=5, pady=5)
        self.easy_radio.pack(side=tk.LEFT)
        self.medium_radio.pack(side=tk.LEFT)
        self.hard_radio.pack(side=tk.LEFT)
        difficulty_frame.pack(pady=(5, 10))


        # Create Text widget for user input
        self.user_input = tk.Text(root, height=4, width=50, font="Arial 12")
        self.user_input.pack(pady=5)
        self.user_input.bind("<KeyRelease>", self.real_time_feedback)

        # Buttons
        self.start_button = tk.Button(root, text="Start Test", command=self.start_test, borderwidth=5, fg='#e0e0e0', bg='#433878',font="comicsansms 12 bold", relief="ridge", padx=5, pady=5)
        self.start_button.pack(pady=(10, 5))

        self.timed_test_button = tk.Button(root, text="Start Timed Test", command=self.start_timed_test, borderwidth=5, fg='#e0e0e0', bg='#433878',font="comicsansms 12 bold", relief="ridge", padx=5, pady=5)
        self.timed_test_button.pack(pady=5)

        self.label_speed = tk.Label(root, text="Speed: 0 WPM", bg='white', fg='#433878',font="comicsansms 12 bold", padx=5, pady=5)
        self.label_speed.pack(pady=(5, 0))

        self.label_accuracy = tk.Label(root, text="Accuracy: 100%", bg='white', fg='#433878',font="comicsansms 12 bold", padx=5, pady=5)
        self.label_accuracy.pack(pady=0)

        self.label_timer = tk.Label(root, text="Time Left: 60s", bg='white', fg='#433878',font="comicsansms 12 bold", padx=5, pady=5)
        self.label_timer.pack(pady=(0, 5))

        self.stats_button = tk.Button(root, text="Show Stats", command=self.show_stats, borderwidth=2, bg='#e0e0e0', fg='#433878',font="comicsansms 12 bold", relief="ridge", padx=5, pady=5)
        self.stats_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset", command=self.reset_test, borderwidth=2, bg='#e0e0e0', fg='#433878',font="comicsansms 12 bold", relief="ridge", padx=5, pady=5)
        self.reset_button.pack(pady=5)

    def start_test(self):
        """Starts a normal (non-timed) typing test."""
        self.is_timed_test = False
        self.label_timer.config(text="")  # Hide timer for normal test
        self.setup_test()
        self.enable_difficulty_buttons()  # Enable difficulty buttons
        self.start_button.config(state=tk.NORMAL)  # Enable Start Test button
        self.timed_test_button.config(state=tk.DISABLED)  # Disable Timed Test button

    def start_timed_test(self):
        """Starts a timed typing test (default: 60 seconds)."""
        
        self.is_timed_test = True
        self.correct_count = 0
        self.incorrect_count = 0
        self.setup_test()
        self.remaining_time = self.time_limit  # Reset timer
        self.label_timer.config(text=f"Time Left: {self.remaining_time}s")  # Update initial timer display
        self.update_timer()  # Start the timer
        self.disable_difficulty_buttons()  # Disable difficulty buttons
        self.start_button.config(state=tk.DISABLED)  # Disable Start Test button

    def setup_test(self):
        """Initializes the typing test (either timed or untimed)."""
        self.test_phrases = {
            "Easy": [
                "Programming", "List", "Dictionary", "Tuple", "Python", "Code", "Test", "Typing", "Speed", "Accuracy",  "Practice",
            ],
            "Medium": [
                "Typing speed tests are fun and challenging.",
                "Python is a versatile programming language.",
                "A typing test helps improve accuracy and speed.",
                "Typing speed is measured in words per minute.",
                "Practice makes perfect when it comes to typing.",
            ],
            "Hard": [
                "Understanding recursion is crucial for mastering algorithms in Python.",
                "Python's decorators allow you to modify the behavior of a function or method.",
                "Using list comprehensions can significantly improve the performance of your code.",
                "Handling exceptions properly is essential for writing robust Python applications."
            ]
        }

        self.test_phrase = random.choice(self.test_phrases[self.difficulty_var.get()])
        self.label_test_phrase.config(text=self.test_phrase)
        self.user_input.config(state=tk.NORMAL)
        self.user_input.delete(1.0, tk.END)
        self.start_time = time.time()
        self.test_in_progress = True

    def update_timer(self):
        """Updates the timer every second during the timed test."""
        if self.test_in_progress and self.is_timed_test:
            if self.remaining_time > 0:
                self.label_timer.config(text=f"Time Left: {self.remaining_time}s")
                self.remaining_time -= 1
                self.root.after(1000, self.update_timer)  # Schedule the next update in 1 second
            else:
                self.end_timed_test()

    def end_timed_test(self):
        """Ends the timed test automatically after the time limit."""
        if self.test_in_progress:
            self.test_in_progress = False
            self.show_results()
            self.enable_difficulty_buttons()  # Re-enable difficulty buttons after test ends
            self.start_button.config(state=tk.NORMAL)  # Re-enable Start Test button
            self.timed_test_button.config(state=tk.NORMAL)  # Re-enable Timed Test button

    def calculate_results(self):
        """Calculates speed (WPM) and accuracy, and updates the UI for each phrase."""
        elapsed_time = time.time() - self.start_time
        user_text = self.user_input.get(1.0, tk.END).strip()

        # Calculate speed in Words Per Minute (WPM)
        speed = (len(user_text.split()) / elapsed_time) * 60 if elapsed_time > 0 else 0
        speed = round(speed, 2)

        # Calculate mistakes and accuracy
        errors = self.mistake(self.test_phrase, user_text)
        accuracy = 100 - (errors / max(len(self.test_phrase), 1) * 100)
        accuracy = round(accuracy, 2)  # Rounding for display

        # Update speed and accuracy in labels
        self.label_speed.config(text=f"Speed: {speed} WPM")
        self.label_accuracy.config(text=f"Accuracy: {accuracy:.2f}%")

        # Update stats for "Show Stats" button
        self.total_tests += 1
        self.total_speed += speed
        self.best_speed = max(self.best_speed, speed)
        self.highest_accuracy = max(self.highest_accuracy, accuracy)

        # Track correct/incorrect counts for timed test
        if accuracy == 100:
            self.correct_count += 1
        else:
            self.incorrect_count += 1

        # If timed test is ongoing, load a new phrase
        if self.is_timed_test and self.test_in_progress:
            self.setup_test()
        else:
            self.test_in_progress = False

    def mistake(self, par_test, user_test):
        """Counts mistakes and returns the number of errors."""
        errors = 0

        # Clear the previous highlights
        self.user_input.config(state=tk.NORMAL)
        self.user_input.delete(1.0, tk.END)

        # Compare user input with the test phrase
        for i in range(len(par_test)):
            if i < len(user_test):
                if user_test[i] == par_test[i]:
                    self.user_input.insert(tk.END, user_test[i], "correct")
                else:
                    self.user_input.insert(tk.END, user_test[i], "incorrect")
                    errors += 1
            else:
                # When user_test is shorter, highlight remaining characters from par_test
                self.user_input.insert(tk.END, par_test[i:], "remaining")
                break  # Exit the loop once we start highlighting remaining characters

        # Handle the case where user_test is longer than par_test
        if len(user_test) > len(par_test):
            self.user_input.insert(tk.END, user_test[len(par_test):], "incorrect")
            errors += len(user_test) - len(par_test)  # Count the extra characters as errors

        return errors


    def real_time_feedback(self, event):
        """Provides real-time feedback during typing."""
        if self.test_in_progress:
            user_text = self.user_input.get(1.0, tk.END).strip()

            # Check if Enter key is pressed or if the user finished typing the phrase
            if event.keysym == "Return" or len(user_text) >= len(self.test_phrase):
                self.calculate_results()


    def show_results(self):
        """Displays results after the timed test."""
        message = (f"Timed Test Completed!\n"
                   f"Correct Phrases: {self.correct_count}\n"
                   f"Incorrect Phrases: {self.incorrect_count}")
        messagebox.showinfo("Test Results", message)

    def show_stats(self):
        """Shows statistics of previous tests."""
        avg_speed = (self.total_speed / self.total_tests) if self.total_tests > 0 else 0
        message = (f"Total Tests: {self.total_tests}\n"
                   f"Average Speed: {avg_speed:.2f} WPM\n"
                   f"Best Speed: {self.best_speed} WPM\n"
                   f"Highest Accuracy: {self.highest_accuracy:.2f}%")
        messagebox.showinfo("Typing Test Stats", message)

    def reset_test(self):
        """Resets the test for a fresh start."""
        self.total_tests = 0
        self.total_speed = 0
        self.best_speed = 0
        self.highest_accuracy = 0
        self.test_in_progress = False
        self.label_speed.config(text="Speed: 0 WPM")
        self.label_accuracy.config(text="Accuracy: 100%")
        self.label_test_phrase.config(text="Typing Speed Test")
        self.user_input.config(state=tk.NORMAL)
        self.user_input.delete(1.0, tk.END)
        self.label_timer.config(text="Time Left: 60s")  # Reset timer display
        self.enable_difficulty_buttons()  # Enable difficulty buttons
        self.start_button.config(state=tk.NORMAL)  # Enable Start Test button
        self.timed_test_button.config(state=tk.NORMAL)  # Enable Timed Test button

    def disable_difficulty_buttons(self):
        """Disables the difficulty selection buttons."""
        self.easy_radio.config(state=tk.DISABLED)
        self.medium_radio.config(state=tk.DISABLED)
        self.hard_radio.config(state=tk.DISABLED)

    def enable_difficulty_buttons(self):
        """Enables the difficulty selection buttons."""
        self.easy_radio.config(state=tk.NORMAL)
        self.medium_radio.config(state=tk.NORMAL)
        self.hard_radio.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingTestApp(root)
    
    app.user_input.tag_configure("correct", foreground="black")
    app.user_input.tag_configure("incorrect", foreground="red")
    app.user_input.tag_configure("remaining", foreground="gray")

    root.mainloop()