# Learning like an engineer

## Why this matters

Two people can spend the same 300 hours on this course and come out at very different levels. The difference is rarely talent. It's *how* they practise: whether they guess before they run, whether they read the error before asking for help, and whether they let an AI tool do the thinking that was supposed to build their skill. Engineering is a job of learning unfamiliar things quickly, every week, for your whole career. This lesson is about the habits that make that work, starting now.

## How this course works

Each lesson has the same parts:

- **The lesson page** teaches the topic fully. Read it with the practice editor open and try the small examples as you go.
- **Videos** are companions: a second explanation from a different teacher. Watch them when something hasn't clicked, or for a broader view.
- **Practice** has code exercises and quizzes. Each code exercise gives you a task, starter code, a **Run** button to try your code, and a **Check** button that runs hidden tests. Wrong quiz answers go into a review queue so you meet them again later.
- **Projects**, one per section, are where you build something real in your own folders and later your own GitHub repository. They become your portfolio.

The exercises are small on purpose. Doing many small things correctly, by yourself, is what builds skill.

## Deliberate practice

Practice only improves you when it's slightly too hard. Copying a solution you've just watched feels productive but builds almost nothing. **Deliberate practice** means working at the edge of what you can do, getting fast feedback, and fixing specific mistakes:

- Attempt the exercise before looking at any hint.
- When you're stuck for a while (say 20–30 minutes of real effort), take the smallest hint that unsticks you, not the whole answer.
- After you pass, compare your code with the reference solution. Note one thing it does better and why.
- A few days later, redo an exercise you found hard, from a blank file. If you can't, you hadn't learned it yet; that's useful to know.

## Predict, then run

Before you press Run or Check, say (or write in a comment) what you expect to happen:

```python
items = [3, 1, 2]
result = items.sort()
print(result)
# My prediction: [1, 2, 3]
# Actual:        None   ← .sort() changes the list and returns None
```

When the prediction is right, you've confirmed your model of how Python works. When it's wrong, you've found a gap in that model, which is the most valuable thing that can happen while learning. If you never predict, you never notice the gaps; you just keep changing things until the tests pass.

This matters even more with a Check button available. Ryan Peterman, a former Instagram engineer, describes failing every onsite interview while he relied on running tests to reverse-engineer answers, and passing most once he made himself think the solution through first. In an interview, and in a lot of real work, there is no button. Treat Check as confirmation of something you already believe, not as a way to find out what to type.

## Read the error before anything else

Errors are the computer telling you exactly what went wrong. Beginners tend to see a wall of red and look away. Instead, read it **from the bottom up**:

```
Traceback (most recent call last):
  File "/home/ada/app/main.py", line 7, in <module>
    total = add_tax(price)
  File "/home/ada/app/main.py", line 3, in add_tax
    return price * 1.2
           ~~~~~~^~~~~
TypeError: can't multiply sequence by non-int of type 'float'
```

1. **The last line** says what kind of error (`TypeError`) and what happened: something was a *sequence* (here, a string) when a number was expected.
2. **The lines above** are the path the program took, outermost call first, down to the line that failed (`line 3, in add_tax`). The `~~~^~~~` marks the exact spot.
3. Ask: what was the value of `price`? Probably text, such as `"9.99"` read from input and never converted to a number.

You'll learn debugging properly later in the course. For now, the habit: read the last line, find your own file's line number, and look at the values on that line before you ask anyone, human or AI.

## Docs before tutorials

When you need to know what a function does, the official documentation is usually the fastest answer, and it's always correct for your version. Python's docs (docs.python.org) have a tutorial and a reference for every built-in and standard-library module. Tutorials and videos are great for the big picture, but they go out of date and they show one person's way. In the REPL, `help(str.split)` shows the documentation without leaving the terminal.

## Asking a good question

At some point you'll be truly stuck, and asking is the right move. How you ask decides whether you get an answer in five minutes or none. A good question has:

1. **What you're trying to do**, in one sentence.
2. **A minimal example**: the smallest piece of code that still shows the problem, which someone else can run. Making it small often reveals the bug before you even post.
3. **What you expected** and **what happened instead**, with the full error message copied as text (not a screenshot).
4. **What you've tried** already.

Compare:

> my code doesnt work pls help

with:

> I'm trying to sum the numbers a user types in. With input `3` and `4` I expect `7`, but I get `34`. Here's the 4-line version that shows it: (code). I checked that the loop runs twice. I think the inputs might be text?

The second one almost answers itself (it's `input()` returning strings, which you'll meet in "Values, variables and types"). Simon Tatham's essay on reporting bugs, linked below, is the classic guide to this.

## AI as a tutor, not a ghostwriter

AI coding assistants are normal at work now. In the 2025 Stack Overflow developer survey, 84% of respondents used them or planned to. The same survey found more developers distrust the accuracy of what they produce (46%) than trust it (33%). You will use these tools in your job. The question is how to use them while you're learning without losing the learning.

In January 2026 Anthropic published a randomised controlled trial (linked below) that looked at exactly this. Junior engineers learned a new Python library, some with an AI assistant and some coding by hand, then took a quiz on it.

- The group using AI scored about **50%**; the hand-coding group scored about **67%**.
- The biggest gap was on **debugging** questions: the skill you need most when AI-written code breaks.
- *How* people used the AI mattered more than *whether* they used it. People who asked it conceptual questions, or asked for explanations alongside code, kept their learning (65% and above). People who delegated writing the code or fixing the bugs to it scored **under 40%**.

So the rule in this course is simple:

- **Attempt first.** Write your own solution before asking for anything.
- **Ask AI to explain, not to write.** "Why does `.sort()` return `None`?" or "What does this error mean?" builds skill. "Write a function that…" skips it.
- **Never keep code you can't explain.** If an AI suggests something, you should be able to explain every line to someone else. If you can't, ask it to explain, or write it yourself.
- **Debug it yourself first.** Read the error, form a guess, test it. Ask for a hint only after that.

Once a skill is solid (you can do it unaided, quickly), using AI to go faster is just good engineering, and the course covers that in its final section.

### Is it still worth learning to code?

Yes. Simon Willison, co-creator of the Django web framework and one of the most careful public writers on AI coding, puts it plainly: learning to code is the best way to take advantage of AI-driven development. Addy Osmani, who has spent over a decade on Chrome at Google, warns that skipping the practice produces people who "don't know what they don't know". AI makes an experienced engineer faster because they can judge its output. Building that judgement is what you're here for.

## Common mistakes

**Watching instead of doing.** A video makes a topic feel familiar, which is easy to mistake for understanding. Close the video and write the code from memory.

**Pressing Check repeatedly with small random changes.** If a test fails twice, stop. Re-read the task and the failing test's message, and predict what your code returns for that input.

**Copying the full error into an AI tool before reading it.** Read the last line first. Half the time you'll know the answer.

**Asking for the whole solution when you wanted a hint.** Be specific: "Don't give me code. What concept am I missing?"

**Skipping the review queue.** Quiz questions you got wrong come back for a reason: spaced repetition is one of the most reliable ways to make knowledge stick.

## Recap

- Practise at the edge of your ability, with feedback, and redo hard exercises later from scratch.
- **Predict, then run.** Wrong predictions are where learning happens. Treat Check as confirmation, not a search tool.
- Read errors **bottom up**: the error type and message, then your own line number, then the values on that line.
- Check the **official docs** early. Ask questions with a minimal example, expected vs actual, and what you tried.
- **AI as tutor, not ghostwriter:** attempt first, ask for explanations, never keep code you can't explain, and debug yourself first. The research shows this is the difference between using AI and losing your learning to it.
