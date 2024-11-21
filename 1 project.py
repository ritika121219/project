import time
import random

# Quiz data stored in memory
quiz_data = [
    {
        "question": "What is the capital of France?",
        "options": ["A. Paris", "B. London", "C. Rome", "D. Berlin"],
        "answer": "A"
    },
    {
        "question": "Which programming language is known as the language of the web?",
        "options": ["A. Python", "B. JavaScript", "C. C++", "D. Java"],
        "answer": "B"
    },
    {
        "question": "What is 2 + 2?",
        "options": ["A. 3", "B. 4", "C. 5", "D. 6"],
        "answer": "B"
    },
    {
        "question": "What planet is known as the Red Planet?",
        "options": ["A. Mars", "B. Venus", "C. Earth", "D. Jupiter"],
        "answer": "A"
    },
]


# Progress Bar Function
def progress_bar(current, total):
    bar_length = 20  # Length of the progress bar
    progress = int(bar_length * (current / total))
    print(f"\nProgress: [{'#' * progress}{'.' * (bar_length - progress)}] {current}/{total}")


# Timer for Each Question
def timed_input(prompt, timeout):
    start_time = time.time()
    print(prompt)
    try:
        answer = input("Your answer (A/B/C/D): ").strip().upper()
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout:
            print("Time's up!")
            return None  # Timeout case
        return answer
    except Exception:
        return None


# Dynamic Feedback
def give_feedback(user_answer, correct_answer):
    if user_answer == correct_answer:
        return "Great job! That's correct! 🎉"
    elif user_answer is None:
        return "You ran out of time! 😟"
    else:
        return f"Oops! The correct answer was {correct_answer}. Better luck next time! 😊"


# Quiz Function
def run_quiz():
    random.shuffle(quiz_data)  # Randomize question order
    score = 0
    print("Welcome to the Enhanced Quiz App!\n")
    total_questions = len(quiz_data)

    for i, item in enumerate(quiz_data):
        print(f"\nQuestion {i + 1}: {item['question']}")
        for option in item['options']:
            print(option)

        # Display progress bar
        progress_bar(i + 1, total_questions)

        # Timer for answering
        user_answer = timed_input("\nYou have 10 seconds to answer!", 10)

        # Check answer and give feedback
        feedback = give_feedback(user_answer, item['answer'])
        print(feedback)

        if user_answer == item['answer']:
            score += 1

    print(f"\nQuiz Over! Your score: {score}/{total_questions}")


# Run the enhanced quiz
run_quiz()
