# Capstone B: Build with a team

> **Note:** This capstone is **optional** if you've done Capstone A, or you can choose it instead. It needs **2–4 other learners**, and takes about 40–60 hours each over 5–6 weeks. If you can't find a team, do Capstone A and contribute to an open-source project for the teamwork practice.

## The goal

Build and ship a small application **as a team**, the way a real software team works: a shared backlog of user stories, estimated and split; branch protection with required reviews and CI; every member merging their own PRs and reviewing other people's; design discussions recorded as decisions; and a retrospective at the end. The product itself can be modest. The evidence of how you worked together is the point.

## Why it impresses

Most junior candidates have only ever worked alone. A team project gives you what a solo project can't:

- **Proof you can collaborate through Git**: merge conflicts resolved, reviews given and received, PRs changed in response to feedback. All of it is visible in the repository's history.
- **Real behavioural-interview stories.** "Tell me about a disagreement with a teammate" and "tell me about a time you had to change plans" are standard questions. After this project you'll have true answers with details, and each member writes one up as a STAR story.
- **Experience of the team rituals** from the lesson How software teams work: backlog, estimates, standups, definition of done, retros. You'll recognise them on day one of a job.

## Forming the team

- **Size:** 3–5 people in total. Two is a pair, not a team; more than five spends most of its time coordinating.
- **Overlap in time zones and hours** matters more than skill level. Agree on at least two shared hours a week for a call.
- **Write a one-page team agreement** in the first meeting and commit it as `TEAM.md`: how you communicate (one chat channel), when you meet, how fast you aim to review PRs (for example within 24 hours), what "done" means, and what happens if someone goes quiet.
- **Rotate roles** every week or two: one person facilitates the meetings, one keeps the board tidy. Everyone writes code and everyone reviews.

## Choosing the product

Pick something with clearly separate parts, so people can work in parallel without constantly editing the same files. A real user (as in Capstone A) is a bonus, not a requirement. Shapes that split well:

```
- Club events:      events + RSVPs + reminders + admin reports
- Study group hub:  groups + sessions + shared resources + attendance
- Small shop stock: products + stock movements + low-stock alerts + reports
- Book exchange:    listings + requests + handover tracking + ratings
```

Each line has four areas, so a team of four can each own one while sharing the database schema and API conventions.

## Scope

**In scope**
- The same technical bar as Capstone A: FastAPI, SQLite or Postgres with plain SQL, tests (unit and integration) in CI, auth with authorisation tests, config from the environment, JSON logs, `/health`, a live deploy.
- A shared repository with **branch protection on `main`**: at least one approving review and passing CI required to merge, no direct pushes.
- A **backlog** of user stories with acceptance criteria, estimated (t-shirt sizes or points), and split until each is about a day of work.
- A project board that matches reality.

**Out of scope**
- Everyone working on everything. Ownership areas keep the team moving.
- Long-lived branches. Merge small PRs often; a branch older than three days is a warning sign.
- A big-bang integration at the end.

## Milestones

```
Week 1  Team and plan
        - TEAM.md agreement; roles for the first week
        - Product chosen; 15–25 user stories with acceptance criteria
        - Stories estimated and split; first week's stories picked
        - Repo: branch protection, CI (ruff + pytest), PR template, CODEOWNERS optional
        - Shared conventions: API error format, naming, folder layout

Week 2  Walking skeleton
        - One thin slice through every layer, end to end, deployed:
          one table, one endpoint, one test, CI, live URL, /health
        - Every member merges at least one PR

Week 3  Features in parallel
        - Each member owns an area; PRs under ~300 changed lines
        - Two short standups a week (async in chat is fine)
        - First design discussion recorded as a decision note

Week 4  Integrate and harden
        - Auth and authorisation across all areas, with tests
        - JSON logging, error handling, coverage in CI
        - Mid-project retro: one change to how you work, then try it

Week 5  Finish and ship
        - Bug bash: everyone tests someone else's area and files issues
        - Fix, document, final deploy, rollback drill

Week 6  Wrap up
        - Final retro document
        - README with each member's contributions (links to their PRs and reviews)
        - Each member writes a STAR story from the project
        - Optional: 5-minute team demo video
```

## Deliverables

- **Repository** with protected `main`, CI, tests, `TEAM.md`, and a README that leads with what the product does, the live URL and a screenshot, then lists each member with links to PRs they authored and reviewed.
- **Backlog and board**: user stories as issues with acceptance criteria and estimates; closed issues linked to the PRs that closed them.
- **At least one decision note** (`docs/decisions/0001-*.md`) recording a real design discussion: the options people argued for, what you chose, and why.
- **Retro document** (`docs/retro.md`): what went well, what didn't, what you changed mid-project and whether it helped. Be specific: "PRs waited two days for review; we added a rule to review before starting new work; wait time fell to under a day."
- **Live deploy** with `/health`, logs and a tested rollback, as in Capstone A.
- **One STAR story per member**, kept in each person's own notes (not necessarily in the repo).

## How reviews should work

Use what you learned in the lesson Code review:

- Authors review their own diff first and write a PR description that says **why**, how it was tested, and what to look at.
- Reviewers label comments (`nit:`, `question:`, `blocking:`), stay specific and kind, and approve when the code improves the codebase, not when it's perfect.
- Disagreements longer than two rounds of comments move to a call, and the outcome is written back into the PR.
- Nobody merges their own PR without an approval, including the person who set up the repo.

## How it's judged

| Area | Strong | Weak |
|---|---|---|
| Collaboration | Every member has merged PRs and given substantive reviews; links in the README | One person wrote most of the code |
| Planning | Stories with acceptance criteria, estimates and splits; the board matches reality | Vague tickets like "backend" |
| Git hygiene | Small PRs, conflicts resolved cleanly, no direct pushes to `main` | Week-long branches, force-pushes to `main` |
| Quality | Tests and CI as in Capstone A, including permission cases | Tests only in one person's area |
| Decisions | A decision note shows real options and a reason | Decisions lived only in a chat |
| Reflection | The retro names specific problems and a change you actually made | "Communication could be better" |
| Shipping | Live, logged, health-checked, rollback tried | Only runs on one laptop |

## Common pitfalls

- **One person carries the project.** It looks bad for everyone in the README. Use the ownership areas and check contribution links every week.
- **Big-bang integration.** The walking skeleton in week 2 exists to prevent this. Integrate every day.
- **Silent blockers.** Use the 30-minute rule from How software teams work: stuck for 30 minutes after a real attempt, ask in the team channel.
- **Arguing in PR comments for days.** Move it to a call, decide, and write the decision down.
- **No user stories, just tasks.** "Add table" isn't a story. Write who wants what and why, with criteria a reviewer can check.
