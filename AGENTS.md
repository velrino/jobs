# Job repository workflows

Use [discover jobs](.agents/workflows/discover-jobs.md) for searches and new opportunities, and [maintain jobs](.agents/workflows/maintain-jobs.md) for existing postings.

The [README](README.md) owns publication and lifecycle policy. `.github/job-catalog.json` owns fields and classifications; `scripts/jobs.py` owns validation, rendering, label sync and duplicate detection. Reuse these sources instead of creating parallel schemas or publishers. Keep documentation and issue content in English.

A request to explain or review is read-only. Search, publishing, issue edits and closing must stay within the user's requested scope. Never submit applications or contact employers as part of these workflows. Preserve unrelated changes; commits require authorization and the trailer `Co-authored-by: Codex <codex@openai.com>`.

## Privacy when collecting opportunities

Private application materials may identify public job links, but are never publication sources for a person's details. Verify vacancy facts on public employer sources. Publish only the opportunity: omit candidate names, contact details, resumes, answers, application status, recruiter conversations, research notes and any statement that the maintainer applied. Keep coverage tracking and personal provenance in ignored `.local/`. Check staged files and rendered issues for accidental personal information before publishing. Honor explicit exclusions without recording their private rationale publicly.
