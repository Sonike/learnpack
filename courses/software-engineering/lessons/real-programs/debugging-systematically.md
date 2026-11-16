# Debugging systematically

Engineers spend more time finding bugs than writing new code, and the difference between a junior and a senior often shows most clearly here. Beginners change things at random until the error goes away; experienced engineers follow a method, and it's faster even when it feels slower. This lesson gives you that method and the tools that support it: well-placed prints, the debugger, bisecting and minimal reproductions.

> **Note:** this is the skill AI assistants most easily take away from you. In a 2026 study of engineers learning new code, the group that let AI do their debugging scored worst on later debugging questions. Use AI to explain an error or a concept, but find and fix the bug yourself until you're confident.

## The scientific method for bugs

A bug is a gap between what you **expected** the code to do and what it **actually** does. Debugging is closing that gap with evidence, one step at a time:

```
1. Reproduce   ->  make the bug happen on demand
2. Hypothesise ->  guess one specific cause
3. Test        ->  check the guess with evidence
4. Fix         ->  change the code for the real cause
5. Protect     ->  add a test so it never comes back
```

**1. Reproduce.** Find the exact input and steps that trigger the bug, ideally in one command you can re-run in seconds. A bug you can't reproduce is a bug you can't confirm you've fixed.

**2. Hypothesise.** Make one specific, checkable guess: "the discount is applied twice", not "something's wrong with discounts". Use the evidence you have: the traceback, the wrong output, what changed recently.

**3. Test the hypothesis.** Look at the actual values: print them, or pause the program in a debugger. Either the evidence supports your guess, or it rules it out. Both outcomes are progress; a ruled-out guess narrows the search.

**4. Fix the cause, not the symptom.** If a total comes out negative, `max(0, total)` hides the symptom. Finding out *why* it's negative fixes the bug.

**5. Add a regression test.** A **regression** is a bug that comes back after being fixed. Write a small test that fails with the old code and passes with the new code. You'll learn testing properly in the testing section; even a simple `assert` in a test file counts for now.

Write down what you've tried as you go. When a bug takes more than twenty minutes, notes stop you going in circles, and they're exactly what you'll need if you ask someone for help.

## Print debugging, done well

The simplest tool is `print`. It's not unprofessional: plenty of senior engineers reach for it first. But do it deliberately.

```python
def average_rating(reviews):
    total = 0
    for r in reviews:
        total += r["stars"]
    return total / len(reviews)

reviews = [{"stars": 5}, {"stars": "4"}, {"stars": 3}]
print(average_rating(reviews))
# TypeError: unsupported operand type(s) for +=: 'int' and 'str'
```

A useful print shows **what** and **which**, with `repr` so you can see types and hidden whitespace. The `=` inside an f-string does this for you:

```python
for r in reviews:
    print(f"{r=}")
    total += r["stars"]
# r={'stars': 5}
# r={'stars': '4'}
```

Now it's obvious: one rating is the string `'4'`, not the number `4`. Where did it come from? That's your next hypothesis (probably a CSV file, where everything is a string).

Tips:
- Print **before** the line that fails, so you see the values that caused it.
- Label every print (`f"{x=}"`), or you'll lose track of which number is which.
- Remove debugging prints when you're done. `git diff` (from the Git section) makes them easy to spot.

## The debugger: pause and look around

A **debugger** lets you pause a running program at any line, look at every variable, and then step forward one line at a time. For anything beyond a quick check it beats print, because you don't have to guess in advance what to print.

### breakpoint() and pdb

Python has a debugger built in, called **pdb**. Put `breakpoint()` on the line where you want to pause:

```python
def average_rating(reviews):
    total = 0
    for r in reviews:
        breakpoint()
        total += r["stars"]
    return total / len(reviews)
```

Run the file in a terminal and the program stops there with a `(Pdb)` prompt:

```bash
$ python ratings.py
> /home/ada/ratings.py(4)average_rating()
-> breakpoint()
(Pdb) p r
{'stars': 5}
(Pdb) c
> /home/ada/ratings.py(4)average_rating()
-> breakpoint()
(Pdb) p r, total
({'stars': '4'}, 5)
(Pdb) q
```

The `->` arrow shows the line about to run. (On Python 3.12 it points at the line after `breakpoint()`; from 3.13 it points at the `breakpoint()` call itself. Either way, nothing below it has run yet.) The first `c` ran one full loop iteration and paused again on the second review, which is the one with the string `'4'`.

The commands you need first:

| Command | Name | What it does |
|---|---|---|
| `p expr` | print | Show the value of any expression, e.g. `p r["stars"]` |
| `n` | next | Run the current line and stop at the next one in this function |
| `s` | step | Like `n`, but if the line calls a function, go **into** it |
| `c` | continue | Run until the next breakpoint (or the end) |
| `l` | list | Show the code around where you are |
| `w` | where | Show the call stack, like a traceback |
| `q` | quit | Stop the program |

