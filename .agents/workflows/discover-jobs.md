# Discover and publish jobs

## Inputs

Read the requested count, seniority, geography and work arrangement from the conversation. Default to all levels, prioritize confirmed remote opportunities eligible for applicants in Brazil/LATAM, and apply the [maintainer guide's publication-date policy](../../docs/maintaining.md#publication-dates). Work arrangement and eligible geography come before seniority when ordering the publication queue: internships/junior first within the remote selection, then mid-level, senior and leadership. Do not fill a remote target with hybrid/on-site postings or remote jobs restricted to another country. Keep relocation in a separate secondary selection when requested. Do not silently broaden geography or age to reach the requested count.

## Procedure

1. Read README.md, docs/maintaining.md and the catalog. Inspect existing `jobs/*.json` and search open and closed GitHub issues before collecting candidates.
2. Search employer career pages and their public ATS listings. Use aggregators for discovery only; open the original listing to establish availability, original publication date, responsibilities, requirements, employment type and applicant geography.
3. Check original publication dates, not updated or indexing dates. Record the source's timezone/date interpretation when material. Remote does not establish Brazil eligibility. Exclude unverifiable candidates and report any shortfall.
4. Create one JSON record per accepted opportunity using the catalog. Preserve a stable provider/board/job identifier and clean application URL. Use explicit unknown values rather than inferring requirements or classifications. Set `last_checked` only after checking the live source. For an explicitly requested older link, explain the exception in `conditions` and follow the maintainer guide's exception policy.
5. Recheck the selected work arrangements and geographic restrictions against the request before previewing. Remote metadata does not override a concrete office-attendance requirement. For conditional remote work, spell out the excluded cities/residence conditions; leave conflicting arrangements unspecified. Never count a remote-only Spain/US/Canada opening as remote from Brazil. Run `python3 scripts/jobs.py check`, then preview only the selected files with `python3 scripts/jobs.py publish jobs/FILE.json --repo OWNER/REPO --max-age-days 7`. Multiple file arguments are supported. Inspect the rendered bodies and proposed classifications.
6. If publishing is authorized, sync labels through the existing script, then repeat the selected-file command with `--apply`. Use one publisher at a time, including local processes and GitHub Actions. Pace large selections instead of firing concurrent writers; batches of at most 25 creations spaced 200 seconds apart stay below the general hourly content ceiling, allowing room for verification/corrections. Respect any `Retry-After` or rate-limit response before resuming. The manual Action provides the same flow for committed records. Older exceptions require a separately reviewed CLI invocation without the age flag; never weaken the default Action.
7. Verify created issues against their records. Report issue links, exclusions and evidence limitations. Run the documented validation before committing any authorized repository changes.

## Source interpretation

- Greenhouse: original `first_published`, not `updated_at`; confirm the job remains listed on the employer board.
- Ashby: compare visible workplace and eligible locations with structured data. The public API documents `publishedAt` as the last publication and `isRemote` as including hybrid work; neither establishes an original publication date or a fully remote arrangement. Use `workplaceType` and corroborate the original date before applying the seven-day policy.
- Gupy: use the original listing's publication and status fields and visible location/workplace details; job ID order does not establish recency.
- Other providers: inspect public employer evidence and document uncertainty. Use normal browser access when needed; do not bypass authentication or access controls.

Do not turn these provider hints into another field schema. The catalog and README remain authoritative.

- Workday: use the active, publicly applicable posting’s `startDate`/`postedOn`, not a separate corporate search index’s `updateDate`. A recent update can belong to an older posting.
- Lever: corroborate API creation timestamps with the public employer page’s `JobPosting.datePosted`; do not silently rename creation as publication.
- Compensation: distinguish salary from meal/home-office allowances, company revenue and learning budgets. Flag implausible placeholder bounds rather than presenting them as a valid range.

- Gem: use `first_published_at` from the [public Job Board API](https://api.gem.com/job_board/v0/reference), not `updated_at`. Check `location_type` and eligible locations; company-wide remote language does not establish a remote vacancy.
- Get on Board: corroborate `published_at` with the original advertisement’s `datePosted` and read its remote-work policy. An API location of `Remote` does not establish country eligibility. Apply narrower employer restrictions when the platform uses a generic worldwide template.

- InHire: an API response with `status=published` and an HTTP 200 HTML shell do not prove that the public application page works. Follow the actual link on the employer board (including its career-page prefix and slug), render it, and confirm the matching title and application action. Defer publication when the public route shows 404 or cannot be verified; do not treat API availability as a substitute.
