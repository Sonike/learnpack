# Using AI tools responsibly

## Why this matters

AI coding tools are now normal at work. In the 2025 Stack Overflow Developer Survey, 84% of respondents said they use or plan to use them. In the same survey, more developers said they *distrust* the accuracy of AI output (46%) than trust it (33%). Both numbers matter to you. Employers will expect you to use these tools well, and they'll expect you to catch the mistakes the tools make. That second part is only possible if you can do the work yourself, which is why this lesson comes near the end of the course, after the fundamentals.

## What these tools are

There are two broad kinds:

- **Assistants**: you ask, they answer. Chat tools and in-editor autocomplete fall here. They suggest a function, explain an error, or draft a test.
- **Agents**: you give a goal, and they take several steps on their own. They read files, edit code, run commands and tests, and loop until they think they're done.

Under the hood both are **large language models**: programs trained on huge amounts of text, including public code, that predict likely next words. That explains their strengths and weaknesses.

```
 Good at                                  Bad at
 ───────                                  ──────
 Explaining code and errors               Knowing your codebase's unwritten rules
 Common patterns and boilerplate          Being right about rare or new APIs
 Drafting tests and docs                  Saying "I don't know"
 Translating between languages            Edge cases nobody asked about
 Spotting typos and simple bugs           Security, unless told to look
```

Because they produce *likely-looking* code, the code usually looks clean and confident even when it's wrong. A model can invent a function, a library option or an entire package, and present it with the same certainty as `print`. This is called a **hallucination**.

## What the evidence says about learning

In January 2026, Anthropic published a randomised controlled trial: junior engineers learned a new Python library either with an AI assistant or by hand, then took a quiz without help. The AI group scored about **50%**, the hand-coding group about **67%**. The biggest gap was on **debugging** questions.

How people used the assistant mattered more than whether they used it. Learners who asked it **conceptual questions**, or asked for **explanations** alongside the code, kept their learning (65% and above). Learners who **delegated** writing or debugging the code scored **under 40%**.

So the course rule has been, and stays:

> AI may explain; you write the code. Once a skill is solid, AI can speed it up.

Using AI to *skip* the practice gives you working code today and no skill tomorrow, and interviews test the skill.

## A workflow that works

When you use an assistant or agent for real work, this loop keeps you in control:

```
 1. Spec        Write down what you want: inputs, outputs, edge cases.
 2. Small step  Ask for one function or one change, not a whole feature.
 3. Read        Read every line. Can you explain it? If not, ask, or rewrite.
 4. Test        Run tests YOU understand. Add the edge cases it skipped.
 5. Commit      Small commit, clear message. Then the next small step.
```

Step 3 is the one people skip. Step 4 only works if the tests are good: if the AI wrote both the code and the tests, the tests often just confirm what the code does, including its bugs. Write, or at least read, the tests yourself.

## Reviewing AI-written code: a worked example

Here's a function an assistant might produce for "parse the dates in a CSV column and return them in UTC". It runs. Read it carefully before reading on:

```python
import csv, io
from datetime import datetime, timezone

def parse_csv_dates(csv_text, column):
    reader = csv.DictReader(io.StringIO(csv_text))
    rows = list(reader)
    results = []
    for row in rows[1:]:  # skip the header row
        value = row[column].strip()
        if not value:
            continue
        try:
            parsed = datetime.fromisoformat(value)
            results.append(parsed.replace(tzinfo=timezone.utc))
        except ValueError:
            continue  # ignore bad rows
    return results
```

Now try it:

```python
text = "id,at\n1,2026-03-01T09:30:00+01:00\n2,2026-03-01T12:00:00+00:00\n"
print([d.isoformat() for d in parse_csv_dates(text, "at")])
# ['2026-03-01T12:00:00+00:00']
```

Two rows went in and one came out. The comment says "skip the header row", but `DictReader` *already* used the header to name the columns, so `rows[1:]` skips the first real row. That's an off-by-one bug, and the confident comment makes it easy to miss.

