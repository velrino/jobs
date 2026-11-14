# Jobs

A repository for sharing job opportunities through GitHub Issues. Postings and labels are written in English.

Browse [open positions](https://github.com/velrino/jobs/issues) or [create a job posting](https://github.com/velrino/jobs/issues/new/choose).

## Share an opportunity

Use the **Job opportunity** issue form. Blank issues are disabled so every posting follows this structure. Verify the original listing, summarize its responsibilities and requirements, and include its public application link, job ID, eligible location and verification date. Include compensation with currency and pay period when disclosed; mark missing information explicitly.

Title format: `[Company] Job Title — Location / Work arrangement`.

Remote work does not imply worldwide eligibility. For example, a US-only remote role uses both `work:remote` and `region:us`. Do not infer full-time employment, visa sponsorship, relocation support or Staff seniority from a salary or an Architect title.

Search **open and closed** issues for the source key and original job URL before posting. A source key identifies one provider, board and job, for example `greenhouse:housecall:5740249004`. Remove tracking parameters from URLs while preserving job identifiers.

## Publication dates

New searches are limited to postings originally published within the last seven calendar days. Record the employer-confirmed date in `published_on`; updates, search indexing and discovery dates do not establish recency. Older existing issues remain historical records. Explicitly requested older links must show their original date and explain the exception.

Use `--max-age-days 7` with the selected new JSON files to reject older or undated postings before any GitHub write. Existing records predating this policy may omit `published_on`. The [source review](docs/source-review-2026-11-13.md) records historical leads excluded from the latest search.

## Reusable classifications

[`.github/job-catalog.json`](.github/job-catalog.json) is the single source for field definitions, label names, descriptions, colors and form choices. Labels use these prefixes:

| Prefix | Purpose |
| --- | --- |
| `role:` | Professional area |
| `specialty:` | Engineering or professional specialty |
| `level:` | Explicit seniority or management level; multiple levels are allowed |
| `work:` | Remote, hybrid or on-site arrangement |
| `type:` | Employment type |
| `region:` | Eligible applicant geography |

Use `unspecified` when a category is not disclosed. Select only supported values; a country listing does not establish eligibility across its entire continent. Maintainers apply the matching labels to issues submitted through the form; the form itself does not assign dropdown values as labels.

Add a catalog value only when an actual posting needs it. Reuse existing categories across companies; keep specific technologies, cities, benefits and salaries in the posting text. All labels within a category share a color. The sync command preserves labels outside the catalog.

The issue form is generated from the catalog. Do not edit it directly:

```sh
python3 scripts/jobs.py generate
python3 scripts/jobs.py check
```

## Publish structured jobs

Requires Python 3.10+ and an authenticated [GitHub CLI](https://cli.github.com/) with access to the target repository.

Files in [`jobs/`](jobs/) are the source records used by the publishing command. Copy an existing JSON file and use the field IDs and choices from the catalog. Classification values are arrays, including categories that accept a single value. Each source key and original URL must be unique.

Preview first; writes require `--apply`:

```sh
python3 scripts/jobs.py labels
python3 scripts/jobs.py labels --apply
python3 scripts/jobs.py publish
python3 scripts/jobs.py publish --apply
```

To select a single file or explicitly target a repository:

```sh
python3 scripts/jobs.py publish jobs/gupy-qualitydigital-12869427.json --repo velrino/jobs --max-age-days 7
```

The script derives titles, Markdown bodies and labels from the catalog and job records. It checks every selected record before writing and requires all selected labels to exist before creating issues. It searches all issues, including closed ones, for the stable source marker or original URL and skips existing postings. Re-running sequentially is safe; do not run concurrent publishers. Publication is sequential and can partially succeed if GitHub fails; re-run to create only the remaining issues.

Publication creates missing issues; it does not overwrite existing descriptions, reopen closed issues or remove labels. To correct an existing posting, update its JSON record and edit the linked issue after verifying the source. Refresh `last_checked` only after checking the live posting; the script validates records, not external vacancy availability.

Keep issues open while the vacancy is available at the last check. Close filled or expired postings as completed. Close duplicates or discarded postings as not planned with a reason. Issue state provides the lifecycle; no duplicate status labels are needed.

## Validation

```sh
python3 scripts/jobs.py check
python3 -m unittest discover -s scripts -p '*_test.py'
```

Checks verify the records and generated form. Tests use a fake GitHub CLI in a temporary directory and never access the real GitHub account.

## Author

Maintained by [Velrino](https://github.com/velrino/).

[Website](https://velrino.co/)
