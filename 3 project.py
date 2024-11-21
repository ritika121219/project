import sqlite3

# 1. Set up the database
def setup_database():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()

    # Create table for questions (with a new column for difficulty)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        option1 TEXT NOT NULL,
        option2 TEXT NOT NULL,
        option3 TEXT NOT NULL,
        option4 TEXT NOT NULL,
        correct_option INTEGER NOT NULL,
        category TEXT NOT NULL,
        difficulty TEXT NOT NULL
    )
    ''')

    # Create table for user scores (allowing multiple attempts)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        score INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()

# 2. Add questions to the database (Admin only)
def add_question():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()

    question = input("Enter the question: ")
    option1 = input("Enter option 1: ")
    option2 = input("Enter option 2: ")
    option3 = input("Enter option 3: ")
    option4 = input("Enter option 4: ")
    correct_option = int(input("Enter the correct option (1-4): "))
    category = input("Enter category: ")
    difficulty = input("Enter difficulty (Easy, Medium, Hard): ")

    cursor.execute('''
    INSERT INTO questions (question, option1, option2, option3, option4, correct_option, category, difficulty)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (question, option1, option2, option3, option4, correct_option, category, difficulty))

    conn.commit()
    conn.close()

# 3. Edit a question (Admin only)
def edit_question():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()

    question_id = int(input("Enter the question ID to edit: "))
    cursor.execute("SELECT * FROM questions WHERE id = ?", (question_id,))
    question_data = cursor.fetchone()

    if question_data:
        print(f"Current question: {question_data[1]}")
        question = input("Enter new question or press Enter to keep it the same: ")
        option1 = input("Enter new option 1 or press Enter to keep it the same: ")
        option2 = input("Enter new option 2 or press Enter to keep it the same: ")
        option3 = input("Enter new option 3 or press Enter to keep it the same: ")
        option4 = input("Enter new option 4 or press Enter to keep it the same: ")
        correct_option = input("Enter new correct option (1-4) or press Enter to keep it the same: ")
        category = input("Enter new category or press Enter to keep it the same: ")
        difficulty = input("Enter new difficulty or press Enter to keep it the same: ")

        # Update only fields that were entered
        cursor.execute('''
        UPDATE questions
        SET question = COALESCE(?, question),
            option1 = COALESCE(?, option1),
            option2 = COALESCE(?, option2),
            option3 = COALESCE(?, option3),
            option4 = COALESCE(?, option4),
            correct_option = COALESCE(?, correct_option),
            category = COALESCE(?, category),
            difficulty = COALESCE(?, difficulty)
        WHERE id = ?
        ''', (question, option1, option2, option3, option4, correct_option if correct_option else question_data[6], category, difficulty, question_id))

        conn.commit()
        print("Question updated successfully.")
    else:
        print("Question not found.")

    conn.close()

# 4. Delete a question (Admin only)
def delete_question():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()

    question_id = int(input("Enter the question ID to delete: "))
    cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
    conn.commit()
    print("Question deleted successfully.")
    conn.close()

# 5. Conduct quiz and track multiple attempts
def conduct_quiz(username):
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 5")  # Get 5 random questions
    questions = cursor.fetchall()

    score = 0
    incorrect_answers = []

    for q in questions:
        print(f"\n{q[1]}")
        print(f"1. {q[2]}")
        print(f"2. {q[3]}")
        print(f"3. {q[4]}")
        print(f"4. {q[5]}")

        answer = int(input("Enter your answer (1-4): "))
        if answer == q[6]:
            print("Correct!")
            score += 1
        else:
            print("Wrong!")
            incorrect_answers.append((q[1], q[6]))  # Store the incorrect answers

    # Save the score for multiple attempts
    cursor.execute("INSERT INTO scores (username, score) VALUES (?, ?)", (username, score))
    conn.commit()

    print(f"\n{username}, your final score is: {score}/{len(questions)}")

    # Show quiz review (incorrect answers)
    print("\nQuiz Review:")
    for question, correct in incorrect_answers:
        print(f"Question: {question}, Correct Answer: {correct}")

    conn.close()

# 6. View leaderboard and multiple attempts
def view_scores():
    conn = sqlite3.connect("quiz_app.db")
    cursor = conn.cursor()

    cursor.execute("SELECT username, MAX(score) AS highest_score FROM scores GROUP BY username")
    scores = cursor.fetchall()

    print("\nLeaderboard:")
    for s in scores:
        print(f"{s[0]} - {s[1]} points")

    conn.close()

# Admin Panel
def admin_panel():
    print("\nAdmin Panel:")
    print("1. Add Question")
    print("2. Edit Question")
    print("3. Delete Question")
    choice = input("Enter your choice: ")

    if choice == "1":
        add_question()
    elif choice == "2":
        edit_question()
    elif choice == "3":
        delete_question()
    else:
        print("Invalid choice.")

# Main Program
if __name__ == "__main__":
    setup_database()

    while True:
        print("\nWelcome to the Quiz App!")
        print("1. Admin Panel")
        print("2. Take Quiz")
        print("3. View Scores")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            admin_panel()
        elif choice == "2":
            username = input("Enter your name: ")
            conduct_quiz(username)
        elif choice == "3":
            view_scores()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
