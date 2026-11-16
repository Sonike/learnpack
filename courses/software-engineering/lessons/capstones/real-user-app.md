# Capstone A: A product someone actually uses

> **Note:** Pick **one** of the two capstones; the second is optional. This one takes about 40–60 hours, or 4–6 weeks at 10–15 hours a week. It pulls together everything: Python, Git, clean code, testing, SQL, APIs and shipping.

## The goal

Build and ship a small web application that solves a **real problem for a real person or group**: a club, a family, a small shop, a teacher, a sports team, a church, a neighbour. Not a to-do app for an imaginary user, but something a named person uses at least once and gives you feedback on. Then make it look like professional work: issues and pull requests for every feature, tests in CI, a deploy with logs and a health check, a design doc, and a demo video.

Last, and most important for interviews: be ready to **add a small feature to it live, in 30 minutes**, while explaining what you're doing.

## Why it impresses

Hiring managers see hundreds of portfolios with the same tutorial projects. Three things make this one stand out:

- **A real user.** A quote in the README from the person who used it ("we stopped using the shared spreadsheet") is evidence you can turn a fuzzy need into working software. That is the job.
- **Professional process, visible.** Issues, small PRs, CI and a design doc show you can work the way a team works, before anyone has hired you onto one.
- **You can extend it live.** More teams are replacing puzzle-style coding rounds with practical ones: "walk me through your project", "add this feature", "this test fails, fix it". A project you know deeply is the best preparation for those, and it's still worth keeping your data-structures practice going for the teams that do ask puzzles.

## Choosing the problem

Spend a week on this before writing code. Talk to two or three people about something annoying they do by hand. Good capstone problems share four traits:

1. **Small.** The core can be done in about five endpoints.
2. **Data-shaped.** People, things, dates and statuses that fit nicely in a few tables.
3. **Has more than one user**, so authorisation matters (members only see their own data; an admin sees everything).
4. **Someone will actually try it** within the next month.

Some shapes that work well:

```
- Equipment loans for a club:  members borrow gear, the treasurer sees who has what
- Shift sign-up for volunteers: coordinator posts shifts, volunteers claim them
- Practice tracker for a music teacher: students log practice, teacher sees totals
- Orders for a home bakery: customers request orders, baker confirms and marks paid
- Chore rota for a shared house: tasks rotate weekly, people mark them done
```

Write a one-paragraph **problem statement** with the user's name (or role, if they prefer privacy) and what they do today without your app. Get them to agree it's right.

## Scope

**In scope**
- A FastAPI backend with SQLite (or Postgres if your host provides it), using plain SQL through a repository layer, as in the databases section.
- 5–10 endpoints covering the core workflow, with Pydantic validation and correct status codes.
- Accounts with hashed passwords (use a maintained library such as `argon2-cffi` or `bcrypt`) and token auth.
- **Authorisation**: users can only see and change what they're allowed to. Tests prove that user A gets `403` or `404` on user B's data.
- A simple frontend is **optional**: server-rendered templates or one plain HTML page that calls the API is plenty. FastAPI's `/docs` page is acceptable for the first user test if your user is comfortable with it; most aren't, so a minimal page is worth it.
- Everything from the Ship it project: config from the environment, JSON logs with redaction, `/health`, CI, a live deploy, a tested rollback.

**Out of scope** (say so in your README)
- Payments, real-time chat, mobile apps, email delivery at scale, microservices.
- A polished design. Clean and usable beats pretty.
- Features your user didn't ask for.

## Milestones

