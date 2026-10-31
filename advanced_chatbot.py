"""
CODEALPHA INTERNSHIP - TASK 4
ADVANCED RULE-BASED CHATBOT / PERSONAL ASSISTANT

Author: Your Name
Version: 2.0.0

A feature-rich terminal chatbot demonstrating:
if/elif, functions, loops, dictionaries, lists, input/output,
string processing, random module, datetime, JSON file handling,
validation, and exception handling.

No third-party packages or internet connection are required.
"""

import json
import os
import random
import string
import ast
import operator
from datetime import datetime, date

APP_NAME = "CODEALPHA ADVANCED CHATBOT"
VERSION = "2.0.0"
DATA_FILE = "chatbot_data.json"
TRANSCRIPT_FILE = "chat_transcript.txt"

# ---------------------------------------------------------------------
# CONFIGURATION AND RESPONSE DATABASE
# ---------------------------------------------------------------------

RESPONSES = {
    "greeting": [
        "Hello! Great to see you. What can I do for you?",
        "Hi there! I'm ready to help.",
        "Hey! Welcome back.",
        "Hello! How is your day going?",
    ],
    "how_are_you": [
        "I'm doing great, thanks for asking!",
        "All systems are running smoothly. How are you?",
        "I'm fine! Ready to chat with you.",
    ],
    "feeling_good": [
        "That's fantastic! Keep that positive energy going.",
        "Glad to hear that!",
        "Wonderful! I hope your day gets even better.",
    ],
    "feeling_bad": [
        "I'm sorry you're having a difficult day. Take things one step at a time.",
        "I hope things improve soon. Would a joke or motivational quote help?",
        "Remember to take a break and be kind to yourself.",
    ],
    "thanks": [
        "You're very welcome!",
        "Happy to help!",
        "Anytime! That's what I'm here for.",
    ],
    "apology": [
        "No worries at all!",
        "It's okay. Let's continue.",
    ],
    "goodbye": [
        "Goodbye! Have a wonderful day.",
        "See you next time. Take care!",
        "Bye! It was great chatting with you.",
    ],
    "joke": [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the computer go to the doctor? It had a virus!",
        "Why was the JavaScript developer sad? Because he didn't Node how to Express himself!",
        "A SQL query walks into a bar, walks up to two tables and asks: Can I join you?",
        "Why did the programmer quit his job? He didn't get arrays!",
    ],
    "fact": [
        "A day on Venus is longer than its year.",
        "Octopuses have three hearts.",
        "Honey can remain edible for an extremely long time when stored properly.",
        "The first computer bug was an actual moth found in a computer relay.",
        "Python was named after Monty Python, not the snake.",
    ],
    "quote": [
        "Great things are done by a series of small things brought together. – Vincent van Gogh",
        "It always seems impossible until it's done. – Nelson Mandela",
        "Success is the sum of small efforts repeated day in and day out. – Robert Collier",
        "The secret of getting ahead is getting started. – Mark Twain",
        "Believe you can and you're halfway there. – Theodore Roosevelt",
    ],
    "creator": [
        "I was developed as an educational Python project for CodeAlpha Internship Task 4.",
        "I'm a rule-based chatbot created using Python programming concepts.",
    ],
    "identity": [
        "I'm CodeAlpha Advanced Bot, your offline Python personal assistant.",
        "You can call me CodeAlpha Bot!",
    ],
    "capabilities": [
        "I can chat, calculate, play games, manage notes and tasks, "
        "generate passwords, analyze text, and much more. Type 'help' to explore."
    ],
    "weather": [
        "I can't access live weather because I'm an offline chatbot. "
        "You can check a trusted weather app for current conditions."
    ],
    "study": [
        "Try the Pomodoro technique: focus for 25 minutes and take a 5-minute break.",
        "Study actively: solve questions, explain concepts aloud, and revise regularly.",
        "Break large topics into smaller tasks. Consistency matters!",
    ],
    "motivation": [
        "Every expert was once a beginner. Keep learning!",
        "Small progress every day adds up to big results.",
        "Don't compare your chapter one with someone else's chapter twenty.",
    ],
    "morning": [
        "Good morning! Wishing you a productive day.",
        "Rise and shine! Make today count.",
    ],
    "night": [
        "Good night! Rest well and recharge.",
        "Sleep well. Tomorrow is another opportunity.",
    ],
    "weekend": [
        "Enjoy your weekend! Make time for rest and fun.",
        "Hope you have a relaxing weekend!",
    ],
}

