---
name: pilot-learn
description: Build Canvas Pilot's knowledge of the student from their Canvas history, school email and Word documents, and save it as context notes (playbook, voice, per-course notes, current term). Use for "learn my Canvas history", "update what you know", "analyze my past assignments", or at the start of a new term.
---

# pilot-learn

Build the knowledge base in `context/`, **read-only**. Never submit, post,
send, reply, move or delete anything in Canvas, Outlook, OneDrive or Teams.

## Source #1: Canvas history (preferred)

The student's own record is the best teacher: what they turned in, what it
scored, and what professors wrote back.

1. Pull it:

   ```bash
   .venv/bin/python scripts/learn_canvas_history.py
   ```

   It writes `context/archive/`:
   - `<course_id>/course.json` + `assignments.json`: courses that can still be
     opened (usually just the current term): syllabus, grading weights,
     assignment specs, rubrics, the student's scores, late/missing flags,
     instructor comments, rubric scores, and `text/<assignment_id>.txt` with
     what they turned in
   - `grades.json`: the final score for every enrollment, past ones included
   - `files.json` + `files/`: the student's own Canvas files. Uploads land in
     `Submissions/<course>/`, so this is the main record of past work even
     when the course is locked. Each document has a `.txt` sidecar.
   - `inbox.json`: Canvas inbox threads with instructors and classmates
   - `stats.json`: per-course aggregates, score by submission type, lowest
     scores with the comments on them

   Re-runs skip concluded courses already pulled (`--refresh` forces them).
   If it raises `SignedOut`, run `.venv/bin/python -m src.canvas_login` so
   the student can sign in, then re-run.

2. Analyze with short Python snippets over the archive, returning aggregates
   and excerpts, never whole files. Cover:
   - **Grades:** the distribution across enrollments, the strongest and
     weakest courses, and the current-term standing
   - **Assignment types:** what each type asks for (essay, discussion post,
     case analysis, presentation, spreadsheet lab, quiz, reflection), how the
     student scores on each, and where the points went (rubric criteria with
     lost points, late or missing work)
   - **Feedback themes:** group the instructor comments and rubric comments
     into themes (citations, depth of analysis, formatting, length, following
     instructions), with 3–5 short excerpts each
   - **Voice:** read 8–12 of the student's own documents across courses and
     years, favoring higher-scored work. Note tone, sentence length, how they
     open and close, first person vs. third, structure and headings,
     citation style, and words they lean on. Quote 3–4 short passages
     that sound most like them.
   - **Instructors:** for each current-term instructor, anything the syllabus,
     comments or inbox show about what they value

## Source #2: school email (Outlook, via the Microsoft 365 connector)

Canvas locks old courses, but its notification emails don't expire. Use
`outlook_email_search` to find:
- Canvas notifications about graded work and submission comments, which carry
  professor feedback from past terms. Add those to the feedback themes.
- Emails from professors and TAs about current courses (extensions,
  clarifications, announcements). Add them to `current.md`.

Summarize, don't copy. Skip anything personal or unrelated to school.

## Source #3: Word documents (OneDrive, via the Microsoft 365 connector)

Use `sharepoint_search` / `sharepoint_folder_search` to list the student's
Word documents, and `read_resource` to open a few. Drafts that never made it
to Canvas still show their voice. Add those findings to `voice.md` and note
which OneDrive folders hold class work in `profile.md`.

If the connector isn't connected, skip sources #2 and #3, say so in the
report, and continue.

## What to write

| File | Contents |
|---|---|
| `context/playbook.md` | Grades at a glance, assignment-type recipes (what earns points and the usual point losses for each type), feedback themes with excerpts, timing habits, and a "before you submit" checklist built from real point losses. Note the date range covered. |
| `context/voice.md` | Voice profile, quoted passages, formatting and citation habits, and do/don't lists for drafts |
| `context/current.md` | One section per current course: instructor, grading weights, key syllabus rules (late policy, AI policy, citation style), standing, what's due next |
| `context/courses/INDEX.md` | One row per course: note file, course, term, final grade |
| `context/courses/<code>-<term>.md` | What the course asked for, how it went, and the feedback worth remembering |
| `context/profile.md` | Create it if missing (name, school, major from the course mix, year). Otherwise just update the facts learned. Leave goals to `pilot-setup`. |

Keep each note under about 150 lines. Keep numbers, rubric wording and
policies exact. When a note already exists, rewrite it in the same structure
rather than appending.

## Report

Finish with: what was pulled (courses, files, threads, emails, documents),
what was locked or skipped and why, what changed since the last run, and 3
things about the student's record that stood out.

The student may name one source ("just read my email"). Do only that
source.
