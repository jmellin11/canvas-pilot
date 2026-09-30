---
name: pilot-assignment
description: Help the student with one Canvas assignment, grounded in the real spec, their course history, their writing voice and related school email and Word documents. Use for "help me with <assignment>", "outline / draft / study for X", "what does this assignment want", or "check my draft".
---

# pilot-assignment

One assignment at a time. Everything you produce stays local. Submitting is
the student's call, through `canvas-submit`.

## 1. Pin down the assignment

Match what the student said to a current Canvas assignment
(`src/canvas_client.py`: `list_courses()`, `list_assignments(course_id)`).
If two could match, list them with due dates and ask.

## 2. Get the real spec

`assignment.description` is rarely the whole spec (README, "The core rule").
Gather:
- the description, the rubric (`get_rubric`) and the points
- files attached to the assignment (`list_assignment_files`) and any
  linked Canvas pages, module items or PDFs. Open them.
- the syllabus rules that apply (`context/current.md`): late policy, AI
  policy, citation style, length conventions

Say plainly if the spec is thin or contradictory, and ask before guessing.

## 3. Pull in what the student already knows

- `context/playbook.md`: the recipe for this assignment type and the usual
  point losses
- `context/courses/<course>.md`: what this professor has rewarded or
  marked down
- `context/archive/`: the student's earlier work of the same type, and this
  instructor's comments on it (search `files.json` and the course's
  `assignments.json` by type or keyword)
- **Outlook** (`outlook_email_search`, Microsoft 365): the instructor's or
  TA's emails about this assignment, such as clarifications, extensions or
  changed due dates. Search by course code, assignment name and instructor.
- **OneDrive / Word** (`sharepoint_search`, `read_resource`, Microsoft 365):
  an existing draft, notes or group files for it
- **Teams** (`chat_message_search`) for group projects

Read-only everywhere: never send, reply, edit or share.

## 4. Brief the student

Keep it short:
- what's actually being asked, as a rubric checklist
- what past feedback says to watch for
- anything from email that changes the spec
- a time estimate, the due date, and what's worth the most points

Then ask what they want: an outline, a full draft, a study guide, a check of
their own draft, or practice questions.

## 5. Produce it

- Work in `runs/<YYYY-MM-DD>/<course>-<assignment-slug>/`.
- Drafts follow `context/voice.md` and the assignment's format. Make a
  `.docx` with python-docx when the student will finish it in Word.
- Check the draft against every rubric line and the spec's hard limits
  (length, sections, citations, file type). Specialized work can go to the
  existing skills: code to `canvas-ics33`, zyBooks to `canvas-zybooks`,
  reading annotation to `canvas-reading-annotation`, long essays to
  `canvas-essay`. For graded writing or code, run the `pre-submit-reviewer`
  agent before calling it done.
- Show the file path, the rubric check, and anything the student has to
  decide or add themselves (personal experiences, data only they have).

## 6. After

If the student corrects the draft, apply the fix. If it looks like a lasting
preference, offer once to save it to `context/voice.md` or
`context/profile.md`. To submit, the student sends exactly `submit N` after
a `canvas-scan` plan exists, and `canvas-submit` takes it from there.