There are two more bugs. `replace(tzinfo=...)` *overwrites* the time zone instead of *converting*, so `09:30+01:00` becomes `09:30` UTC instead of `08:30` UTC, an hour wrong. And `except ValueError: continue` silently drops bad data: a typo in the file just disappears. You'll fix all three in this lesson's exercise. The pattern is typical: nothing crashes, it looks tidy, and it's wrong in exactly the ways a quick glance won't catch.

## Hallucinated packages

Sometimes an assistant says `pip install some-package` for a package that doesn't exist. Attackers know this happens and register those made-up names on PyPI with malicious code inside. This is sometimes called **slopsquatting**. Installing a package runs its code on your machine with your permissions, and a virtual environment doesn't stop that.

Before installing anything you don't recognise:

1. Search for it on **pypi.org**. Does it exist? Who publishes it? When was it released?
2. Check its **homepage or repository**. Is it maintained? How many people use it?
3. Check the **official docs** of the library you're actually using. Does it mention this package?

Python can also tell you whether a module is part of the standard library:

```python
import sys

print("json" in sys.stdlib_module_names)      # True
print("requests" in sys.stdlib_module_names)  # False: a third-party package
```

In the exercise you'll use this, plus Python's `ast` module, to flag every import that is neither standard library nor on your team's approved list.

## Secrets, data and company rules

Anything you paste into an AI tool leaves your machine and goes to the company that runs it. At work, follow these rules without exception:

- **Only use tools your employer has approved**, with the company account, not a personal one. Approved tools come with contracts about how data is stored and used.
- **Never paste secrets**: passwords, API keys, tokens, private keys. Not even "just to debug". If you did, treat the secret as leaked and rotate it.
- **Never paste customer or personal data**: names, emails, addresses, support tickets, database rows.
- **Ask before pasting proprietary code** into any tool that isn't approved for it.

When in doubt, ask your manager. Nobody gets in trouble for asking; people do get in trouble for leaking customer data.

## Licensing and attribution

AI tools learned from public code, and occasionally reproduce chunks of it closely. Public code still has a **license** that says how you may use it. If a suggestion looks like it came from a specific project (unusual names, a copied comment, a long distinctive block), don't paste it into your employer's codebase. Some companies require you to mention AI use in your PR description. Follow your team's rule.

## Talking about AI in interviews

Interviewers will ask how you use AI tools. A good answer is honest and specific:

```
I use it like a patient senior engineer: to explain unfamiliar code or
errors, and to review my work. While I was learning, I wrote the code
myself first and only used it to explain. Now I use it to draft
boilerplate and tests, but I read every line and run tests I understand.
Last month it suggested a pandas option that doesn't exist; the test
caught it.
```

That answer shows you know the strengths, the risks, and that you're in charge. "I don't use AI at all" sounds out of date; "it writes most of my code" sounds like a risk.

## Common mistakes

- **Trusting tidy code.** Clean formatting and confident comments say nothing about correctness. Read it.
- **Letting the AI write the tests for its own code.** The tests then agree with the bugs.
- **Asking for a whole feature in one go.** You get 300 lines you can't review. Ask for small steps.
- **Installing suggested packages without checking.** Check PyPI and the official docs first.
- **Pasting the error *and* the database password.** Strip secrets and personal data from anything you paste.
- **Delegating debugging while you're learning.** The research is clear that this is where skill loss is largest. Debug it yourself, then ask the AI to explain anything you still don't understand.

## Recap

- Assistants answer questions; agents take multi-step actions. Both predict likely code, so they can be confidently wrong.
- Evidence (Anthropic, 2026): delegating code and debugging hurt learning; asking for explanations didn't. AI may explain; you write the code until the skill is solid.
- Workflow: spec → small step → read every line → run tests you understand → commit.
- Check any unfamiliar package on PyPI before installing it.
- Only approved tools at work; never paste secrets, customer data or proprietary code where it isn't allowed.
- In interviews, describe your real, specific workflow, including how you catch the tool's mistakes.
