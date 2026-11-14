# Discover and publish jobs

## Inputs

Read the requested count, seniority, geography and work arrangement from the conversation. Default to all levels, prioritize remote opportunities eligible for applicants in Brazil, and apply the README's publication-date policy. Do not silently broaden geography or age to reach the requested count.

## Procedure

1. Read README.md and the catalog. Inspect existing `jobs/*.json` and search open and closed GitHub issues before collecting candidates.
2. Search employer career pages and their public ATS listings. Use aggregators for discovery only; open the original listing to establish availability, original publication date, responsibilities, requirements, employment type and applicant geography.
3. Check original publication dates, not updated or indexing dates. Record the source's timezone/date interpretation when material. Remote does not establish Brazil eligibility. Exclude unverifiable candidates and report any shortfall.
4. Create one JSON record per accepted opportunity using the catalog. Preserve a stable provider/board/job identifier and clean application URL. Use explicit unknown values rather than inferring requirements or classifications. Set `last_checked` only after checking the live source. For an explicitly requested older link, explain the exception in `conditions` and follow the README's exception policy.
5. Run `python3 scripts/jobs.py check`, then preview only the selected files with `python3 scripts/jobs.py publish jobs/FILE.json --repo OWNER/REPO --max-age-days 7`. Multiple file arguments are supported. Inspect the rendered bodies and proposed classifications.
6. If publishing is authorized, sync labels through the existing script, then repeat the selected-file command with `--apply`. Use one publisher at a time, including local processes and GitHub Actions. The manual Action provides the same flow for committed records. Older exceptions require a separately reviewed CLI invocation without the age flag; never weaken the default Action.
7. Verify created issues against their records. Report issue links, exclusions and evidence limitations. Run the documented validation before committing any authorized repository changes.

## Source interpretation

- Greenhouse: original `first_published`, not `updated_at`; confirm the job remains listed on the employer board.
- Ashby: compare visible workplace and eligible locations with structured data; a remote flag alone is insufficient.
- Gupy: use the original listing's publication and status fields and visible location/workplace details; job ID order does not establish recency.
- Other providers: inspect public employer evidence and document uncertainty. Use normal browser access when needed; do not bypass authentication or access controls.

Do not turn these provider hints into another field schema. The catalog and README remain authoritative.