```
Week 1  Problem and plan
        - Problem statement agreed with your user
        - 8–15 user stories with acceptance criteria, as GitHub issues
        - A public GitHub project board (To do / In progress / Done)
        - One-page design doc: components, data model, API sketch, one trade-off
        - Repo with README skeleton, ruff + pytest in CI, branch protection on main

Week 2  The core workflow
        - Schema and repository layer with integration tests on :memory: SQLite
        - The 3–4 endpoints of the main workflow, test-first where you can
        - Every feature: issue -> branch -> small PR -> CI green -> merge

Week 3  Users and permissions
        - Sign-up, login, hashed passwords, token auth
        - Authorisation rules, with tests for "other user's data" cases
        - First ADR: a decision note (e.g. "why tokens, not sessions")

Week 4  Ship and test with your user
        - Deploy with env config, JSON logs, /health; rollback drill done
        - Minimal frontend if needed
        - Your user tries it; you watch and take notes without helping

Week 5  Feedback and polish
        - Fix the top 3 issues from the user test (each as an issue + PR)
        - Second ADR: a decision the feedback changed
        - Coverage reported in CI; README finished

Week 6  Show it
        - 3-minute demo video
        - "What I'd do next" write-up
        - Live-extension practice (see below), at least twice
```

## Deliverables

**In the repository**
- `README.md` that leads with: what it is, who uses it, the live URL, a screenshot or GIF, and the user's quote. Then: how to run it locally, how to run the tests, the environment variables, and links to the design doc and ADRs.
- `docs/design.md`: problem, constraints, components (ASCII diagram), data model, API table, trade-offs.
- `docs/adr/0001-*.md` and `docs/adr/0002-*.md`: two decision notes, each with context, the decision, the alternatives and the consequences.
- Tests: unit tests for the business rules and integration tests for the API, including the auth and "other user's data" cases. Coverage shown in CI.
- `docs/next.md`: what you'd build next and why, in priority order, including known technical debt.

**Outside the repository**
- The live deploy, with `/health` returning 200.
- A **3-minute demo video** (screen recording with your voice is fine): the problem in 20 seconds, the main workflow, one piece of code you're proud of, and one thing you'd change.

## The live-extension drill

This is the practice that pays off in interviews. Ask a friend (or write on cards and draw one at random) for a small feature request, set a 30-minute timer, and talk out loud while you:

1. Restate the request and ask one or two clarifying questions.
2. Find where the change goes (route, repository, schema).
3. Write a failing test first.
4. Make it pass, run the whole suite, and commit.

Examples of good drill requests: "add a `notes` field to loans", "let admins list overdue items", "reject bookings more than 30 days ahead", "add pagination to the list endpoint". Afterwards, write two lines on what slowed you down. Do this at least twice before you list the project on your resume.

> **Note:** AI assistants are allowed for explanations and reviews, as everywhere in this course, but write the code yourself. The point of the capstone is that you can explain and change every line under interview pressure, and the live drill will show whether you can.

## How it's judged

Use this as a self-review, then ask a peer or mentor to score it too.

| Area | Strong | Weak |
|---|---|---|
| Real problem | A named user, their quote, and a change they asked for that you made | A hypothetical user; no feedback |
| Process | Every feature has an issue and a small PR with a clear description; the board is current | A few huge commits straight to `main` |
| Correctness | Tests for the rules and the API, including error and permission cases; CI green | Happy-path tests only, or none in CI |
| Security | Hashed passwords, parameterised SQL, authorisation tested, no secrets in history | Plain-text passwords; users can read each other's data |
| Operations | Live, `/health`, JSON logs with request IDs, a rollback you actually tried | Only runs on your laptop |
| Design | The doc and ADRs explain trade-offs and what you'd revisit | A list of technologies |
| Communication | README and demo make the value clear in under a minute | A reader has to run the code to find out what it does |
| Ownership | You can add a small feature live in 30 minutes and explain every line | You can't explain parts of your own code |

## Common pitfalls

- **Building for months before the first user test.** Put something in front of your user by week 4 at the latest. Their first five minutes will reshape your plan.
- **Scope creep.** New ideas go into `docs/next.md`, not into this week.
- **Skipping authorisation tests.** "User A can't see user B's data" is the bug interviewers most like to ask about. Test it.
- **A README written last.** Write the top section in week 1 and keep it true as you go.