# Exact phrases are intentionally used to keep this a transparent,
# beginner-friendly rule-based chatbot.
INTENT_PATTERNS = {
    "greeting": ["hello", "hi", "hey", "hii", "howdy", "hello bot"],
    "how_are_you": ["how are you", "how are you doing", "are you fine", "how do you do"],
    "feeling_good": ["i am fine", "im fine", "i am good", "i am great", "doing good", "i feel happy"],
    "feeling_bad": ["i am sad", "i am not fine", "i feel bad", "i am tired", "bad day"],
    "thanks": ["thanks", "thank you", "thank u", "many thanks"],
    "apology": ["sorry", "i am sorry", "my mistake"],
    "goodbye": ["bye", "goodbye", "see you", "see you later", "exit", "quit"],
    "joke": ["tell me a joke", "joke", "make me laugh", "say something funny"],
    "fact": ["tell me a fact", "fact", "interesting fact", "random fact"],
    "quote": ["quote", "motivational quote", "inspire me", "give me a quote"],
    "creator": ["who created you", "who made you", "who is your creator"],
    "identity": ["what is your name", "who are you", "your name"],
    "capabilities": ["what can you do", "your features", "capabilities"],
    "weather": ["weather", "how is the weather", "is it raining"],
    "study": ["study tips", "help me study", "how to study", "exam tips"],
    "motivation": ["motivate me", "motivation", "i need motivation"],
    "morning": ["good morning"],
    "night": ["good night"],
    "weekend": ["happy weekend", "good weekend"],
}


def separator(char="=", width=74):
    print(char * width)


def title(text):
    print()
    separator()
    print(text.center(74))
    separator()


def normalize(text):
    """Lowercase text and remove common punctuation."""
    text = text.lower().strip()
    for char in "!?.,;:":
        text = text.replace(char, "")
    return " ".join(text.split())


def get_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")


