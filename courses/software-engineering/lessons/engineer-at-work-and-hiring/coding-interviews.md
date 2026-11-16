# Coding interviews

## Why this matters

In 2026, a live coding round is still the most common technical screen for junior roles. You get a problem, 30–45 minutes, and an interviewer watching you think. Some teams are moving to other formats, such as debugging unfamiliar code or extending your own project, and those are covered below. Either way, the skill being tested is the same: can you take a fuzzy problem, reason about it out loud, and turn it into correct code? That skill is trainable, and this lesson gives you the method.

## What the interviewer is actually grading

Most candidates think the goal is "get the optimal answer". Interviewers usually score several things:

```
 Communication     Did you clarify, explain your thinking, take hints?
 Problem solving   Did you find an approach, compare options, optimise?
 Coding            Is the code correct, readable, idiomatic?
 Testing           Did you check it with examples and edge cases?
 Complexity        Can you state and justify the Big-O?
```

A candidate who talks clearly, writes a correct brute-force solution, and explains how to optimise it often scores better than one who silently writes an optimal answer with a bug. Thinking out loud isn't optional: if the interviewer can't hear your reasoning, they can't give you credit for it.

## The flow: seven steps

Use the same steps every time, in practice and in interviews, until they're automatic.

```
 1. Clarify      Restate the problem. Ask about input size, empty input,
                 duplicates, negatives, sorted or not, what to return.
 2. Examples     Write 2–3 small examples by hand, including an edge case.
 3. Brute force  Say the simplest correct approach and its Big-O.
 4. Optimise     Find the repeated or wasted work. Pick a better pattern.
 5. Code         Write it cleanly, explaining as you go.
 6. Test         Trace your code on your examples, line by line.
 7. Complexity   State time and space, and why.
```

Here's what that sounds like on a real problem: *"Given a list of integers, return the length of the longest run of consecutive values."*

**1. Clarify.** "Can the list be empty? Then I return 0. Can there be duplicates? Do they count once? Does the run have to be next to each other in the list, or any order?" (Any order; duplicates count once.)

**2. Examples.** `[100, 4, 200, 1, 3, 2]` → 4 (1, 2, 3, 4). `[]` → 0. `[1, 2, 2, 3]` → 3.

**3. Brute force.** "I could sort, then walk through counting runs. That's O(n log n) for the sort."

**4. Optimise.** "Can I avoid sorting? If I put the numbers in a set, I can check 'is x + 1 here?' in O(1). The waste would be re-counting the same run from every number in it, so I'll only start counting at a number whose `x - 1` isn't in the set: that's the start of a run."

**5. Code.**

```python
def longest_consecutive(nums):
    values = set(nums)
    best = 0
    for x in values:
        if x - 1 in values:
            continue              # not the start of a run
        length = 1
        while x + length in values:
            length += 1
        best = max(best, length)
    return best

print(longest_consecutive([100, 4, 200, 1, 3, 2]))  # 4
print(longest_consecutive([]))                       # 0
```

**6. Test.** Trace `[1, 2, 2, 3]`: the set is {1, 2, 3}. At 1, 0 isn't present, so count 1, 2, 3 → length 3. At 2 and 3, skip. Returns 3. Correct.

**7. Complexity.** "O(n) time: each number is checked as a start once, and the inner loop visits each number at most once overall. O(n) space for the set."

You'll solve this one yourself in the exercises, plus two more.

## The patterns map

There are thousands of interview problems but only a dozen or so ideas behind most of them. Learning to recognise the **pattern** from the wording is the real skill. You've met all of these in the data structures and algorithms section:

```
 If the problem says…                            Try…
 ──────────────────────────────────────────────  ─────────────────────────
 "have we seen this before?", pairs summing to   Hash map / set
 a target, counting, grouping
 sorted array, pair or triple meeting a condition  Two pointers
 longest/shortest contiguous subarray/substring  Sliding window
 matching brackets, "next greater", undo          Stack
 sorted data, or "smallest X that works"          Binary search
 shortest path / fewest steps, levels             BFS (queue)
 all paths, connected regions, trees              DFS (recursion or stack)
 k largest / smallest, "next earliest"            Heap (heapq)
 overlapping intervals, scheduling                Sort first, then sweep
```

