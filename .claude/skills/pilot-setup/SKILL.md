---
name: pilot-setup
description: Short onboarding interview that fills in the student's profile, goals and preferences for Canvas Pilot, and checks that Canvas and Microsoft 365 are connected. Use on the first run, or for "update my profile".
---

# pilot-setup

Ask one question at a time and save answers as you go. Skip anything that's
already filled in `context/profile.md`.

## Connections first

1. **Canvas:** `.venv/bin/python -c "from src import canvas_client as c; print(c.session_alive(10))"`.
   If this prints False, or `.env` has no `CANVAS_BASE`, dispatch
   `canvas-setup` for the mechanical part and come back.
2. **Microsoft 365:** run one `outlook_email_search` for recent mail. If the
   connector is missing or can't authenticate, ask the student to connect it
   with their school account (Customize → Connectors). Some schools require
   IT approval. If so, note in the profile that email and OneDrive go
   through the built-in browser instead.

## Interview

1. Major, year, expected graduation, and any concentration or minor.
   → Profile
2. What matters most this term: a GPA target, particular courses, keeping
   up while working? → Profile › Current goals
3. Work and commitments that affect when you study (jobs, shifts, clubs).
   → Profile › Schedule
4. How much help you want by default: an outline and feedback, a full draft
   you edit, or just the checklist and deadlines. → Profile › Preferences
5. Anything about your writing I should always follow or avoid (tone,
   first person, formatting, citation style). → `voice.md` › Do / don't
6. Your time zone (default America/Denver). → Profile

If `context/playbook.md` doesn't exist yet, offer to run `pilot-learn` now.

Finish with a 3-line summary of what Canvas Pilot now knows about you.
