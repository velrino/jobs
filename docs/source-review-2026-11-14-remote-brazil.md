# Remote Brazil/LATAM source review — 2026-11-14

## Verified selection

The seven-calendar-day window is 2026-11-07 through 2026-11-14, checked against employer publication evidence. The requested target of 1,000 qualifying opportunities was not reached. A search result, a recently updated advert and an unconfirmed international work location are not counted toward that target.

The focused selection contains **167 remote opportunities that explicitly include Brazil**, spanning internships, junior/entry-level, mid-level, senior and leadership roles. Some also have an equivalent employer posting for Colombia; those country variants are linked rather than inflated into separate opportunities. Check individual residence and office-attendance exceptions, especially Campinas-based applicants for CI&T projects.

The complete publication set for this review contains **333 new issues (#187–#519)** from 155 employers. Of these, 170 have a remote label: 167 include Brazil and three are restricted to other locations. The remaining 107 hybrid and 56 on-site records retain their separate classifications and are **not** counted toward the focused remote quota. This is a dated publication audit, not a claim that every catalogued role meets the remote Brazil/LATAM selection.

The last 58 publications, [#462](https://github.com/velrino/jobs/issues/462) through [#519](https://github.com/velrino/jobs/issues/519), are exclusively remote opportunities with stated Brazil eligibility. Unpublished hybrid, on-site, relocation and unconfirmed leads were removed from the public publication queue. Their existence does not establish current eligibility or publication dates.

Browse [remote roles in Brazil](https://github.com/velrino/jobs/issues?q=is%3Aissue%20is%3Aopen%20label%3Awork%3Aremote%20label%3Aregion%3Abrazil), then combine the existing seniority labels. No application or candidate information is part of these records.

## Employer evidence and exclusions

- Gupy: live published status, the employer's `publishedAt`, qualifications/duties, workplace fields and registration deadline. Generic titles were checked for actual technical work; examples include HR implementation with Python/SQL and logistics internships building SQL/Power BI automations. Retail, clinical, purely commercial and administrative results, internal-only and test adverts, expired deadlines and talent pools were excluded.
- Greenhouse: current employer board and original `first_published`, not `updated_at`. Canonical's [Junior Project Manager](https://job-boards.greenhouse.io/canonical/jobs/5861481) appeared in a recent external feed, but the employer reports original publication on 2024-03-28; it was excluded from this seven-day selection.
- SmartRecruiters: active employer postings and their `releasedDate`, with role-specific qualifications and workplace flags. Company-wide “worldwide” wording, domestic moving bonuses and a future transfer programme do not establish international eligibility for the advertised job. Talan's LATAM location headers conflicted with CET remote restrictions and were not treated as confirmed remote Brazil eligibility.
- Lever: current public employer postings and `JobPosting.datePosted` corroborated the API creation date. Identical/country-language variants of the same requisition were consolidated. A Claude Systems Architect title whose body described a mid-level Java developer was excluded because the scope was unresolved.
- Workday/Accenture: active `canApply`/`posted` status and original `startDate`/`postedOn`, rather than the corporate index's `updateDate`. For example, an SAP AMS posting updated on November 13 had a Workday start date of October 27 and was excluded. Generic “Early Career” metadata did not override explicit multi-level titles or experienced requirements. Data-scientist requirements were separated by junior, mid and senior track.
- Ashby: the [official public API documentation](https://developers.ashbyhq.com/docs/public-job-posting-api) defines `publishedAt` as the last publication and `isRemote` as including hybrid work. Neither alone establishes original publication or fully remote work. Uncorroborated cases were excluded.
- Other discovery sources included employer careers pages, YC, Amazon Jobs, Workable, Manatal and specialist boards. Aggregators supplied leads only. Manatal examples lacked public original-date evidence; a Workable source rate limit prevented complete verification. These were not converted into qualifying records merely to increase the count.

Relocation was researched separately, including Canada, Dubai and Abu Dhabi. It does not establish remote work from Brazil/LATAM and was not used to fill the remote target. A work-permit question alone is not a promise of sponsorship. No conclusion that these markets have no suitable jobs is implied by the verified selection.

## Reuse and verification

The README owns eligibility and publication policy. The discovery workflow now orders work arrangement and geography before seniority; the catalog continues to own all fields, classifications and generated form choices. Only Colombia was added as a country category needed by accepted records. No duplicate schema, alternate public publisher or scheduled search was introduced.

All selected files were validated and previewed through the existing publisher with `--max-age-days 7`. Publications were serialized and paced below GitHub's documented content-creation limits. Open and closed issues were checked for source markers and original URLs. Final verification compares every title, body and label set with the records and checks that all 186 pre-existing issues retained their title, body, state and labels. Blank issue creation remains disabled.

Verification passed: all 333 new issues matched their record titles, bodies and labels; the final 58 have both `work:remote` and `region:brazil`. All 186 pre-existing issues were unchanged. Local catalog/form validation passed for 519 records and 57 labels, and all eight repository tests passed.
