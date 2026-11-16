# File organiser CLI

Everyone has a Downloads folder full of PDFs, screenshots, zip files and installers. In this project you'll build a command-line tool that tidies a folder by moving each file into a subfolder for its type, safely: it never overwrites anything, it can show you its plan before it acts, and it can undo what it did.

It brings this whole section together: `argparse` for the interface, `pathlib` for moving files, JSON for the undo log, exception handling for everything that can go wrong on a real disk, and the debugger for the bugs you'll hit on the way.

## What it does

```bash
$ python organise.py organise ~/Downloads --dry-run
would move  report.pdf      -> documents/report.pdf
would move  holiday.jpg     -> images/holiday.jpg
would move  holiday.jpg     -> images/holiday (1).jpg     # a name clash, so a suffix
would move  setup.zip       -> archives/setup.zip
4 files would be moved. Run again without --dry-run to move them.

$ python organise.py organise ~/Downloads
moved 4 files. Undo with: python organise.py undo ~/Downloads

$ python organise.py undo ~/Downloads
restored 4 files.
```

## Requirements

- **Command-line interface** built with `argparse` and subcommands:
  - `organise <folder> [--dry-run]`: sort the files directly inside `<folder>` (not in subfolders) into subfolders by type.
  - `undo <folder>`: move every file back to where it was before the last `organise`.
- **Types by extension**, kept in one dict that's easy to edit, for example `images` (`.jpg`, `.jpeg`, `.png`, `.gif`), `documents` (`.pdf`, `.docx`, `.txt`, `.md`), `archives` (`.zip`, `.tar`, `.gz`), `audio`, `video`, and `other` for everything else. Match extensions case-insensitively (`.JPG` is an image).
- **Never overwrite.** If `images/holiday.jpg` already exists, use `images/holiday (1).jpg`, then `(2)`, and so on.
- **`--dry-run`** prints the full plan and moves nothing.
- **Undo log:** after a real run, write a JSON file in the folder (for example `.organise-log.json`) listing every move as `{"from": ..., "to": ...}`. `undo` reads it, moves the files back in reverse order, and deletes the log. A missing or corrupt log gives a clear message, not a traceback.
- **Clear errors** for a folder that doesn't exist, a path that's a file, and permission problems (`PermissionError`). Exit with a non-zero code (`sys.exit(1)`) on errors.
- Separate the **planning** (a function that returns the list of moves, without touching the disk) from the **doing** (a function that performs them). That makes the planner easy to test, and `--dry-run` just prints the plan.

## Build it in this order

1. `plan_moves(folder) -> list[tuple[Path, Path]]`. Test it on a temporary folder made with `tempfile.TemporaryDirectory()`.
2. Name clash handling inside the planner (remember that two files in the same run can clash with each other, not just with existing files).
3. `argparse` with `organise` and `--dry-run`, printing the plan.
4. Actually moving the files (`Path.rename`, or `shutil.move`), and writing the log.
5. `undo`.
6. Error handling for every failure you can think of. Try each one on purpose.

> **Note:** test on a **copy** of a folder, never on your real Downloads, until undo works.

## Write-up

Add a `README.md` with how to install and run it, and a short section, **"A bug I found with the debugger"**: what the symptom was, how you reproduced it, what you inspected with `breakpoint()` or VS Code breakpoints, the cause, and the fix. Use your AI assistant to explain concepts if you get stuck, but write the code and the write-up yourself.
