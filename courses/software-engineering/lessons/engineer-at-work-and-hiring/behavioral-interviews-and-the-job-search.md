# Behavioral interviews and the job search

## Why this matters

Almost every interview process includes a **behavioral** round: "Tell me about a time when…". Juniors often treat it as small talk and lose offers they'd earned in the coding rounds. Then there's the search itself: where to apply, how to get noticed, what to do with an offer, and how to keep going after rejections. Nobody teaches this, and it decides whether all your work turns into a job.

## Behavioral interviews: what they test

Behavioral questions assume that **how you acted before predicts how you'll act again**. So the interviewer wants real stories, not opinions. "I'm a great team player" is an opinion. "When my teammate and I disagreed about the database schema, I…" is evidence.

Typical questions:

- Tell me about a time you disagreed with someone. (**conflict**)
- Tell me about a mistake you made. (**failure**)
- Tell me about something you had to learn quickly. (**learning fast**)
- Tell me about something you took responsibility for without being asked. (**ownership**)
- Tell me about working in a team. (**teamwork**)
- Tell me about the hardest bug you've fixed. (**technical problem**)

### The STAR method

Structure every answer as **STAR**:

```
 S  Situation   Where and when? One or two sentences of context.
 T  Task        What was your goal or responsibility?
 A  Action      What did YOU do, step by step?   ← most of the answer
 R  Result      What happened? Numbers if you have them. What you learned.
```

Here's a weak answer to "Tell me about a hard bug":

```
We had a lot of bugs in our project and we all worked really hard as a
team to fix them, and in the end it was fine.
```

No specific situation, "we" everywhere so the interviewer can't see what *you* did, and the result is "it was fine". Here's the same experience told with STAR:

```
S  In my expense-tracker project, monthly totals were wrong for some
   users, but only near the end of the month.
T  I needed to find out why and make sure it couldn't come back.
A  I wrote a failing test with an expense at 23:30 on the 31st. It
   failed, so I knew the bug was in date handling. Stepping through in
   the debugger, I saw I was storing local time but grouping by UTC
   month, so late-evening expenses landed in the next month. I switched
   to storing UTC everywhere and converting only for display.
R  The test passed, I added two more edge-case tests, and the totals
   have been correct since. I now store timestamps in UTC by default.
```

It's specific, it's about your actions, and it ends with a result and a lesson. Aim for about two minutes per answer.

### Prepare six stories

You don't need a story for every possible question. Prepare **six** good stories, one per theme above, and adapt them. Most questions map onto one of them. Your stories can come from this course's projects, the capstone, previous jobs (even non-tech ones), volunteering or study.

Write them down in STAR form, then practise saying them out loud until they're natural, not memorised word for word. A simple way to keep them:

```python
stories = {
    "conflict": "Disagreed with teammate on schema in capstone...",
    "failure": "Deployed without a migration, broke the demo...",
    "hard bug": "Expense totals wrong at month end (UTC vs local)...",
}
question_theme = "hard bug"
print(stories[question_theme][:40])
# Expense totals wrong at month end (UTC v
```

### Failure questions

"Tell me about a mistake" makes people nervous. Interviewers aren't looking for someone who never fails; they want someone who **owns** mistakes and **learns** from them. Pick a real mistake with real consequences (not "I work too hard"), describe what you did to fix it, and spend the most time on what you changed afterwards.

### Questions you ask

At the end you'll be asked "Do you have any questions for us?" Always have two or three. Good ones show you're thinking about doing the job well:

- "What does a new junior engineer work on in their first month?"
- "How does code review work on the team?"
- "How do juniors get support and feedback here?"

## Researching the company

Before any interview, spend 30 minutes on: what the product does and who pays for it, what the team you'd join works on, any recent news, and the engineering blog if they have one. Use the product if you can. "I tried your app and noticed…" is a strong way to open a conversation, and you'll have a real answer to "Why do you want to work here?"

## Where juniors actually get hired

Mass-applying to every job ad with the same resume has a low success rate. The channels that work better for juniors:

- **Internships and apprenticeships.** Many companies hire most of their juniors from these. Look for apprenticeship programmes aimed at career changers too.
- **Referrals.** An employee recommending you puts your application in front of a person. Referrals come from relationships, not from asking strangers.
- **Personal outreach** to engineers and hiring managers (see below).
- **Local and smaller companies.** Less competition than famous brands, and you often get broader experience.
- **Open source.** A merged PR to a project a company uses is a conversation starter with that company's engineers.
- **Communities and meetups.** Local Python meetups, online communities, hackathons. Show up repeatedly and help others.

