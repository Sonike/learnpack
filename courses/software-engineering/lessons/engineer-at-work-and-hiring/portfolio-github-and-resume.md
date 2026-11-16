# Portfolio, GitHub and resume

## Why this matters

When you apply for a junior role, you have no work history to point to. What you have is **evidence**: projects someone can open, run and read, and a one-page resume that makes them want to look. Hiring managers are busy and skim. A recruiter may give your resume under a minute; an engineer may give each repo about the same. This lesson is about making those minutes count.

## What hiring managers look for

The people hiring juniors are mostly trying to answer three questions:

1. **Can you build something real and finish it?**
2. **Can you work like an engineer?** Tests, clear commits, a README, sensible structure.
3. **Will you learn fast and be good to work with?**

In October 2026, Felix Rieseberg, an engineer at Anthropic and co-maintainer of Electron, wrote in his post "Hunger beats tenure" that he had removed the coding interview from his team's process and now looks for small prototypes that show **taste, empathy and principled thinking**, and he advises juniors to tie their work to real goals and ship things. That's one team, and most companies still run coding interviews (see the lesson "Coding interviews"). But it points the same way as nearly every hiring manager you'll meet: **finished, real projects beat certificates and clones**.

### Depth beats volume

Twenty half-finished tutorials and to-do-app clones say "I follow along". Two or three **deep** projects say "I build":

```
 Weak portfolio                       Strong portfolio
 ──────────────                       ────────────────
 todo-app                             habit-tracker-api
 weather-app                            FastAPI + SQLite, auth, 94% coverage,
 calculator                             CI, deployed, used by 12 club members
 tutorial-flask-blog                  file-organiser
 netflix-clone                          CLI with dry-run and undo, on PyPI
 my-first-repo                        an open source PR merged into a tool
 ...14 more                             you actually use
```

What makes a project deep:

- It solves a **real problem** for a real person, ideally not just you.
- It has **tests** and **CI**, and they pass.
- It's **deployed** or installable, so someone can try it in a minute.
- You made and can explain **design decisions** ("I chose SQLite because…").
- You can **extend it live**. Some interviews now ask exactly that.

The projects you've built in this course (the file organiser, the expense tracker, the REST API you shipped) are the start of this portfolio. The capstone is meant to be the centrepiece.

## READMEs that sell the project

The README is the front page of a project. A reviewer reads the top and decides whether to keep going. Put things in this order:

```markdown
# Habit Tracker API

Track daily habits with streaks and reminders. Built for my running
club's 12 members, who use it every day.

**Live demo:** https://habits.example.com/docs  ·  ![demo](demo.gif)

## Run it locally
    git clone ... && cd habit-tracker
    python -m venv .venv && source .venv/bin/activate
    pip install -e ".[dev]"
    uvicorn app.main:app --reload

## Run the tests
    pytest        # 87 tests, 94% branch coverage

## Design decisions
- SQLite, not Postgres: one small server, under 1,000 writes a day.
- Streaks computed on read, not stored: simpler, and fast at this size.

## What I'd do next
- Push notifications instead of email reminders.
```

1. **One sentence: what it does and for whom.** No backstory.
2. **Proof it works**: a live link, a screenshot or a short GIF.
3. **How to run it** and **how to run the tests**, copy-pasteable.
4. **Design decisions**: two or three, with the reasons. This is what separates you from people who followed a tutorial.
5. **What's next**: shows you know its limits.

Test your README by following it yourself on a fresh clone. If a step is missing, the reviewer will hit it too.

## A clean GitHub profile

Your GitHub profile is often the second link a recruiter clicks. Make it easy:

- **Pin your best 3–6 repos** (Profile → Customize your pins). These are what people see first.
- **Add a profile README**: a repo named exactly like your username, with a `README.md`. Three or four lines: who you are, what you build, how to reach you.
- **Archive or make private** the old tutorial repos you don't want judged.
- **Write descriptive repo descriptions** and add topics, so the repo list itself reads well.
- **Commit history matters a little.** Clear messages and steady work look better than one "final version" commit. You don't need a green square every day.

