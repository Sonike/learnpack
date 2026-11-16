# Branches and merging

On a team, five people might be working on five different features in the same codebase on the same day, and none of them wants half-finished work from the others breaking their code. **Branches** make that possible: each piece of work happens on its own line of history, and gets **merged** back when it's ready. Even working alone, branches let you try an idea without risking the version that works. And when two lines of work touch the same lines of code, you'll get a **merge conflict**, which sounds scary and isn't, once you know how to read one.

## What a branch really is

From the lesson "Version control basics": every commit is a snapshot that points back to its parent. That gives a chain:

```
A <-- B <-- C
            ^
           main
```

A **branch is just a name that points to a commit.** `main` is a branch; right now it points to `C`. That's all a branch is: a tiny file containing a commit's hash. Creating a branch is instant, and it costs nothing.

When you commit on a branch, the new commit's parent is the commit the branch pointed to, and the branch name **moves forward** to the new commit.

How does Git know which branch you're on? A special pointer called **`HEAD`** points to your current branch. `git log --oneline` shows it as `HEAD -> main`.

## Creating and switching branches

Let's start a new feature on its own branch:

```bash
$ git switch -c add-farewell
Switched to a new branch 'add-farewell'
```

`git switch -c name` **c**reates a branch at your current commit and switches to it. You'll also see the older command `git checkout -b name` in tutorials and answers online; it does the same thing.

```
A <-- B <-- C
            ^
           main
           add-farewell  <-- HEAD
```

Both names point to `C`. Now commit on the new branch:

```bash
$ echo 'print("Goodbye!")' >> hello.py
$ git commit -am "Say goodbye"
[add-farewell 3b8e1d2] Say goodbye
 1 file changed, 1 insertion(+)
```

(`-a` stages every already-tracked file that changed, so `commit -am` adds and commits in one go. It never adds untracked files.)

```
A <-- B <-- C <-- D
            ^     ^
          main   add-farewell  <-- HEAD
```

`add-farewell` moved to `D`. `main` didn't move: it still points to `C`, so anyone working from `main` doesn't see your change yet.

Switching back to `main` changes the files in your working tree to match `C`:

```bash
$ git switch main
Switched to branch 'main'
$ cat hello.py
print("Hello!")
```

The goodbye line hasn't vanished; it's safe in commit `D`, on the other branch. Switch back and it reappears.

```bash
$ git branch
  add-farewell
* main
```

`git branch` lists branches; the `*` marks the current one.

> **Note:** commit (or stash, covered in "Good commits and undoing mistakes") before switching branches. If uncommitted changes would be overwritten, Git refuses to switch and tells you which files are in the way.

## Merging

When the feature is ready, you bring it into `main` with `git merge`. You switch to the branch you want to merge **into**, then name the branch to merge **from**:

```bash
$ git switch main
$ git merge add-farewell
Updating 9c4f0e1..3b8e1d2
Fast-forward
 hello.py | 1 +
 1 file changed, 1 insertion(+)
```

### Fast-forward merges

"Fast-forward" is the simple case. `main` was at `C`, and `D` was built directly on top of `C`. Nothing happened on `main` in the meantime, so there's nothing to combine: Git simply moves the `main` label forward to `D`.

```
before:  A <-- B <-- C <-- D         after:  A <-- B <-- C <-- D
                     ^     ^                                   ^
                   main   add-farewell                    main, add-farewell
```

No new commit is created.

### Merge commits

Now the realistic case: while you worked on your branch, someone else added commit `E` to `main`.

```
              D   <-- add-farewell
             /
A <-- B <-- C
             \
              E   <-- main  (HEAD)
```

The histories have **diverged**. `main` can't just slide forward to `D`, because that would lose `E`. So Git creates a new **merge commit**, `M`, that has **two parents** (`E` and `D`) and combines both sets of changes:

```bash
$ git merge add-farewell
Merge made by the 'ort' strategy.
 hello.py | 1 +
 1 file changed, 1 insertion(+)
```

```
              D
             /  \
A <-- B <-- C    M   <-- main  (HEAD)
             \  /
              E
```

`main` now points to `M`; `add-farewell` still points to `D`. Git may open an editor for the merge commit's message; the default ("Merge branch 'add-farewell'") is fine, so save and close it. (`ort` is just the name of Git's merging algorithm.)

Once a branch is merged, you can delete its name. The commits stay in history:

```bash
$ git branch -d add-farewell
Deleted branch add-farewell (was 3b8e1d2).
```

