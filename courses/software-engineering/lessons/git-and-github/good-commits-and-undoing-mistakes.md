# Good commits and undoing mistakes

A project's history is only as useful as its commits. Six months from now, someone (probably you) will run `git log` or `git blame` to understand why a line exists, and will find either "Handle empty carts at checkout: users who removed every item crashed the page" or "fix stuff". This lesson covers how to make commits worth reading, and then the other half of daily Git life: undoing mistakes safely. Everyone commits to the wrong branch or stages the wrong file sometimes. Knowing which undo command fits which situation turns a panic into a ten-second fix.

## Small, focused commits

A good commit does **one thing**: fixes one bug, adds one small feature, renames one concept. Why bother?

- **Review is easier.** A reviewer can follow a story of small steps.
- **Undoing is easier.** If one change turns out wrong, you can revert exactly that commit without losing everything else.
- **Bisecting works.** `git bisect` (from "Debugging systematically") finds the commit that broke something. That's only useful if the commit is small enough to point at the cause.

If you've made several unrelated changes, use the staging area to split them: `git add` one file, commit, then the next. `git add -p` goes further and lets you stage individual chunks within a file. (It's interactive, so try it in your own terminal.)

A useful rhythm: commit whenever you reach a small working state. The tests pass, the function does one more thing than before: commit.

## Writing commit messages

The most widely shared guide to this is Chris Beams' "How to Write a Git Commit Message" (in the resources). Its **seven rules**:

1. **Separate the subject from the body with a blank line.**
2. **Limit the subject line to 50 characters.**
3. **Capitalize the subject line.**
4. **Do not end the subject line with a period.**
5. **Use the imperative mood in the subject line.**
6. **Wrap the body at 72 characters.**
7. **Use the body to explain what and why, not how.**

Here's a message that follows them:

```
Return 0 for the total of an empty cart

Checkout crashed with ZeroDivisionError when a user removed every
item, because the average-price calculation divided by the item count.
Skip the average when the cart is empty and return a total of 0.

Closes #87
```

Rule by rule:

- **The subject is a summary** that shows up everywhere: `git log --oneline`, GitHub's commit list, PR titles. 50 characters keeps it readable in all of them (GitHub cuts subjects off at 72).
- **Imperative mood** means writing it as a command: "Add", "Fix", "Remove", not "Added", "Fixes" or "Fixing". The trick: a good subject completes the sentence *"If applied, this commit will ___"*. "If applied, this commit will **return 0 for the total of an empty cart**." It also matches Git's own messages, like "Merge branch 'x'".
- **The body explains why.** The diff already shows *how* the code changed. What it can't show is the problem you were solving, why you chose this approach, and what you considered. That's what future readers need.
- **The blank line** matters to tools: Git treats the first line as the subject, and many commands only show that.

Not every commit needs a body. "Fix typo in README" says it all. But any change whose reason isn't obvious deserves a few lines.

