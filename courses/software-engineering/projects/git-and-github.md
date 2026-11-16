# Team Git exercise

Git skills only become real when there's someone else on the other end of the remote. In this project you'll run a small project the way a professional team does: issues, feature branches, pull requests, reviews, a protected `main`, a deliberate merge conflict, and an undo with `git revert`.

Do it with a friend or fellow learner if you can. If you're working alone, **simulate a second person** with two clones of the same repository in two different folders (`alice/` and `bob/`), and switch between them. That's how you'll create a real conflict.

## The project

The code can be small; the history is what's being judged. A good choice is a repository of your section 3 tools: put your **commit message checker** (`check_commit_message`, from the practice for "Good commits and undoing mistakes") in a script, plus one or two other utilities from this section, with a README.

## Steps

1. **Create the repository on GitHub** with a `README.md` and a Python `.gitignore` (`.venv/`, `__pycache__/`, `*.pyc`, `.env`). Clone it.
2. **Protect `main`:** in Settings, add a branch protection rule or ruleset that requires a pull request before merging. If you're working with a partner, require one approval. (A free account allows this on public repositories.)
3. **Create three issues**, each a small, real piece of work, for example: "Add a command-line interface to the commit checker", "Check the commits of a whole repository", "Document usage in the README".
4. **For each issue:** branch from an up-to-date `main`, commit in small steps, push, and open a pull request with **What / Why / How to test** sections and `Closes #N`. Merge it once it's reviewed. Each issue should be closed by its own PR.
5. **Create a merge conflict on purpose.** On two branches (or in your two clones), change the same line of the README differently. Merge one PR, then update the other branch from `main` (`git pull origin main` while on it) and resolve the conflict. Describe what you chose and why in that PR.
6. **Review.** On at least one PR, leave at least two review comments (your partner's PR, or your own if you're alone: comment as a reviewer would). Address them with a follow-up commit and reply to each comment.
7. **Undo a mistake properly.** Merge something deliberately wrong to `main` (a typo, a broken line), then fix it with `git revert <hash>` in a new PR, and explain in that PR why `revert` was the right tool rather than `reset`.
8. **Check your history.** Run your commit message checker over every commit message on `main` (`git log --format=%B` prints them) and fix your habits if it complains.

## Tips

- Use `git status` before every command you're unsure about, and `git log --oneline --graph --all` to see the branch structure.
- If something goes wrong locally, `git reflog` almost always has the commit you need.
- Keep the conflict calm: read both sides, decide, remove every marker, run the code, then `git add` and `git commit`.