### Outreach that gets replies

A cold message works when it's **short, specific, personal**, and makes a **small ask**:

```
Hi Sam, I read your post on moving your team's background jobs to a
queue. I built something similar in my expense-tracker API (link).
Could I ask you two questions about how your team onboards juniors?
15 minutes whenever suits.
```

It shows you know their work, links one relevant project, and asks for 15 minutes, not a job. Compare "Can you refer me? Here's my resume", a big ask from a stranger. If the conversation goes well, they may offer to refer you; you rarely need to ask.

### Track everything

Treat the search like a project. Keep a tracker, a spreadsheet is fine, with: company, role, link, date applied, channel (ad, referral, outreach), contact person, status and next step.

```python
apps = [
    {"company": "A", "channel": "ad", "status": "rejected"},
    {"company": "B", "channel": "referral", "status": "interview"},
    {"company": "C", "channel": "ad", "status": "no reply"},
    {"company": "D", "channel": "outreach", "status": "interview"},
]
for channel in ("ad", "referral", "outreach"):
    sent = [a for a in apps if a["channel"] == channel]
    got = [a for a in sent if a["status"] == "interview"]
    print(channel, f"{len(got)}/{len(sent)} interviews")
# ad 0/2 interviews
# referral 1/1 interviews
# outreach 1/1 interviews
```

After a few weeks, your own numbers tell you which channels are worth your time.

## Take-home tasks

Some companies send a **take-home**: a small project to build in a few hours or days. Treat it like a real pull request:

- Read the brief twice and ask questions if anything is unclear.
- Respect the time limit they give; say what you'd do with more time.
- Include tests, a README with how to run it, and a short note on your decisions and trade-offs.
- Keep commits clean.

Expect to discuss it afterwards ("Why did you do it this way? How would you add X?"). If you used AI tools, follow their stated rules and be ready to explain every line.

## Offers and negotiation basics

When you get an offer:

- **Say thank you, and ask for it in writing**, with salary, start date, benefits and any probation period.
- **You can usually take a few days** to decide. Ask for a specific date.
- **Research the range** for the role and location (salary surveys, job ads that list pay, people you know).
- **Asking politely is normal.** "Thank you, I'm excited about this. Based on my research for this role, I was hoping for something closer to X. Is there flexibility?" The worst usual answer is "no". Juniors often have less room on salary, but sometimes there's flexibility on start date, equipment, learning budget or remote days.
- **Don't accept and keep interviewing elsewhere.** Once you've said yes, withdraw from other processes.

## Handling rejection

You will be rejected, probably many times. Everyone is, including people who are now senior engineers. A rejection often reflects things you can't see: an internal candidate, a budget change, someone with one more year of experience.

- **Ask for feedback.** Many companies won't give it, but some will, and it's gold.
- **Review each interview** within a day: what went well, what you'd do differently. Add missed coding problems to your mistakes log.
- **Keep the pipeline full.** Don't stop applying while waiting on one company you love.
- **Keep building.** Shipping a feature or contributing to open source during the search gives you new stories and keeps your skills sharp.
- **Look after yourself.** Set a weekly target (applications, outreach messages, practice problems) and stop when you hit it.

## Common mistakes

- **"We" in every story.** The interviewer is hiring you. Say "I" for what you did.
- **Long situation, tiny action.** Keep S and T short; spend most of the time on A.
- **No result**, or a vague one. End with what happened and what you learned.
- **Fake weaknesses** ("I'm a perfectionist"). Use a real mistake and show the learning.
- **No questions for them.** Prepare two or three.
- **Mass-applying with one generic resume** and no outreach. Target fewer roles and personalise.
- **Accepting the first number without a word.** A polite question is normal.
- **Treating rejection as a verdict.** It's data. Review, adjust, keep going.

## Recap

- Behavioral rounds look for evidence of how you've acted. Answer with **STAR**: short situation and task, detailed action, clear result.
- Prepare six stories: conflict, failure, learning fast, ownership, teamwork, a hard bug. Practise them out loud.
- Research the company and prepare your own questions.
- Juniors get hired through internships, apprenticeships, referrals, short personal outreach, smaller companies, open source and communities.
- Track every application and learn which channels work for you.
- Treat take-homes like a real PR. Get offers in writing, research the range, and ask politely.
- Rejection is normal. Review, adjust, keep the pipeline full, and keep building.
