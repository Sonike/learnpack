# Job-ready packet

Everything a hiring manager needs to say yes, in one place: a resume, a portfolio that proves your skills, stories for the behavioral round, interview practice, one open source contribution and a running job search. This isn't a project you finish and forget. It's the toolkit you'll use every week until you get the offer.

Keep it all in one private GitHub repo (for example `job-search`) except the parts that must be public (your profile README and portfolio repos). Paste the links below as you go.

## What to build

### 1. A one-page resume

- Use Jake's resume template or a similarly plain, single-column layout. Export to PDF.
- Projects section with your **three strongest projects**: the capstone and two section projects (the REST API you shipped is a good candidate).
- Every bullet starts with an action verb and has a number. Run each bullet through your `score_resume_bullet` function from the lesson "Portfolio, GitHub and resume" and fix every flag.
- Have one other person read it for 30 seconds and tell you what they remember. If it isn't what you wanted, rewrite.

### 2. A GitHub profile that sells

- A profile README (repo named after your username): who you are, what you build, how to contact you.
- Pin your **3 best repos**. Each one's README has: one-sentence purpose, demo link or GIF, setup steps that work on a fresh clone, how to run the tests, and two design decisions.
- Archive or make private anything you don't want judged.

### 3. Six STAR stories

In `stories.md`, write one story for each theme: **conflict, failure, learning fast, ownership, teamwork, a hard bug**. Use Situation / Task / Action / Result headings. Keep S and T to one or two sentences each; most of the words go in Action. Then say each one out loud, timed, and trim any over about two minutes.

### 4. Two mock coding interviews

Do two mock interviews, with a peer playing interviewer (another learner, a friend who codes) or by recording yourself on a problem you haven't seen. Use a 35-minute timer and the seven steps from the lesson "Coding interviews". Afterwards, write a self-review in `mocks.md`:

```
Problem:         ...
Pattern:         ...
Solved?          yes / brute force only / no
Did I clarify?   ...
Where I went quiet or stuck:  ...
What I'd do differently:     ...
```

### 5. One open source contribution

Find a project you use, read its `CONTRIBUTING.md`, and open one pull request: a docs fix, a test, or a "good first issue". Comment on the issue before starting. It doesn't have to be merged by the time you finish, but it must be a real PR that follows the project's rules.

### 6. A running application tracker

A spreadsheet (or CSV in the repo) with columns: company, role, link, date, channel (ad / referral / outreach / other), contact, status, next step, notes. Reach **20 targeted applications** (each with a tailored resume) and **10 personal outreach messages** to engineers or hiring managers, written in the short, specific, small-ask style from the lesson. After four weeks, compute your interview rate per channel and write two sentences on what you'll change.

## How it's judged

A reviewer (a mentor, peer or you, honestly) should be able to answer yes to:

- Would a recruiter understand what you've built in 30 seconds from the resume?
- Can a stranger clone each pinned repo and run its tests by following the README?
- Does each STAR story make clear what **you** did and what the result was?
- Do the mock reviews show specific things to improve, and are they in your mistakes log?
- Does the open source PR follow the project's contribution rules?
- Is the tracker up to date, with a next step for every live application?

> **Note:** AI tools can help here the way a good friend would: ask one to critique a bullet, play an interviewer, or point out vague parts of a story. Write the words yourself. Interviewers will ask about everything on your resume and in your stories, and they'll notice if it doesn't sound like you.
