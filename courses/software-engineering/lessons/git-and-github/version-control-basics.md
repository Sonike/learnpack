# Version control basics

Every software team in the world uses version control, and almost all of them use **Git**. It's how you save your work in meaningful steps, go back when something breaks, see who changed what and why, and work on the same code as other people without overwriting each other. On your first day at a job you'll be expected to use it, and your GitHub profile, built on Git, is a big part of how employers will judge your projects.

## Why version control?

Without it, people end up with folders like this:

```
essay.docx
essay_v2.docx
essay_v2_final.docx
essay_v2_final_REALLY_final.docx
essay_v2_final_fixed_by_sam.docx
```

Which one is current? What changed between them? What if Sam and you both edited `v2` at the same time? Version control replaces this mess with one folder and a complete, labelled history of every change.

A **version control system** records changes to a set of files over time so you can recall any earlier version. Git is the one you'll use. It's **distributed**: every copy of a project contains the full history, so you can work offline and nothing depends on a single server.

## The three areas

This is the most important idea in Git, and the one that confuses beginners most. A Git project has three places a version of your file can be:

```
 working tree          staging area            repository
 (your files)          (the "index")           (the history)
 +-----------+  git add  +-----------+  git commit  +-----------+
 | edit here | --------> | next      | -----------> | saved     |
 |           |           | snapshot  |              | snapshots |
 +-----------+           +-----------+              +-----------+
```

- The **working tree** is the files on your disk, the ones you edit in VS Code.
- The **staging area** (also called the **index**) is where you put together the next snapshot. You choose exactly which changes go into it.
- The **repository** (or **repo**) is the history: every snapshot you've committed, stored in a hidden `.git` folder inside your project.