Two examples of reading the clues:

- *"Fewest single-letter changes to turn one word into another"*: "fewest steps" means **BFS**, where each word is a node and one-letter changes are the edges. That's the word ladder exercise.
- *"Minimum rooms so overlapping meetings don't clash"*: "overlapping intervals" means **sort by start**, then use a **heap** of end times to know when the earliest room frees up. That's the meeting rooms exercise.

```python
import heapq

ends = []
heapq.heappush(ends, 30)
heapq.heappush(ends, 10)
print(ends[0])              # 10: the earliest end time is always at index 0
print(heapq.heappop(ends))  # 10
```

## How to practise

How you practise matters more than how many problems you do.

**Patterns over volume.** Don't try to solve hundreds of random problems. Work through a curated list grouped by pattern: the **NeetCode 150** (with free video solutions) or **Grind 75** from the Tech Interview Handbook. Pick one list and finish it after this course.

**Reason before you run.** This is the most important habit. Ryan Peterman, a former Meta engineer, described going from failing every onsite to passing most of them by changing one thing: he stopped pressing "run tests" to reverse-engineer the answer and started thinking the solution through first. In interviews there's often no test button. So in practice:

1. Set a timer (30–35 minutes).
2. Work through the seven steps on paper or in comments.
3. Trace your code on your examples by hand.
4. **Only then** press Check.

The Check button in these exercises plays the role of "run tests". Treat a failure as information about your reasoning, not as a hint generator.

**Spaced repetition.** Keep a **mistakes log**: every problem you couldn't solve, with one line on the idea you missed. Re-solve each one a week later without looking. The ones you still miss go back in the log.

**Mock interviews.** Practise out loud, with a friend or another learner playing interviewer, or record yourself. Talking while coding feels awkward at first. Only practice fixes that.

## When you're stuck

Everyone gets stuck. What you do next is part of the grade.

- **Say what you're thinking.** "I'm trying to avoid the nested loop. The repeated work is recomputing the sum each time…"
- **Fall back to brute force.** A correct O(n²) solution is real progress. Write it, then improve it.
- **Try a smaller example**, or draw the data.
- **Run through the patterns map.** "Could a hash map help? Would sorting help?"
- **Take hints gracefully.** A hint isn't a failure; ignoring one is.

Never go silent for minutes, and never say "I don't know" and stop.

## The newer formats

Some teams have replaced or added to the classic round. Prepare for these too:

- **Practical coding**: build a small feature, such as an endpoint, a parser or a CLI command, in a realistic setting, often with internet access.
- **Debugging**: you get unfamiliar code with a failing test and have to find the bug. The debugging and reading-code lessons are your preparation.
- **Extending your own project**: "Add a filter to your habit tracker's API." You need to know your portfolio projects inside out. Practise adding a small feature to one of them in 30 minutes.
- **Code review**: you get a pull request and comment on it, exactly as in the lesson "Code review".
- **AI-allowed rounds**: some companies let you use an assistant and watch how you use it: do you check its output, test it, and explain it?

## Common mistakes

- **Coding immediately.** Two minutes of clarifying saves twenty of rewriting. Always do steps 1–3.
- **Silence.** The interviewer can't grade thoughts they can't hear.
- **Skipping the test step.** Trace your code on an example before saying "done". Interviewers notice when you find your own bug.
- **Memorising solutions.** Interviewers change the details. Learn why each pattern works.
- **Wrong complexity claims.** `x in my_list` inside a loop is O(n²), not O(n). Know the cost of each operation.
- **Grinding hundreds of problems** without reviewing mistakes. Fewer problems with a mistakes log beats volume.

## Recap

- Interviewers grade communication, problem solving, code, testing and complexity, not just the final answer.
- Use the seven steps every time: clarify, examples, brute force, optimise, code, test, complexity.
- Learn the patterns map; most problems are a known pattern in disguise.
- Practise with a timer, reason before you press Check, keep a mistakes log, and do mock interviews out loud.
- When stuck, think aloud, write the brute force, try small examples, take hints.
- Prepare for practical, debugging, extend-your-project and review rounds too.