To write a multi-line message, run `git commit` without `-m` and Git opens your editor. Lines starting with `#` in that editor are comments and are dropped. (Setting VS Code as Git's editor: `git config --global core.editor "code --wait"`.)

Bad subjects, and better ones:

| Bad | Why | Better |
|---|---|---|
| `fixed bug` | Which bug? Past tense | `Fix crash when cart is empty` |
| `Updates` | Says nothing | `Update Python to 3.13 in CI` |
| `WIP` | Not a finished step | Commit when it works, or squash before merging |
| `Changed the login page so that the remember me checkbox works again.` | 70 characters, period, past tense | `Fix "remember me" on the login page` |

You'll write a checker for these rules in the practice, and use it on your own project's history.

## Undoing things: pick the right tool

Git has several undo commands, and they're easy to mix up. The key question is always: **where is the mistake?** In your working tree, in the staging area, in a commit only you have, or in a commit you've already pushed for others?

### Discard changes to a file: git restore

You edited a file and want to throw the edits away, back to the last committed (or staged) version:

```bash
$ git restore app.py
```

> **Note:** this **permanently** deletes your uncommitted edits to that file. There's no undo for uncommitted work, because Git never saw it.

### Unstage a file: git restore --staged

You ran `git add` on something you didn't mean to:

```bash
$ git restore --staged secrets.txt
```

The file goes back to "modified, not staged". Your edits are kept. (`git status` reminds you of both commands.)

### Fix the last commit: git commit --amend

Typo in the message you just wrote, or forgot to add a file?

```bash
$ git add forgotten_file.py
$ git commit --amend -m "Add CSV export for orders"
```

`--amend` replaces the last commit with a new one. Only do this **before you've pushed**; after that, others may have the old commit.

### Undo a commit you've already pushed: git revert

A commit on `main` turned out to break things, and everyone has already pulled it. Don't rewrite history. Instead, add a **new commit that does the opposite**:

```bash
$ git revert 8d2e5f0
[main c41a7b2] Revert "Say goodbye too"
 1 file changed, 1 deletion(-)
```

History now shows both the mistake and its reversal, which is honest and safe: nobody's copy is broken, because nothing was removed. **`revert` is the right undo for anything shared.**

### Move a branch back: git reset

`git reset` moves the current branch to an earlier commit, as if the later commits never happened. How it treats your files depends on a flag:

```bash
$ git reset --soft HEAD~1    # undo the commit; its changes stay staged
$ git reset HEAD~1           # undo the commit; its changes stay in your files, unstaged (the default, --mixed)
$ git reset --hard HEAD~1    # undo the commit AND throw away its changes
```

`HEAD~1` means "one commit before `HEAD`"; `HEAD~3` would be three back.

`reset` rewrites history, so it's only safe for commits **you haven't pushed**. `--soft` and the default are gentle: your work stays in your files. `--hard` deletes uncommitted work, so think twice before using it.

A classic use: you made two commits on `main` that should have been on a feature branch.

```bash
$ git switch -c feature-x      # new branch keeps the two commits
$ git switch main
$ git reset --hard HEAD~2      # move main back to before them
```

The commits are safe on `feature-x`; `main` is back where it was. (Only do this if those two commits weren't pushed.)

### Put work aside: git stash

You're halfway through something and need to switch branches to fix an urgent bug, but your work isn't ready to commit:

```bash
$ git stash
Saved working directory and index state WIP on main: 8d2e5f0 Say goodbye too
$ git switch hotfix
# ... fix, commit ...
$ git switch main
$ git stash pop
```

`git stash` saves your uncommitted changes on a stack and gives you a clean working tree; `git stash pop` brings them back. `git stash list` shows what's stored. Don't leave things in the stash for long; it's easy to forget them.

### Recover "lost" commits: git reflog

Ran `git reset --hard` and lost a commit you needed? It's almost certainly not gone. Git keeps a log of everywhere `HEAD` has pointed recently, called the **reflog**:

```bash
$ git reflog
c41a7b2 (HEAD -> main) HEAD@{0}: reset: moving to HEAD~1
9e7d3f1 HEAD@{1}: commit: Add CSV export for orders
8d2e5f0 HEAD@{2}: commit: Say goodbye too
$ git reset --hard 9e7d3f1
```

Find the commit before the mistake, and reset (or create a branch) back to it. Committed work is very hard to lose in Git. Uncommitted work is easy to lose, which is one more reason to commit often.

### Summary: which undo?

| Situation | Command | Safe after pushing? |
|---|---|---|
| Throw away edits to a file | `git restore <file>` | (not committed) |
| Unstage a file, keep edits | `git restore --staged <file>` | (not committed) |
| Fix the last commit's message or contents | `git commit --amend` | No |
| Undo a pushed commit | `git revert <hash>` | **Yes** |
| Undo local commits, keep the changes | `git reset HEAD~1` (or `--soft`) | No |
| Undo local commits and discard changes | `git reset --hard HEAD~1` | No |
| Set work aside to switch branches | `git stash`, later `git stash pop` | (not committed) |
| Find a commit you "lost" | `git reflog` | (local only) |

## Never force-push shared branches

After rewriting history (`reset`, `--amend`, rebase), a normal `git push` is rejected because your branch no longer contains commits the remote has. `git push --force` overrides that by **replacing the remote branch with yours**. On a branch others use, that silently deletes their commits.

The rules most teams follow:

- **Never force-push `main`** or any shared branch. Many teams make it impossible with branch protection (next lesson).
- On your **own** feature branch that nobody else has pulled, force-pushing after tidying up is acceptable. Use `git push --force-with-lease`, which refuses if the remote has commits you haven't seen.
- When in doubt, `git revert` instead.

## Common mistakes

**`reset --hard` with uncommitted work.** Those changes are gone; the reflog only remembers commits. Commit or stash first.

**Amending or resetting pushed commits**, then force-pushing to "fix" the rejection. Use `revert` for anything others have.

**Messages like "fix", "changes", "asdf".** Your history becomes useless exactly when you need it. One focused commit, one clear message.

**Forgetting the stash.** `git stash list` weeks later shows five mystery entries. Pop it right after you come back, or commit to a branch instead.

## Recap

- Make **small commits that each do one thing**; split mixed changes with the staging area.
- Follow the seven rules: blank line after the subject, subject ≤ 50 characters, capitalized, no period, **imperative** ("Fix", not "Fixed"), body wrapped at 72, body explains **what and why**.
- `restore` discards or unstages; `--amend` fixes the last unpushed commit; `revert` safely undoes pushed commits; `reset` moves a branch back (local only; `--hard` discards); `stash` sets work aside; `reflog` finds lost commits.
- Never force-push shared branches. If you must force-push your own branch, use `--force-with-lease`.