A **commit** is a saved snapshot of the staged files, plus a message saying what changed and why, your name, and the time. Git stores commits as complete snapshots of the project (efficiently: unchanged files aren't stored twice), and each commit points to the one before it, its **parent**. That chain of commits is your history.

Why have a staging area at all? Because you often change several things at once, but they belong in different commits. Maybe you fixed a bug *and* reworded the README. Staging lets you commit the bug fix on its own, with its own message, then the README change separately.

## Your first repository

First, tell Git who you are (once per computer). This name and email appear on every commit you make:

```bash
$ git config --global user.name "Ada Lovelace"
$ git config --global user.email "ada@example.com"
```

Now create a project and turn it into a repository with `git init`:

```bash
$ mkdir greeter && cd greeter
$ git init
Initialized empty Git repository in /home/ada/greeter/.git/
```

That `.git` folder is the repository. Don't edit anything inside it by hand. Delete it and the history is gone; your files stay.

### git status: where am I?

`git status` tells you the state of all three areas. Run it constantly; it's the command you'll type most.

```bash
$ echo 'print("Hello!")' > hello.py
$ git status
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	hello.py

nothing added to commit but untracked files present (use "git add" to track)
```

**Untracked** means Git sees the file but has never been told to follow it. Notice that `git status` even tells you what to do next. Read its output; it's helpful.

> **Note:** if your first branch is called `master` instead of `main`, your Git is set to the old default. Run `git config --global init.defaultBranch main` before `git init` to use `main`, which GitHub and most teams use now.

### git add: stage changes

```bash
$ git add hello.py
$ git status
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   hello.py
```

`hello.py` is now in the staging area. `git add .` stages every change in the current folder; it's convenient, but check `git status` first so you don't stage something you didn't mean to.

### git commit: save the snapshot

```bash
$ git commit -m "Add greeting script"
[main (root-commit) 4f1c2ab] Add greeting script
 1 file changed, 1 insertion(+)
 create mode 100644 hello.py
```

`-m` gives the commit message inline. Without `-m`, Git opens a text editor for a longer message. `4f1c2ab` is the start of the commit's **hash**: a unique ID made from the commit's contents. Every commit has one, and you can use the first 7 characters to refer to it. (Writing good commit messages has its own lesson, "Good commits and undoing mistakes".)

### Modified files and git diff

Now change the file:

```bash
$ echo 'print("Goodbye!")' >> hello.py
$ git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   hello.py

no changes added to commit (use "git add" and/or "git commit -a")
```

`git diff` shows exactly what changed, line by line, between your working tree and the staging area:

```bash
$ git diff
diff --git a/hello.py b/hello.py
index 2b4d8a1..9e3f0c7 100644
--- a/hello.py
+++ b/hello.py
@@ -1 +1,2 @@
 print("Hello!")
+print("Goodbye!")
```

Lines starting with `+` were added, `-` were removed, and the rest are unchanged context. Once you've staged a change, plain `git diff` shows nothing for it; use `git diff --staged` to see what's about to be committed. Checking `git diff --staged` before every commit is a great habit: it catches debugging prints and accidental edits.

### git log: the history

```bash
$ git add hello.py
$ git commit -m "Say goodbye too"
[main 8d2e5f0] Say goodbye too
 1 file changed, 1 insertion(+)
$ git log --oneline
8d2e5f0 (HEAD -> main) Say goodbye too
4f1c2ab Add greeting script
```

Newest first. `HEAD` means "where you are now". Plain `git log` shows the full messages, authors and dates. `git show 4f1c2ab` shows a single commit and its changes.

### Staging only some changes

Here's why the staging area matters. Say you edit two files for two different reasons:

```bash
$ git status --short
 M hello.py
 M README.md
$ git add hello.py
$ git status --short
M  hello.py
 M README.md
```

`--short` gives one line per file with two status columns: the **left column is the staging area**, the **right column is the working tree**. `M ` (left) means staged; ` M` (right) means modified but not staged. Now `git commit` saves only `hello.py`. The scriptable version of this, `git status --porcelain`, uses the same two columns, and you'll parse it in the practice.

What if you stage a file and then edit it again?

```bash
$ git add hello.py
$ echo '# one more line' >> hello.py
$ git status --short
MM hello.py
```

`MM`: one version is staged, and a newer version is in your working tree. **The commit will contain the staged version, not your latest edit.** Run `git add` again to stage the newer one.

## .gitignore: what never to commit

Some files should never go into a repository:

- **`.venv/`**: your virtual environment. It's large, specific to your machine, and recreated from `requirements.txt` or `pyproject.toml`.
- **`__pycache__/`** and **`*.pyc`**: compiled files Python generates automatically.
- **Secrets**: `.env` files, API keys, passwords. Once a secret is pushed, assume it's compromised: people run bots that scan public repositories for keys within minutes, and deleting the file later doesn't remove it from the history. You'd have to revoke and replace the key.
- Editor and OS clutter: `.vscode/` (sometimes), `.DS_Store` on macOS.

List them in a file called `.gitignore` at the root of your project, and Git will pretend they don't exist:

```
# Python
__pycache__/
*.pyc
.venv/

# Secrets
.env

# OS
.DS_Store
```

- A line ending in `/` matches a folder.
- `*` is a wildcard: `*.pyc` matches every file ending in `.pyc`, in any folder.
- `#` starts a comment.
- `!` un-ignores: `*.log` then `!keep.log` ignores every log except `keep.log`. When patterns conflict, the **last** matching one wins.

Commit `.gitignore` itself, so everyone on the project shares it. GitHub has ready-made templates; its Python template is a good start.

> **Note:** `.gitignore` only affects untracked files. If you already committed `.venv`, adding it to `.gitignore` won't remove it. Run `git rm -r --cached .venv` (removes it from the repo, keeps it on disk), then commit.

## Common mistakes

**Running `git init` in the wrong folder**, like your home directory. Suddenly `git status` lists every file you own. Delete that `.git` folder (carefully: `rm -rf ~/.git`, only that one) and run `git init` inside the project folder.

**Forgetting to `git add` before committing.** `git commit` says `nothing added to commit` or commits only the old staged version. Check `git status` first.

**`fatal: not a git repository (or any of the parent directories): .git`.** You're not inside a repository. `cd` into your project folder, or run `git init` if it was never created.

**Committing secrets or `.venv`.** Set up `.gitignore` **before** your first commit.

**Giant "did stuff" commits.** One commit per logical change makes history useful. More on that in "Good commits and undoing mistakes".

## Recap

- Version control keeps a labelled history of every change. Git is distributed: every clone has the whole history.
- Three areas: **working tree** (your files), **staging area** (the next snapshot), **repository** (committed history).
- `git init` creates a repo; `git status` shows where everything is; `git add` stages; `git commit -m` saves a snapshot; `git diff` and `git diff --staged` show changes; `git log --oneline` shows history.
- In `git status --short`, the left column is the staging area and the right column is the working tree. A file can be both staged and modified.
- `.gitignore` keeps `.venv`, `__pycache__`, and secrets out of your repository. Set it up before your first commit.
