# Parse a user story

Teams write work as **user stories**: one sentence in the shape

```
As a <role>, I want <goal> so that <benefit>.
```

followed by **acceptance criteria**, often written as `Given` / `When` / `Then` lines (with `And` for extra steps). Before a story is "ready" to work on, all of those parts must be there. You'll write a small checker a team could run on new tickets.

Write `parse_user_story(text: str) -> dict`.

- `text` is the whole ticket: the story sentence on one line, then (optionally) criteria lines. Blank lines can appear anywhere.
- The **story line** is the first non-blank line that doesn't start with `Given`, `When`, `Then` or `And`.
- Return a dict with these keys:
  - `"role"`: the text after `As a` / `As an` at the start of the story line, up to a comma, `I want`, or the end of the line.
  - `"goal"`: the text after `I want` (drop a leading `to `), up to a comma, `so that`, or the end of the line.
  - `"benefit"`: the text after `so that`, to the end of the line.
  - `"criteria"`: a list of every line that starts with `Given`, `When`, `Then` or `And`, stripped, in order.
  - `"missing"`: a list of the parts that are absent, in the order `"role"`, `"goal"`, `"benefit"`, `"criteria"`.
- Matching is case-insensitive. Strip spaces, commas and full stops from the ends of the role, goal and benefit. A part that's absent is `None` (or `[]` for criteria).

## Example

```python
ticket = """As a library member, I want to renew a loan online so that I don't pay late fees.

Given I have a book due tomorrow
When I click "Renew"
Then the due date moves forward 14 days"""

parse_user_story(ticket)
# {'role': 'library member',
#  'goal': 'renew a loan online',
#  'benefit': "I don't pay late fees",
#  'criteria': ['Given I have a book due tomorrow', 'When I click "Renew"',
#               'Then the due date moves forward 14 days'],
#  'missing': []}
```

> **Hint:** `re.search(pattern, line, re.IGNORECASE)` with a lazy group like `(.+?)` followed by the possible endings, for example `(?:,|\bi want\b|$)`.
