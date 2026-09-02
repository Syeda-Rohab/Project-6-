# Project 6: The Doorbell Loop

A loop that reacts to a pull request, with no prompt typed. Uses
**100% free GitHub infrastructure** — GitHub Actions (free for public
repos) and the built-in `GITHUB_TOKEN` (no API key, no paid service).

- **Time:** 45–60 min
- **Difficulty:** medium
- **Concepts used:** Concept 7 (event-driven), Concept 10 (connectors)

## Files
| File | Role |
|---|---|
| `calculator.py` | Source code — `get_item()` has a null check + bounds check |
| `test_calculator.py` | Tests for the clean version |
| `pr_reviewer.py` | The review logic — scans a diff for two planted-bug patterns |
| `.github/workflows/pr-review.yml` | **The doorbell.** Fires automatically on `pull_request` events |

## What the reviewer looks for
1. **Deleted null check** — a removed line containing `is None` / `is not None`.
2. **Off-by-one risk** — a changed comparison against `len(...)` (`>=` vs `>`, etc).

Tested locally already (see below) — it correctly caught both.

## Proof it works (tested locally before pushing)
Planted bug: removed `if lst is None: return None`, and changed
`index >= len(lst)` to `index > len(lst)` (off-by-one).
```
## Automated PR Review (Doorbell Loop)

This automated reviewer found potential issues in this PR:

- ⚠️ Possible deleted null-check — this line was removed: `if lst is None:`
- ⚠️ Possible off-by-one risk in a bounds check — new line: `if index < 0 or index > len(lst):`

Please double check these before merging.
```

## Setting this up for real on GitHub (free, ~10 min)

1. **Create a free GitHub account** if you don't have one: github.com
2. **Create a new repository** (public is easiest — Actions minutes
   are unlimited for public repos). Name it anything, e.g. `doorbell-loop`.
3. **Push these files to it:**
   ```
   cd path\to\project6
   git remote add origin https://github.com/<your-username>/doorbell-loop.git
   git push -u origin main
   ```
   (If prompted, sign in with your GitHub username/password or a
   personal access token — GitHub will guide you.)
4. **Confirm the workflow is recognized:** go to your repo on
   github.com → the "Actions" tab → you should see "PR Doorbell
   Review" listed (it won't have run yet — that's expected, it only
   fires on pull requests).
5. **Open a PR with the planted bug:**
   ```
   git push origin fix/planted-bug
   ```
   Then on github.com, go to your repo → you'll see a banner offering
   to "Compare & pull request" for `fix/planted-bug` → click it →
   "Create pull request".
6. **Wait ~20–30 seconds.** No prompt typed, nobody clicked "review."
   Refresh the PR page — a comment will appear from `github-actions[bot]`
   listing the two planted bugs.
7. **Prove the event heartbeat re-fires:** push any small additional
   commit to the same branch (e.g. edit the README and
   `git push origin fix/planted-bug` again). This fires the
   `synchronize` event, and the workflow runs again automatically —
   a second review comment appears without you doing anything beyond
   the push.

## Done-when checklist
- [x] The reviewer catches the deleted null check.
- [x] The reviewer catches the off-by-one bug.
- [ ] *(do this part on github.com)* The PR gets a comment you never
  asked for.
- [ ] *(do this part on github.com)* Pushing again re-fires the review
  via the `synchronize` event.

## The four heartbeats (Projects 1–3 + this one)
| Project | Heartbeat | How it fires |
|---|---|---|
| 1 | In-session | You keep the conversation going yourself |
| 2 | Conditional | A check (e.g. `if` a test fails) decides whether to continue |
| 3 | Scheduled | `cron` fires it on a timer, no human involved |
| 6 (this one) | Event-driven | GitHub fires it the instant a `pull_request` event happens |

## Why this needs no paid tools
- GitHub Actions: free, generous minutes on public repos.
- `GITHUB_TOKEN`: auto-generated per workflow run, no signup, no key
  to manage, used only to post the comment.
- `pr_reviewer.py`: plain Python, no external API, no LLM call — a
  deterministic heuristic checker, same spirit as Project 4's reviewer.
