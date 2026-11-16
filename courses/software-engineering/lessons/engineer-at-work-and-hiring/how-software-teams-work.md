# How software teams work

## Why this matters

On your first day at a job, nobody hands you a blank file and says "build something". You get a **ticket** in a tracker, a teammate to ask questions, a standup at 9:30, and a pull request that two people will review. Most junior engineers who struggle early don't struggle with Python. They struggle with not knowing how the work flows: what "done" means, when to ask for help, and how to tell people what they're doing. This lesson is that missing manual.

## Who's on the team

A typical product team has five to ten people. The names vary between companies, but the jobs are the same:

```
            what to build and why           how it looks and feels
          ┌───────────────────────┐       ┌──────────────────────┐
          │   Product manager     │       │   Designer           │
          │   (PM)                │       │   (UX / UI)          │
          └──────────┬────────────┘       └──────────┬───────────┘
                     │        tickets, mockups       │
                     ▼                               ▼
          ┌──────────────────────────────────────────────────────┐
          │   Engineers  (you are here)                          │
          │   build it, test it, ship it, keep it running        │
          └──────────────────────────┬───────────────────────────┘
                                     │  builds to check
                                     ▼
          ┌──────────────────────────────────────────────────────┐
          │   QA / test engineers (on some teams)                │
          │   try to break it before customers do                │
          └──────────────────────────────────────────────────────┘
```

- The **product manager** decides *what* to build and *why*, based on what users and the business need. They own the priority order.
- The **designer** decides how it works for the user: screens, flows, wording.
- **Engineers** decide *how* to build it, then build, test, ship and run it. Often there's an **engineering manager** who looks after the people (your growth, hiring, workload) and a **tech lead** who looks after the technical direction.
- **QA** (quality assurance) engineers test the product. Many teams no longer have separate QA: engineers write automated tests and test their own work.

When something is unclear about *what* to build, ask the PM or designer. When it's unclear *how*, ask an engineer. Asking the right person saves everyone time.

## Tickets and user stories

All planned work lives in a **tracker** (Jira, Linear, GitHub Issues). Each piece of work is a **ticket** (also called an issue or a card). There are three common kinds:

- **Bug**: something is broken. A good bug ticket says what you did, what you expected, and what happened instead.
- **Task**: technical work, such as "upgrade FastAPI to the latest version".
- **User story**: a feature described from the user's point of view.

A **user story** has a fixed shape:

```
As a <role>, I want <goal> so that <benefit>.
```

For example:

```
As a library member, I want to renew a loan online so that I don't pay late fees.
```

Each part does a job. The **role** says who you're building for. The **goal** says what they want to do. The **benefit** says *why*, and the "why" is what lets you make good decisions when the ticket doesn't cover something. If renewing is about avoiding late fees, then a member with a loan that's *already* overdue probably matters too, and you should ask about it.

A story alone is too vague to build. It needs **acceptance criteria**: testable statements that say when the story is done. Many teams write them as **Given / When / Then**:

```
Given I have a book due tomorrow
When I click "Renew"
Then the due date moves forward 14 days
And I see a confirmation message
```

- **Given** is the starting situation.
- **When** is the action.
- **Then** is the result you can check.
- **And** adds another step to the line before it.

Notice how directly this maps to a test. "Given" is your setup, "When" is the call, "Then" is the assert. When you pick up a story, write those tests first and you know exactly when you're finished.

> **Try it:** In the exercise for this lesson you'll write `parse_user_story`, a checker that pulls the role, goal, benefit and criteria out of a ticket and lists what's missing. Teams use checks like this in "definition of ready" reviews.

### When is a ticket ready?

Before work starts, the team checks the ticket is **ready**: it has a clear story, acceptance criteria, any design attached, and no open questions. Here's a ticket that isn't:

```
Improve the search page.
```

Improve how? Faster? Better results? Prettier? You could spend a week and still not be done, because nobody agreed what done means. If you get a ticket like this, don't guess. Comment on it: "What should be different when this is finished? Is it speed, result quality or layout?"

## Breaking work down and estimating

Teams want to know roughly how long things will take, so they can plan and keep promises. Two common ways to estimate:

- **Story points**: a relative size (1, 2, 3, 5, 8, 13…) agreed by the team. A 2 is about twice a 1. Points measure *effort and uncertainty*, not hours.
- **T-shirt sizes**: S, M, L, XL. Rougher, used for early planning.

The more useful habit for you is **splitting**. A story that would take a week hides a lot of risk. Split it until each piece takes **under a day** and could be shipped and reviewed on its own:

```
Too big:   "Members can manage loans online"

Split:     1. List my current loans with due dates
           2. Renew one loan (if no one has reserved it)
           3. Show an error if renewal isn't allowed
           4. Email a confirmation after renewing
```