> **Note:** `breakpoint()` needs a terminal you can type into, so it won't work in the in-browser practice editor. Try it on your own machine.

### The VS Code debugger

VS Code (with the Python extension) gives you the same thing with a mouse:

1. Click in the margin to the left of a line number. A red dot appears: that's a **breakpoint**.
2. Open the Run and Debug panel and choose "Python Debugger: Debug Python File" (or press F5).
3. The program pauses at the red dot. The **Variables** panel shows every local variable; hover over any name in the code to see its value.
4. Use the toolbar: **Step Over** (run this line, like `n`), **Step Into** (go into the function this line calls, like `s`), **Continue** (like `c`).
5. Add expressions to the **Watch** panel to see them update as you step, e.g. `total` or `len(reviews)`.

You can right-click a breakpoint and add a **condition**, like `r["stars"] == "4"`, so it only pauses on the interesting loop iteration instead of all 10,000. The VS Code docs in the resources show every feature.

## Narrowing it down

When you have no idea where a bug is, don't read the whole program. **Halve the search space** instead.

### Bisecting your code

Add a check halfway through the process: is the data still correct at this point? If yes, the bug is in the second half; if no, it's in the first half. Repeat. Ten checks can find one bad line among a thousand, because each check throws away half of what's left.

The same idea works on **data**: if a 10,000-row file crashes your import, try the first 5,000 rows. Still crashes? Try the first 2,500. You'll find the one bad row quickly.

### Bisecting your history: git bisect

If the code worked last week and is broken today, the bug was introduced by one of the commits in between. You'll learn Git in the next section; here's the preview. `git bisect` checks out the commit halfway between "known good" and "known bad", you test it and say `good` or `bad`, and it halves again:

```bash
$ git bisect start
$ git bisect bad              # the current version is broken
$ git bisect good v1.4        # version 1.4 worked
Bisecting: 15 revisions left to test after this (roughly 4 steps)
[3f9c2a1] Add bulk discount codes
$ python -m pytest -q         # test this version...
$ git bisect bad              # ...it's broken too
Bisecting: 7 revisions left to test after this (roughly 3 steps)
[b07e4d9] Cache product prices
```

After about five steps it names the exact commit that broke things. With 1,000 commits it would take about ten. That's **binary search**, and you'll implement it in the practice exercise "first bad version".

### Minimal reproductions

A **minimal reproduction** (or "repro") is the smallest program that still shows the bug. You make one by deleting things: remove a function, re-run, still broken? Keep deleting. Back to working? Put it back; that piece matters.

This is the most underrated debugging technique. Very often, the act of shrinking the problem reveals the cause. If it doesn't, you now have a ten-line example to share instead of a thousand-line project, and people can actually help you.

## Rubber duck debugging

Explain the code, line by line, out loud, to someone who knows nothing about it: a colleague, a friend, or literally a rubber duck on your desk. "This loop goes over every review, adds the stars to the total, which is... oh. Stars is a string here." Saying each step forces you to check assumptions you'd skip when reading silently. It works far more often than it should.

## Writing a good bug report

Sometimes the bug isn't yours to fix: it's in a library, or another team's service. A good bug report gets fixed; a vague one gets ignored. Include:

- **What you did:** exact steps, or the minimal reproduction.
- **What you expected to happen.**
- **What actually happened**, with the full error message and traceback, copied as text, not a screenshot.
- **Your environment:** Python version (`python --version`), library versions, operating system.
- **What you've already tried.**

Simon Tatham's essay "How to Report Bugs Effectively" (in the resources) is the classic guide. It's worth reading once.

## Common mistakes

**Changing several things at once.** You edit three lines, the bug disappears, and you don't know which change fixed it, or whether the other two broke something else. One change, then re-run.

**Not reproducing first.** "I think I fixed it" isn't the same as "I ran the steps that failed, and now they pass".

**Trusting your assumptions.** "That variable can't be `None` here." Check it. The bug is, almost by definition, in the part you're sure is right.

**Fixing the symptom.** Wrapping the failing line in `try`/`except`, adding `if x is not None` everywhere, or rounding away a wrong number makes the error message disappear and the bug stay.

**Never taking a break.** After an hour of staring, walk away for ten minutes. Many bugs are solved in the kitchen.

## Recap

- Debugging is a method: **reproduce, hypothesise, test, fix, add a regression test.**
- Print well: labelled, with `repr` (`print(f"{x=}")`), just before the failing line.
- Use the debugger (`breakpoint()` in a terminal, or VS Code breakpoints) to pause and inspect. In pdb, `p` prints, `n` steps over, `s` steps into, `c` continues.
- When you don't know where to look, halve the search: in your code, your data, or your history with `git bisect`.
- Shrink the problem to a minimal reproduction; explain it to a rubber duck; write bug reports with steps, expected, actual and environment.
