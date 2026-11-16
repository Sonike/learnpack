# Ship your capstone

This is the project that goes at the top of your resume and your GitHub profile. Pick **one** capstone:

- **Capstone A: A product someone actually uses.** You build and ship a small app for a real person or group, and get their feedback.
- **Capstone B: Build with a team.** You build and ship an app with 2–4 other learners, the way a software team works.

The full briefs, with milestones, deliverables and judging tables, are in the two capstone lessons. The second capstone is optional; if you have time after the first, the team project adds strong collaboration evidence to a solo portfolio.

## The shared bar

Whichever you choose, the finished project must have:

- A **FastAPI** backend with **SQLite or Postgres** through plain SQL and a repository layer.
- **Accounts and authorisation**, with tests proving one user can't read or change another user's data.
- **Tests** for the business rules and the API, running in **CI** on every push, with coverage reported.
- A **live deploy** with configuration from environment variables, structured JSON logs with redaction, a `/health` endpoint, and a rollback you've tried once.
- **Issues and pull requests for every feature** and a public project board.
- A **design doc** and **two decision notes** (ADRs) that explain trade-offs.
- A **README** that leads with what it is, who it's for, the live URL and a screenshot.
- A **3-minute demo video** and a short "what I'd do next" write-up.

Then the extra bar for your choice:

| Capstone A (real user) | Capstone B (team) |
|---|---|
| A named user (or their role) and their quote in the README | `TEAM.md` agreement; branch protection with required reviews |
| One change you made because of their feedback | A backlog of estimated, split user stories |
| The 30-minute live-extension drill, practised twice | Every member's PRs and reviews linked in the README |
| | A retro document and a STAR story per member |

## Before you call it done

Ask someone who hasn't seen the project to open the README and, within one minute, tell you what the app does and who it's for. Then give them the live URL. If either step confuses them, fix that before anything else: it's exactly what a recruiter or hiring manager will do.

> **Note:** keep the repository public and the deploy running while you job-hunt. A dead link on a resume costs you more than a missing project.
