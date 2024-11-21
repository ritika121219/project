import json

# File paths
QUIZ_FILE = "quiz_data.json"
LEADERBOARD_FILE = "leaderboard.json"

# Function to load quiz data
def load_quiz_data():
    try:
        with open(QUIZ_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save quiz data
def save_quiz_data(quiz_data):
    with open(QUIZ_FILE, "w") as file:
        json.dump(quiz_data, file, indent=4)

# Function to load leaderboard data
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Function to save leaderboard data
def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file, indent=4)

# Function to add a question
def add_question(quiz_data):
    category = input("Enter the category (e.g., Math, Science): ").capitalize()
    difficulty = input("Enter the difficulty level (Easy, Medium, Hard): ").capitalize()
    question = input("Enter the question: ")
    options = [input(f"Enter option {i + 1}: ") for i in range(4)]
    correct_option = int(input("Enter the correct option number (1-4): ")) - 1

    if correct_option < 0 or correct_option >= 4:
        print("Invalid correct option. Question not added.")
        return

    if category not in quiz_data:
        quiz_data[category] = []
    quiz_data[category].append({
        "question": question,
        "options": options,
        "correct": correct_option,
        "difficulty": difficulty
    })
    print("Question added successfully!")

# Function to take a quiz
def take_quiz(quiz_data):
    category = input("Choose a category: " + ", ".join(quiz_data.keys()) + ": ").capitalize()
    if category not in quiz_data:
        print("Invalid category!")
        return

    difficulty = input("Choose a difficulty level (Easy, Medium, Hard): ").capitalize()
    questions = [q for q in quiz_data[category] if q["difficulty"] == difficulty]

    if not questions:
        print(f"No {difficulty} questions available in the {category} category!")
        return

    score = 0
    for q in questions:
        print("\n" + q["question"])
        for i, option in enumerate(q["options"]):
            print(f"{i + 1}. {option}")
        answer = int(input("Enter your answer (1-4): ")) - 1
        if answer == q["correct"]:
            print("Correct!")
            score += 1
        else:
            print(f"Wrong! Correct answer: {q['options'][q['correct']]}")

    print(f"\nYou scored {score}/{len(questions)}")

    # Update leaderboard
    name = input("Enter your name for the leaderboard: ")
    update_leaderboard(name, score)

# Function to update the leaderboard
def update_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]  # Top 10 scores
    save_leaderboard(leaderboard)
    print("\nLeaderboard:")
    for idx, entry in enumerate(leaderboard, start=1):
        print(f"{idx}. {entry['name']} - {entry['score']}")

# Main menu
def main():
    quiz_data = load_quiz_data()

    while True:
        print("\nQuiz App")
        print("1. Add Question")
        print("2. Take Quiz")
        print("3. View Leaderboard")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_question(quiz_data)
            save_quiz_data(quiz_data)
        elif choice == "2":
            take_quiz(quiz_data)
        elif choice == "3":
            leaderboard = load_leaderboard()
            print("\nLeaderboard:")
            for idx, entry in enumerate(leaderboard, start=1):
                print(f"{idx}. {entry['name']} - {entry['score']}")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
1