## The one-page resume

A junior resume should be **one page**. Use a simple, single-column layout. Jake's resume template (free on GitHub, LaTeX or an Overleaf copy) is a widely used choice. A typical order:

```
 Name · email · GitHub · LinkedIn · city (or "Remote")

 Education        degree / bootcamp / this course, dates

 Projects         3 projects, 2–3 bullets each, with links
                  (for career changers and new grads, projects go ABOVE
                   experience if they're your strongest evidence)

 Experience       any jobs, including non-tech, with transferable results

 Skills           Languages: Python, SQL · Tools: Git, pytest, FastAPI,
                  GitHub Actions, Docker
```

### Writing bullets

Each bullet should be: **action verb + what you did + evidence**. Evidence is usually a number: users, speed, size, coverage, time saved.

```
 Weak:    Responsible for the backend of a group project.
 Weak:    Worked with Python, FastAPI, SQLite and pytest.
 Strong:  Built a habit-tracking API (FastAPI, SQLite) used daily by
          12 club members; 94% test coverage, deployed with CI.
 Strong:  Cut a CSV import from 40 s to 3 s by batching inserts in one
          transaction.
```

"Responsible for" describes a duty, not something you achieved. A list of tools with no result shows nothing. Numbers make bullets believable and memorable, even small ones ("12 users", "3 s", "87 tests").

Non-tech experience counts. "Trained 4 new staff on the stock system" from a retail job shows teaching and reliability. Keep it short and pick bullets with results.

You can check your bullets automatically. This is the core of the exercise:

```python
ACTION_VERBS = {"built", "cut", "reduced", "shipped", "designed"}

bullet = "Responsible for testing"
first = bullet.split()[0].lower()
print(first in ACTION_VERBS)                     # False
print(any(ch.isdigit() for ch in bullet))        # False
```

### Tailoring

For each application, spend ten minutes adjusting:

- Reorder projects so the most relevant one is first (an API project for a backend role).
- Use the job ad's words where they're true for you. If it says "REST APIs" and you built one, say "REST API", not just "backend".
- Cut what isn't relevant to make room.

### Myths about ATS

An **ATS** (applicant tracking system) is the software companies use to collect and sort applications. You'll read that "75% of resumes are rejected by robots". That claim isn't backed by good evidence. In most companies the ATS stores and searches applications, and a person reads them. What actually matters:

- A **simple layout** (single column, real text, no text inside images) so it parses correctly.
- **Honest keyword overlap** with the job ad, because recruiters do search.
- A **PDF**, unless they ask for something else.

Don't stuff invisible keywords into the page or invent skills. Humans read it, and interviewers will ask about everything on it.

## Common mistakes

- **Many shallow projects.** Pin three good ones; archive the rest.
- **A README that starts with "This is my project for…"** Start with what it does and a demo.
- **Setup steps that don't work.** Test them on a fresh clone.
- **Two-page resumes** for juniors. Cut to one.
- **Bullets with no numbers** and "responsible for". Use action + result + number.
- **Listing every technology you've touched.** Only list what you'd be comfortable being asked about.
- **Fancy templates** with columns, graphics and skill bars. Hard to read and parse. Keep it plain.
- **Lying or exaggerating.** "Used by thousands" when it's used by you will come out in the interview.

## Recap

- Hiring managers want evidence that you can build real things, work like an engineer, and learn fast.
- Two or three **deep** projects (real users, tests, CI, deployed, explained decisions) beat many clones.
- README order: what and for whom → demo → run it → run tests → design decisions → what's next.
- Pin your best repos, add a short profile README, archive the rest.
- One-page resume, simple layout. Bullets = action verb + what + number. Tailor for each role.
- The ATS mostly stores applications; people read them. Keep the layout simple and the keywords honest.
