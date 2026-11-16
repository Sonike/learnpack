# GitHub, remotes and pull requests

Git on your laptop keeps your history safe from your own mistakes. **GitHub** puts that history online, where it's backed up, where your teammates can get it, and where code gets **reviewed** before it becomes part of the product. The **pull request** is the centre of daily work on almost every software team: it's where you propose a change, discuss it, and get it approved. It's also where employers will look at how you work.

## Git versus GitHub

They're easy to confuse:

- **Git** is the version control tool. It runs on your computer and works fine with no internet.
- **GitHub** is a website that hosts Git repositories and adds collaboration on top: pull requests, code review, issues, and automation (CI). GitLab and Bitbucket are similar services; the ideas transfer.

## Remotes

A **remote** is another copy of your repository, usually on a server like GitHub, that you can send commits to and get commits from. By convention, the main remote is called **`origin`**.

### Cloning an existing repository

To get a copy of a project that's already on GitHub, **clone** it:

```bash
$ git clone https://github.com/octocat/Hello-World.git
Cloning into 'Hello-World'...
remote: Enumerating objects: 13, done.
Receiving objects: 100% (13/13), done.
$ cd Hello-World
$ git remote -v
origin	https://github.com/octocat/Hello-World.git (fetch)
origin	https://github.com/octocat/Hello-World.git (push)
```

`git clone` downloads the **whole history**, sets up `origin` pointing at the URL, and checks out the default branch.

### Connecting a project you started locally

If you began with `git init` on your machine, create an empty repository on GitHub (the "New repository" button; don't tick "Add a README", so it's truly empty), then connect and upload:

```bash
$ git remote add origin https://github.com/ada/greeter.git
$ git push -u origin main
Enumerating objects: 6, done.
Writing objects: 100% (6/6), 520 bytes | 520.00 KiB/s, done.
To https://github.com/ada/greeter.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

`-u` (short for `--set-upstream`) links your local `main` with `origin/main`, so from now on plain `git push` and `git pull` know where to go.

## push, fetch and pull

Your local repository and GitHub's copy are separate. Nothing syncs automatically; you move commits explicitly.

```
   your laptop                              GitHub
 +--------------+        git push       +--------------+
 |  main        |  -------------------> |  main        |
 |              |  <------------------- |              |
 +--------------+   git fetch / pull    +--------------+
```

- **`git push`** sends your new commits to the remote.
- **`git fetch`** downloads new commits from the remote **without changing your files or your branches**. It updates **remote-tracking branches** like `origin/main`: your local record of where `main` was on GitHub the last time you checked.
- **`git pull`** is **`git fetch` followed by `git merge`**: it downloads the new commits and merges `origin/main` into your current branch.

### When push is rejected

If a teammate pushed to `main` after your last pull, GitHub has commits you don't. Pushing would throw theirs away, so Git refuses:

```bash
$ git push
To https://github.com/ada/greeter.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/ada/greeter.git'
hint: Updates were rejected because the remote contains work that you do not
hint: have locally. This is usually caused by another repository pushing to
hint: the same ref. If you want to integrate the remote changes, use
hint: 'git pull' before pushing again.
```

This is Git protecting your teammate's work. The fix is in the hint: `git pull` (resolving any conflicts, as in "Branches and merging"), run the tests, then `git push` again. Do **not** reach for `git push --force`; that overwrites the remote with your version and deletes their commits from the branch.

## Authenticating: SSH keys or HTTPS tokens

GitHub needs to know it's really you before accepting a push. Your account password doesn't work for Git operations. There are two options:

- **HTTPS with a personal access token** (or a credential helper like the GitHub CLI's `gh auth login`, which handles the token for you). The URL looks like `https://github.com/ada/greeter.git`.
- **SSH keys.** You generate a key pair on your computer (`ssh-keygen -t ed25519`), add the **public** key to your GitHub settings, and use URLs like `git@github.com:ada/greeter.git`. The **private** key never leaves your machine.

Either works; GitHub's docs walk through both. Whichever you choose, **treat tokens and private keys like passwords**: never paste them into code, chat, a commit, an issue, or an AI tool. A token in a public repository is usually found by automated scanners within minutes. If one leaks, revoke it in GitHub's settings straight away and make a new one.

## Forks

A **fork** is your own copy of someone else's repository, on GitHub, under your account. You fork when you want to contribute to a project you can't push to, such as an open-source library.

It's easy to mix up three related ideas:

| | Where the copy lives | What it's for |
|---|---|---|
| **Clone** | Your computer | Working on a repository locally |
| **Fork** | GitHub, under your account | Getting a copy of someone else's project you can push to |
| **Branch** | Inside one repository | A separate line of work within the same project |

The open-source flow is: fork on GitHub → clone **your fork** → create a branch → commit → push to your fork → open a pull request back to the original project. On a team where you have push access to the shared repository, you skip the fork and just push branches.

## Pull requests

A **pull request** (PR; GitLab calls it a merge request) says: "here's a branch with changes; please review them and merge them into `main`". It shows the diff, runs automated checks, and gives reviewers a place to comment on specific lines.

The everyday flow:

```bash
$ git switch main
$ git pull                               # start from the latest main
$ git switch -c fix-empty-cart-total     # one branch per change
# ... edit, test, commit (maybe several commits) ...
$ git push -u origin fix-empty-cart-total
remote: Create a pull request for 'fix-empty-cart-total' on GitHub by visiting:
remote:      https://github.com/ada/shop/pull/new/fix-empty-cart-total
```

Open that link (or click the "Compare & pull request" banner GitHub shows), choose the base branch (`main`), write a title and description, and create the PR. Then:

1. **Reviewers read the diff** and leave comments: questions, suggestions, problems.
2. **You respond.** Reply to each comment, push more commits to the same branch to address them (the PR updates automatically), and re-request review.
3. **Automated checks run** (the lesson "Team workflow, issues and CI" covers these).
4. **Someone approves and merges.** The branch is usually deleted afterwards.

Keep PRs **small**. A 50-line PR gets a careful review within hours. A 2,000-line PR gets a skim, a "looks good to me", and bugs. Many teams aim for under about 400 changed lines.

### A PR description reviewers love

The description is where you do the reviewer's thinking for them. A good template:

```markdown
## What
Return 0.00 instead of crashing when the cart is empty.

## Why
Checkout crashed with ZeroDivisionError for users who removed every item.
Closes #87.

## How to test
1. `pytest tests/test_cart.py`
2. Add one item to the cart, remove it, open checkout: the total shows 0.00.

## Notes
I kept the shipping logic unchanged; it's covered by #90.
```

- **What** changed, in a sentence or two.
- **Why**: the problem it solves, with a link to the issue. `Closes #87` (or `Fixes #87`) also tells GitHub to close issue 87 automatically when the PR is merged.
- **How to test**: exact steps, so the reviewer can check your claim in two minutes.
- Screenshots for anything visual, and notes on anything you're unsure about.

You'll write a checker for these sections in the practice.

### Being reviewed (and reviewing)

Code review is about the code, not about you. Every engineer, at every level, gets comments on their PRs. Thank people, ask when a comment isn't clear, push back politely when you disagree and explain why, and never take it personally.

When you review, be specific and kind: "This loop runs once per item and queries the database each time; could we fetch them all at once?" beats "This is slow." Ask questions rather than issuing orders, and say what's good too.

> **Note:** it's fine to ask an AI assistant to review your PR before a human sees it, the same way you'd run the tests. But you must be able to explain every line yourself: reviewers will ask, and so will interviewers.

## Common mistakes

**Pushing to the wrong place.** `git push` with no upstream gives `fatal: The current branch fix-x has no upstream branch.` Git prints the exact command to fix it: `git push --set-upstream origin fix-x`.

**Working on an old `main`.** You branch from a `main` you last pulled a week ago, and your PR is full of conflicts. Always `git pull` on `main` before creating a branch.

**Force-pushing to fix a rejected push.** It deletes your teammates' commits from the remote branch. Pull, merge, push.

**Pasting tokens.** A token in a script, a screenshot or a chat message is a leaked token. Revoke it.

**One giant PR for a week of work.** Split it: one PR per logical change.

## Recap

- Git is the tool; GitHub hosts repositories and adds pull requests, review, issues and CI.
- A **remote** is another copy of the repository; `origin` is the usual name. `git clone` copies a remote repository with its full history.
- `git push` sends commits; `git fetch` downloads without merging; `git pull` = fetch + merge. A rejected push means the remote has new commits: pull first, never force.
- Authenticate with SSH keys or HTTPS tokens, and never paste them anywhere.
- **Clone** = local copy, **fork** = your GitHub copy of someone else's repo, **branch** = a line of work inside one repo.
- A pull request proposes a branch for review. Keep PRs small, and describe **What**, **Why** (with `Closes #N`) and **How to test**.
