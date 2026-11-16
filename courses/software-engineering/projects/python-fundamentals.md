# A terminal game: text adventure or quiz

Build a small game that runs in the terminal: either a **text adventure** (move between rooms, pick things up, reach a goal) or a **quiz game** (questions by topic, a score, maybe a high-score table). Pick whichever you'd enjoy more; the rules are the same.

The point isn't the game. It's practising everything from this section in one program that a real person uses: functions with one job each, loops, conditionals, lists and dicts, and input handling that never crashes. You'll also learn what happens when someone who isn't you plays it.

Plan on a week of evenings.

## Rules

- **No classes yet.** Use functions, lists and dicts only. (Classes come in the object-oriented section, and this project will make you appreciate them.)
- **Standard library only.**
- **Data separate from logic.** The rooms or questions live in a dict (or a list of dicts) at the top of the file or in their own module. The functions read that data; they don't hard-code it. Adding a room or a question should mean editing data, not code.
- **Never crash on bad input.** Typing nothing, a number out of range, `QUIT` in capitals or random text must produce a helpful message and a second chance, not a traceback.
- **Small functions.** At least 8 functions, each under 20 lines, each doing one thing.

## Suggested shape

For a quiz:

```python
QUESTIONS = {
    "python": [
        {"question": "What does len([1, 2, 3]) return?", "options": ["2", "3", "4"], "answer": 1},
        ...
    ],
    "terminal": [...],
}
```

For an adventure:

```python
ROOMS = {
    "hall": {"description": "A dusty hall.", "exits": {"north": "library"}, "items": ["lamp"]},
    "library": {"description": "Shelves of books.", "exits": {"south": "hall"}, "items": []},
}
```

Functions you'll probably want (rename them to fit your game):

```
show_menu()                    print the choices
ask_choice(prompt, valid)      keep asking until the input is one of valid; return it
pick_topic(questions)          let the player choose a topic
ask_question(q)                show one question, return True if answered correctly
run_quiz(questions)            loop over questions, return the score
describe_room(room)            return the text for a room
move(current, direction)       return the new room name, or the same one if there's no exit
show_result(score, total)      print the final score
main()                         the game loop
```

Keep `input()` and `print()` in a few functions at the edges (like `ask_choice` and `main`) and make the rest **return** values. That way you can test them, and you will in the testing section.

## Steps

1. Write the data structure first, with 3 rooms or 5 questions.
2. Write `ask_choice` and try to break it: empty input, spaces, capitals, numbers out of range.
3. Build the game loop with `while`, and a way to quit.
4. Add the score or state display at the end.
5. Grow the data to at least 6 rooms or 15 questions, without changing any function.
6. Ask a friend or family member to play it **without your help**. Watch, don't explain. Write down the first thing that confused them, fix it, and describe the fix in a comment at the top of the file.

## Stretch goals

- Save high scores (or the player's progress) to a JSON file with the `json` module.
- Shuffle the questions with `random.shuffle`, passing the random generator in as a parameter so you could test it.
- Write two or three `test_*.py` functions for the pure functions (`move`, `ask_question`'s checking logic) and run them with pytest.
