# Early-career and international source review — 2026-11-13

## Published selection

The batch contains 100 additional opportunities from 37 employers, originally published between 2026-11-06 and 2026-11-13. All passed the publisher's seven-calendar-day age filter. This batch contains no historical exceptions.

Seventy records include an internship, junior or entry-level classification: 35 internships, 21 junior roles and 14 entry-level/graduate/working-student opportunities. One of the entry-level records is a multi-level requisition that also accepts more experienced engineers. These labels describe eligibility categories, not a claim that all 70 require no experience.

Thirty-five opportunities explicitly permit work in Brazil. The selection also includes Mexico, Argentina, Chile, Costa Rica, the US, Canada, Vietnam and European locations. CERN opportunities require work in Geneva; Brazil's Associate Member status is relevant to nationality eligibility, not permission to work remotely from Brazil. The [official CERN stakeholder page](https://home.cern/about/who-we-are/our-stakeholders) was checked for membership.

## Source evidence

- Gupy: original `publishedAt`, published status, registration deadline and current public role fields. Candidate collection covered IT service providers, industry, finance, education and research. 29 records selected.
- Greenhouse: original `first_published` from the current employer job-board response, with full public job content. Updates were not treated as publication. 38 records selected.
- SmartRecruiters: current public employer postings, `releasedDate` and active status, with role-specific descriptions and qualifications. 33 records selected, including CERN, Bosch, Experian, ServiceNow, Endava and Ubisoft.

The existing catalog remains the source of fields, form choices and labels. New categories support actual selected opportunities: entry-level programs, IT support, embedded work, game development, visual design, business operations, apprenticeships, permanent employment and additional countries. The form was regenerated through the existing script.

## Review decisions

- A recently published Minas Tênis Clube internship was excluded because its live registration deadline had passed, despite published status and a still-accessible page.
- LinkedIn's Sales Operations internship was excluded because the public employer posting API reported it inactive.
- Near-identical Compass QA and Java adverts were consolidated during selection; separate shifts or internship seasons were retained when they identify distinct opportunities.
- Duplicate language versions of Bosch trainee programmes were not counted separately.
- Sopra Steria's cloud/DevOps records require two or three years of experience despite generic entry-level metadata; they are not labeled junior/entry-level.
- Endava's Junior DevOps title conflicts with generic mid-senior metadata; the explicit role title and requirements take precedence.
- Pinterest's Sales Analytics internship requires office attendance despite remote location wording. Product Design placements may be hybrid or remote; no specific arrangement is promised.
- Brex engineering internships are remote, but full-time conversion requires hybrid work in São Paulo; the restriction is recorded.
- Riot internships explicitly restrict US work authorization and exclude visa sponsorship. Several require graduate study; disclosed pay marked “Remote Only” is recorded conditionally.
- Talan lists Buenos Aires but specifies remote work within CET timezone. Eligibility is marked unresolved rather than generalized to LATAM.
- Unknown salary, workplace and geography fields remain explicit. No worldwide eligibility is inferred from a remote label.

## Verification

The complete selected batch was validated and previewed before any write, checked against open and closed issues for source markers/URLs, and reviewed for candidate information. Publication uses the existing renderer, label synchronization and sequential publisher. Repository tests use a fake GitHub CLI and do not submit applications.

Published as issues [#87](https://github.com/velrino/jobs/issues/87) through [#186](https://github.com/velrino/jobs/issues/186). A post-publication read verified all 100 titles, bodies and label sets against their records; all 86 pre-existing issues retained their title, body, state and labels. Local validation passed for 186 records and 56 labels, and all eight repository tests passed.