## Merge conflicts

Git merges changes automatically when they touch different files, or different parts of the same file. When both branches changed **the same lines** differently, Git can't know which version is right, so it stops and asks you. That's a **merge conflict**. It's not an error and nothing is broken; it's Git being careful.

```bash
$ git merge friendlier-greeting
Auto-merging hello.py
CONFLICT (content): Merge conflict in hello.py
Automatic merge failed; fix conflicts and then commit the result.
```

`git status` lists the files that need attention under "Unmerged paths". Open `hello.py` and you'll see **conflict markers**:

```
def greet(name):
<<<<<<< HEAD
    greeting = "Hello"
=======
    greeting = "Hi there"
>>>>>>> friendlier-greeting
    return f"{greeting}, {name}!"
```

How to read it:

- `<<<<<<< HEAD` to `=======` is **ours**: the version on the branch you're on (and merging into).
- `=======` to `>>>>>>> friendlier-greeting` is **theirs**: the version from the branch you're merging in.
- Everything outside the markers merged cleanly.

### Resolving a conflict, calmly

1. **Run `git status`** to see every conflicted file.
2. **Open each file and decide** what the code should be. Keep ours, keep theirs, keep both, or write something new that combines them. Think about what each side was trying to do; if you don't know, ask whoever wrote the other change.
3. **Delete all the marker lines** (`<<<<<<<`, `=======`, `>>>>>>>`). The file must be valid code again.
4. **Run the code or the tests.** A file without markers can still be wrong.
5. **Stage and commit:**

```bash
$ git add hello.py
$ git commit
[main 7a1d9c3] Merge branch 'friendlier-greeting'
```

VS Code highlights conflicts and offers "Accept Current Change" (ours), "Accept Incoming Change" (theirs) and "Accept Both Changes" buttons above each one. They're handy, but understand what they do, which is exactly what you'll code in the practice exercise.

If you get in a muddle, you can always back out and return to how things were before the merge:

```bash
$ git merge --abort
```

## Rebase: the other way to combine work

You'll hear about **rebase**, so here's the concept. Instead of joining two diverged histories with a merge commit, `git rebase main` (run on your feature branch) **replays your branch's commits on top of the latest `main`**, as if you had started your work from there:

```
before:                        after git rebase main:
      D  <-- feature                       D'  <-- feature
     /                                    /
A-B-C-E  <-- main             A-B-C-E  <-- main
```

The result is a straight-line history with no merge commit. But notice `D'`: rebasing creates **new commits** with new hashes, and abandons the old ones. If anyone else already has the old `D` (because you pushed it and they pulled it), their history and yours now disagree, which causes real confusion.

So the rule is simple: **never rebase a branch other people are using.** Rebasing your own local, unshared commits is fine. As a beginner, use merge; it's always safe. The Learn Git Branching tutorial in the resources lets you try rebase visually without risk.

## Common mistakes

**Committing to the wrong branch.** You forgot to create a branch and made commits directly on `main`. Check `git status` (its first line says `On branch ...`) before you start work. "Good commits and undoing mistakes" shows how to move commits to the right branch.

**Merging in the wrong direction.** `git merge main` while on your feature branch brings `main` *into* the feature, which is useful for updating your branch, but it isn't the same as merging your feature into `main`. Always ask: which branch am I on, and which branch am I bringing in?

**Committing conflict markers.** You resolved most of the file and left a stray `=======`. The code then fails with `SyntaxError: invalid syntax` pointing at it. Search the file for `<<<<<<<` before committing.

**Panicking at a conflict.** Conflicts are routine; experienced engineers resolve several a week. Nothing is lost, and `git merge --abort` takes you back.

**Long-lived branches.** A branch that lives for three weeks drifts far from `main` and ends in a huge, painful merge. Keep branches small and merge them often.

## Recap

- A **branch** is a movable name that points to a commit. `HEAD` points to the branch you're on. Commits on a branch move only that branch's name.
- `git switch -c name` creates and switches (older: `git checkout -b name`); `git switch name` switches; `git branch` lists.
- `git merge other` brings `other` into the current branch. A **fast-forward** just moves the name; diverged histories get a **merge commit** with two parents.
- Conflicts happen when both sides changed the same lines. Between `<<<<<<<` and `=======` is ours (`HEAD`); between `=======` and `>>>>>>>` is theirs. Edit, remove the markers, test, `git add`, `git commit`. `git merge --abort` backs out.
- Rebase replays commits on a new base and rewrites them. Never rebase shared branches.