Each piece is small enough to review in one sitting, and if piece 4 slips, pieces 1–3 still ship. Good splits are **vertical**: each one delivers something a user can see, rather than "do all the database work" then "do all the API work".

## Scrum and Kanban

Most teams use one of two ways to organise the flow of tickets.

**Scrum** works in fixed **sprints**, usually two weeks:

```
 Sprint planning ──► two weeks of work + daily standups ──► Review ──► Retro
 (pick tickets)                                            (demo)    (improve
                                                                      the process)
```

At **sprint planning**, the team picks the top tickets from the **backlog** (the ordered list of everything waiting). At the end there's a **review** (show what you built) and a **retrospective** or **retro** (what went well, what didn't, what we'll change).

**Kanban** has no sprints. Tickets flow across a board, and the team limits how many can be "in progress" at once so work finishes instead of piling up:

```
 To do        In progress (max 3)     In review       Done
 ───────      ───────────────────     ─────────       ────
 [#41]        [#37] you               [#35]           [#30]
 [#42]        [#38] Ana                               [#31]
 [#43]
```

You don't need to pick a favourite. Learn the words, and follow whatever your team does.

## Standups and updates

The **daily standup** is a short meeting, about 15 minutes, often standing to keep it short. Each person answers roughly:

1. What did I finish yesterday?
2. What am I doing today?
3. Is anything **blocking** me?

The third question is the important one. A standup isn't a status report to your manager; it's how blockers get noticed the same day. "I'm blocked on the payments test environment, does anyone know who owns it?" is the best thing you can say in a standup. Detailed problem-solving happens *after* the meeting, with only the people who need to be there.

Written updates follow the same idea. A good update on a ticket or in a team channel is short and specific:

```
Renew-loan (#38): renewal works and is tested. Blocked on one question:
should members with an overdue book be allowed to renew? Asked Priya
(PM) in the ticket. Meanwhile I'm starting the error message (#39).
```

It says where things stand, what's blocking, who you asked, and what you're doing while you wait.

## Definition of done

Teams agree on a **definition of done**: a checklist every ticket meets before it counts as finished. A typical one:

```
[ ] Acceptance criteria met
[ ] Tests written and passing in CI
[ ] Code reviewed and approved
[ ] Docs or README updated if behaviour changed
[ ] Deployed (or merged, ready to deploy)
```

"It works on my machine" is not done. "I pushed it" is not done. Done means someone else could rely on it.

## Asking for help: the 30-minute rule

New engineers usually make one of two mistakes. Some ask immediately, before trying anything, and never build the skill of getting unstuck. Others struggle silently for two days because they don't want to look slow. The second is worse: the team loses two days, and you look slower than if you'd asked.

A common rule is: **try on your own for about 30 minutes, then ask.** When you ask, show your work:

```
I'm trying to run the tests locally and get
"ModuleNotFoundError: No module named 'app'".
I've activated the venv and run pip install -r requirements.txt.
I also tried running from the repo root. Is there a step I'm missing?
```

This tells the helper what you're trying, the exact error, and what you've ruled out. Most questions like this get answered in a minute. And when the answer was missing from the README, add it: that's a great first pull request.

## Common mistakes

- **Starting a vague ticket without asking.** You build the wrong thing, and it's your time that's wasted. Ask on the ticket, in writing, so the answer is recorded.
- **One giant pull request at the end.** Split the work and open small PRs as you go. Reviewers can't review 2,000 lines well, and you get feedback too late to change course.
- **Using standup to explain every detail.** Say the headline and the blocker. Offer to talk afterwards.
- **Going quiet when stuck.** Silence looks worse than a question. Use the 30-minute rule.
- **"Done" means "the code is written".** Check the definition of done: tests, review, docs, deploy.
- **Estimating in hours as promises.** Estimates are guesses. When you learn something that changes yours, say so early: "This is bigger than we thought because X; I'd split it like this."

## Recap

- Teams have product managers (what and why), designers (how it feels), engineers (how it's built and run) and sometimes QA.
- Work lives in tickets. A user story says **As a** role, **I want** goal, **so that** benefit, and acceptance criteria in **Given / When / Then** say when it's done.
- A ticket is **ready** when nobody has to guess. If it isn't, ask on the ticket.
- Split work into vertical pieces under a day. Estimates are guesses; update them when you learn more.
- Scrum works in sprints with planning, review and retro; Kanban is a continuous flow with limits on work in progress.
- Standups exist to surface **blockers**. Updates say status, blocker, who you asked and what's next.
- Try for about 30 minutes, then ask, showing what you tried.