def get_integer(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                print(f"Enter a number greater than or equal to {minimum}.")
                continue
            if maximum is not None and value > maximum:
                print(f"Enter a number less than or equal to {maximum}.")
                continue
            return value
        except ValueError:
            print("Please enter a valid whole number.")


def load_data():
    """Load persistent user settings, notes, tasks, and chat history."""
    default = {"name": "", "notes": [], "tasks": [], "history": []}
    if not os.path.exists(DATA_FILE):
        return default
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            saved = json.load(file)
        if not isinstance(saved, dict):
            return default
        for key in default:
            if key not in saved or not isinstance(saved[key], type(default[key])):
                saved[key] = default[key]
        return saved
    except (OSError, json.JSONDecodeError):
        print("Warning: Saved data could not be read. Starting with fresh data.")
        return default


def save_data(data, quiet=False):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        if not quiet:
            print(f"Data saved to {DATA_FILE}.")
    except OSError as error:
        print(f"Unable to save data: {error}")


def record(history, speaker, message):
    history.append({
        "speaker": speaker,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })


def show_welcome(data):
    title(APP_NAME)
    print(f"Version {VERSION} | Offline rule-based assistant")
    print("Bot: Hello! I'm CodeAlpha Advanced Bot.")
    if data["name"]:
        print(f"Bot: Welcome back, {data['name']}!")
    else:
        print("Bot: You can personalize me using the 'set name' command.")
    print("Bot: Type 'help' to view all features, or 'bye' to exit.")


def identify_intent(message):
    cleaned = normalize(message)
    for intent, patterns in INTENT_PATTERNS.items():
        if cleaned in [normalize(pattern) for pattern in patterns]:
            return intent
    if cleaned.startswith(("hello ", "hi ", "hey ")):
        return "greeting"
    if cleaned.startswith("how are you"):
        return "how_are_you"
    return None


# ---------------------------------------------------------------------
# SAFE CALCULATOR
# ---------------------------------------------------------------------

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_expression(expression):
    """Safely evaluate arithmetic expressions without eval()."""
    def evaluate(node):
        if isinstance(node, ast.Constant) and type(node.value) in (int, float):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
            left = evaluate(node.left)
            right = evaluate(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Exponent is too large.")
            return _ALLOWED_OPERATORS[type(node.op)](left, right)
        if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
            return _ALLOWED_OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("Only basic arithmetic is allowed.")

    parsed = ast.parse(expression, mode="eval")
    result = evaluate(parsed.body)
    if isinstance(result, complex):
        raise ValueError("Complex results are not supported.")
    return result


def calculator():
    title("SMART CALCULATOR")
    print("Supports +  -  *  /  //  %  ** and parentheses.")
    print("Example: (25 + 5) * 2 / 3")
    expression = get_non_empty("Enter calculation: ")
    try:
        result = evaluate_expression(expression)
        print(f"Result: {result}")
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as error:
        print(f"Could not calculate: {error}")


# ---------------------------------------------------------------------
# PERSONALIZATION AND DATE/TIME
# ---------------------------------------------------------------------

def set_name(data):
    title("PERSONALIZE CHATBOT")
    data["name"] = get_non_empty("What should I call you? ")
    save_data(data)
    print(f"Nice to meet you, {data['name']}!")


def show_date_time():
    now = datetime.now()
    title("DATE AND TIME")
    print("Date       :", now.strftime("%A, %d %B %Y"))
    print("Time       :", now.strftime("%I:%M:%S %p"))
    print("Day        :", now.strftime("%A"))
    print("Month      :", now.strftime("%B"))
    print("Year       :", now.year)
    print("Week number:", now.isocalendar().week)


def days_between():
    title("DATE DIFFERENCE CALCULATOR")
    print("Enter dates in YYYY-MM-DD format.")
    try:
        first = date.fromisoformat(get_non_empty("First date: "))
        second = date.fromisoformat(get_non_empty("Second date: "))
        print("Difference:", abs((second - first).days), "days")
    except ValueError:
        print("Invalid date. Example format: 2026-10-31.")


# ---------------------------------------------------------------------
# NOTES AND TO-DO MANAGER
# ---------------------------------------------------------------------

def notes_menu(data):
    while True:
        title("PERSONAL NOTES MANAGER")
        print("1. Add note")
        print("2. View notes")
        print("3. Delete note")
        print("0. Back to main menu")
        choice = input("Choose: ").strip()

        if choice == "1":
            note = get_non_empty("Enter your note: ")
            data["notes"].append({
                "text": note,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
            save_data(data, quiet=True)
            print("Note saved.")
        elif choice == "2":
            if not data["notes"]:
                print("No notes saved yet.")
            else:
                for index, item in enumerate(data["notes"], 1):
                    print(f"{index}. {item['text']} [{item.get('created', '')}]")
        elif choice == "3":
            if not data["notes"]:
                print("No notes to delete.")
            else:
                for index, item in enumerate(data["notes"], 1):
                    print(f"{index}. {item['text']}")
                number = get_integer("Note number to delete: ", 1, len(data["notes"]))
                deleted = data["notes"].pop(number - 1)
                save_data(data, quiet=True)
                print("Deleted:", deleted["text"])
        elif choice == "0":
            break
        else:
            print("Invalid option.")


def todo_menu(data):
    while True:
        title("TO-DO LIST MANAGER")
        print("1. Add task")
        print("2. View tasks")
        print("3. Mark task completed")
        print("4. Delete task")
        print("0. Back to main menu")
        choice = input("Choose: ").strip()

        if choice == "1":
            task = get_non_empty("Enter task: ")
            data["tasks"].append({"task": task, "completed": False})
            save_data(data, quiet=True)
            print("Task added.")
        elif choice == "2":
            if not data["tasks"]:
                print("Your task list is empty.")
            else:
                for index, item in enumerate(data["tasks"], 1):
                    status = "DONE" if item["completed"] else "PENDING"
                    print(f"{index}. [{status}] {item['task']}")
        elif choice == "3":
            pending = [i for i, task in enumerate(data["tasks"]) if not task["completed"]]
            if not pending:
                print("No pending tasks.")
            else:
                for index, item in enumerate(data["tasks"], 1):
                    print(f"{index}. [{'DONE' if item['completed'] else 'PENDING'}] {item['task']}")
                number = get_integer("Task number completed: ", 1, len(data["tasks"]))
                data["tasks"][number - 1]["completed"] = True
                save_data(data, quiet=True)
                print("Task marked as completed.")
        elif choice == "4":
            if not data["tasks"]:
                print("No tasks to delete.")
            else:
                for index, item in enumerate(data["tasks"], 1):
                    print(f"{index}. {item['task']}")
                number = get_integer("Task number to delete: ", 1, len(data["tasks"]))
                removed = data["tasks"].pop(number - 1)
                save_data(data, quiet=True)
                print("Deleted:", removed["task"])
        elif choice == "0":
            break
        else:
            print("Invalid option.")


# ---------------------------------------------------------------------
# TEXT UTILITIES
# ---------------------------------------------------------------------

def text_toolkit():
    while True:
        title("TEXT TOOLKIT")
        print("1. Word and character counter")
        print("2. Reverse text")
        print("3. Palindrome checker")
        print("4. Uppercase / lowercase converter")
        print("5. Count vowels and consonants")
        print("0. Back")
        choice = input("Choose: ").strip()

        if choice == "0":
            break
        if choice not in ("1", "2", "3", "4", "5"):
            print("Invalid option.")
            continue

        text = get_non_empty("Enter text: ")
        if choice == "1":
            print("Characters (including spaces):", len(text))
            print("Characters (excluding spaces):", len(text.replace(" ", "")))
            print("Words:", len(text.split()))
            print("Lines:", len(text.splitlines()))
        elif choice == "2":
            print("Reversed:", text[::-1])
        elif choice == "3":
            cleaned = "".join(char.lower() for char in text if char.isalnum())
            print("It is a palindrome." if cleaned == cleaned[::-1] else "It is not a palindrome.")
        elif choice == "4":
            print("Uppercase:", text.upper())
            print("Lowercase:", text.lower())
            print("Title case:", text.title())
        elif choice == "5":
            vowels = sum(char.lower() in "aeiou" for char in text if char.isalpha())
            consonants = sum(char.isalpha() and char.lower() not in "aeiou" for char in text)
            print("Vowels:", vowels)
            print("Consonants:", consonants)
            print("Digits:", sum(char.isdigit() for char in text))


def password_generator():
    title("PASSWORD GENERATOR")
    length = get_integer("Password length (8-64): ", 8, 64)
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    password = "".join(random.SystemRandom().choice(chars) for _ in range(length))
    print("Generated password:", password)
    print("Store it safely. Do not share passwords with others.")


# ---------------------------------------------------------------------
# MINI GAMES
# ---------------------------------------------------------------------

def number_guessing_game():
    title("NUMBER GUESSING GAME")
    secret = random.randint(1, 100)
    attempts = 0
    print("I have selected a number between 1 and 100.")
    while True:
        guess = get_integer("Your guess (0 to quit): ", 0, 100)
        if guess == 0:
            print("Game ended. The number was", secret)
            break
        attempts += 1
        if guess < secret:
            print("Too low! Try a higher number.")
        elif guess > secret:
            print("Too high! Try a lower number.")
        else:
            print(f"Correct! You found it in {attempts} attempt(s).")
            break


def rock_paper_scissors():
    title("ROCK PAPER SCISSORS")
    options = ["rock", "paper", "scissors"]
    user_score = 0
    bot_score = 0
    print("First to 3 points wins. Type 'quit' to stop.")
    while user_score < 3 and bot_score < 3:
        user = normalize(input("\nChoose rock, paper, or scissors: "))
        if user == "quit":
            break
        if user not in options:
            print("Invalid choice.")
            continue
        bot = random.choice(options)
        print("Bot chose:", bot)
        if user == bot:
            print("It's a tie!")
        elif (user, bot) in [
            ("rock", "scissors"), ("paper", "rock"), ("scissors", "paper")
        ]:
            user_score += 1
            print("You win this round!")
        else:
            bot_score += 1
            print("Bot wins this round!")
        print(f"Score - You: {user_score} | Bot: {bot_score}")
    if user_score == 3:
        print("Congratulations! You won the game.")
    elif bot_score == 3:
        print("The chatbot won this time. Try again!")
    else:
        print("Game stopped.")


# ---------------------------------------------------------------------
# CHAT HISTORY AND EXPORT
# ---------------------------------------------------------------------

def show_history(data):
    title("CONVERSATION HISTORY")
    if not data["history"]:
        print("No conversation history available.")
        return
    for item in data["history"][-50:]:
        print(f"[{item.get('timestamp', '')}] {item['speaker']}: {item['message']}")
    print("\nShowing the latest 50 messages at most.")


def export_transcript(data):
    title("EXPORT CHAT TRANSCRIPT")
    try:
        with open(TRANSCRIPT_FILE, "w", encoding="utf-8") as file:
            file.write(APP_NAME + "\n")
            file.write("=" * 74 + "\n")
            file.write(f"Exported: {datetime.now().isoformat(timespec='seconds')}\n\n")
            for item in data["history"]:
                file.write(
                    f"[{item.get('timestamp', '')}] "
                    f"{item['speaker']}: {item['message']}\n"
                )
        print(f"Transcript exported to {TRANSCRIPT_FILE}.")
    except OSError as error:
        print("Export failed:", error)


# ---------------------------------------------------------------------
# HELP AND COMMAND ROUTER
# ---------------------------------------------------------------------

def show_help():
    title("CHATBOT HELP AND FEATURE DIRECTORY")
    sections = {
        "CONVERSATION": [
            "hello / hi", "how are you", "i am fine", "i am sad",
            "what is your name", "who created you", "thanks", "bye"
        ],
        "FUN AND LEARNING": [
            "joke", "fact", "quote", "motivate me", "study tips"
        ],
        "INFORMATION": [
            "date", "time", "date difference"
        ],
        "TOOLS": [
            "calculator", "password", "text tools", "notes", "todo"
        ],
        "GAMES": [
            "guess game", "rock paper scissors"
        ],
        "CHAT MANAGEMENT": [
            "history", "export", "save", "clear history"
        ],
        "PERSONALIZATION": [
            "set name"
        ],
    }
    for heading_text, commands in sections.items():
        print(f"\n{heading_text}")
        print("  " + " | ".join(commands))
    print("\nYou can also use the numbered main menu.")


def main_menu():
    title("MAIN MENU")
    print("CONVERSATION")
    print("  1. Start chatting (type messages)")
    print("  2. View help and all features")
    print("  3. Set / change your name")
    print("\nPRODUCTIVITY")
    print("  4. Notes manager")
    print("  5. To-do list manager")
    print("  6. Date and time")
    print("  7. Date difference calculator")
    print("\nPYTHON TOOLS")
    print("  8. Calculator")
    print("  9. Text toolkit")
    print(" 10. Password generator")
    print("\nENTERTAINMENT")
    print(" 11. Number guessing game")
    print(" 12. Rock-paper-scissors")
    print(" 13. Random joke")
    print(" 14. Random fact")
    print(" 15. Motivational quote")
    print("\nCHAT DATA")
    print(" 16. View conversation history")
    print(" 17. Export chat transcript")
    print(" 18. Save all data")
    print(" 19. Clear conversation history")
    print("  0. Exit")
    separator("-")


def chat_loop(data):
    title("CHAT SESSION")
    print("Type 'back' to return to the main menu.")
    while True:
        try:
            message = input("\nYou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBot: Returning to main menu.")
            break

        if not message:
            print("Bot: Please enter a message.")
            continue

        cleaned = normalize(message)
        if cleaned == "back":
            break

        if cleaned == "date":
            reply = f"Today is {datetime.now().strftime('%A, %d %B %Y')}."
        elif cleaned == "time":
            reply = f"The time is {datetime.now().strftime('%I:%M:%S %p')}."
        elif cleaned in ("help", "commands"):
            show_help()
            reply = "I displayed the feature directory."
        elif cleaned in ("joke", "tell me a joke", "make me laugh"):
            reply = random.choice(RESPONSES["joke"])
        else:
            intent = identify_intent(message)
            if intent:
                reply = random.choice(RESPONSES[intent])
            else:
                reply = (
                    "I don't know how to respond to that yet. "
                    "Try 'help', or use one of the available commands."
                )

        print("Bot:", reply)
        record(data["history"], "You", message)
        record(data["history"], "Bot", reply)

        if identify_intent(message) == "goodbye":
            save_data(data, quiet=True)
            print("Bot: Chat session ended. Returning to the main menu.")
            break


def clear_history(data):
    title("CLEAR CHAT HISTORY")
    confirm = input("Type CLEAR to delete conversation history: ").strip()
    if confirm == "CLEAR":
        data["history"].clear()
        save_data(data, quiet=True)
        print("Conversation history cleared.")
    else:
        print("Cancelled. No history was deleted.")


def run():
    data = load_data()
    show_welcome(data)

    while True:
        main_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            chat_loop(data)
        elif choice == "2":
            show_help()
        elif choice == "3":
            set_name(data)
        elif choice == "4":
            notes_menu(data)
        elif choice == "5":
            todo_menu(data)
        elif choice == "6":
            show_date_time()
        elif choice == "7":
            days_between()
        elif choice == "8":
            calculator()
        elif choice == "9":
            text_toolkit()
        elif choice == "10":
            password_generator()
        elif choice == "11":
            number_guessing_game()
        elif choice == "12":
            rock_paper_scissors()
        elif choice == "13":
            print("\nBot:", random.choice(RESPONSES["joke"]))
        elif choice == "14":
            print("\nBot:", random.choice(RESPONSES["fact"]))
        elif choice == "15":
            print("\nBot:", random.choice(RESPONSES["quote"]))
        elif choice == "16":
            show_history(data)
        elif choice == "17":
            export_transcript(data)
        elif choice == "18":
            save_data(data)
        elif choice == "19":
            clear_history(data)
        elif choice == "0":
            save_data(data, quiet=True)
            print("\nBot: Your data has been saved. Goodbye!")
            break
        else:
            print("Invalid choice. Enter a number from 0 to 19.")

        input("\nPress Enter to return to the main menu...")


if __name__ == "__main__":
    run()
