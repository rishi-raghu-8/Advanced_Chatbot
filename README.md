# CodeAlpha Internship – Task 4: Advanced Rule-Based Chatbot

A feature-rich, offline Python chatbot and personal assistant built using Python fundamentals. It expands the basic chatbot task with conversational intents, productivity tools, text utilities, mini-games, and persistent local data.

## Features

### Rule-based conversation
- Multiple greeting, farewell, gratitude, apology, and mood responses.
- Predefined responses for identity, creator, study tips, motivation, weather limitations, and capabilities.
- Random response variations.
- Case-insensitive phrase matching and basic punctuation normalization.
- Help and feature directory.

### Personal assistant
- Personalize the bot with your name.
- Current date, time, weekday, month, year, and week number.
- Calculate the number of days between two dates.

### Productivity
- Notes manager: add, view, and delete notes.
- To-do manager: add, view, complete, and delete tasks.
- Data persists locally in JSON.

### Python tools
- Arithmetic calculator with safe expression parsing (does not use `eval`).
- Text word/character/line counter.
- Reverse text.
- Palindrome checker.
- Uppercase/lowercase/title-case converter.
- Vowel, consonant, and digit counter.
- Random password generator.

### Entertainment
- Random jokes, facts, and motivational quotes.
- Number guessing game.
- Rock-paper-scissors game with score tracking.

### Chat management
- Conversation history.
- Save user data in JSON.
- Export conversation transcript to TXT.
- Clear conversation history with confirmation.

## Requirements

- Python 3.8 or newer
- No external packages
- No internet connection or API key

## Run

Extract the ZIP, open a terminal inside the project folder, and run:

```bash
python advanced_chatbot.py
```

Windows alternative:

```powershell
py advanced_chatbot.py
```

## Project structure

```text
CodeAlpha_Advanced_Chatbot/
│
├── advanced_chatbot.py
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Main menu

```text
1. Start chatting
2. View help and all features
3. Set / change your name
4. Notes manager
5. To-do list manager
6. Date and time
7. Date difference calculator
8. Calculator
9. Text toolkit
10. Password generator
11. Number guessing game
12. Rock-paper-scissors
13. Random joke
14. Random fact
15. Motivational quote
16. View conversation history
17. Export chat transcript
18. Save all data
19. Clear conversation history
0. Exit
```

## Example conversation

```text
You: hello
Bot: Hi there! I'm ready to help.

You: how are you
Bot: I'm doing great, thanks for asking!

You: tell me a joke
Bot: Why do programmers prefer dark mode? Because light attracts bugs!

You: bye
Bot: See you next time. Take care!
```

## Data files

The application creates these files when used:

| File | Purpose |
|---|---|
| `chatbot_data.json` | User name, notes, tasks, and conversation history |
| `chat_transcript.txt` | Exported readable conversation transcript |

These generated files are excluded from Git using `.gitignore` so personal notes and chat history are not accidentally uploaded.

## Concepts demonstrated

- Variables, strings, lists, tuples, and dictionaries
- Conditional statements (`if`, `elif`, `else`)
- Loops (`while`, `for`)
- Functions and modular program design
- Input and output
- String methods and text processing
- Random module
- Date and time handling
- JSON file handling
- Exception handling and input validation
- Abstract Syntax Trees for safe calculator expression parsing

