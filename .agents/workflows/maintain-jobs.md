# Maintain existing opportunities

1. Read the README's lifecycle policy. Select the requested records/issues, or list open issues for a repository-wide review. Include both record-backed and manually submitted opportunities.
2. Reopen each original source. Compare availability, requirements, compensation, workplace and eligible geography with the issue. A blocked request, timeout, empty JavaScript shell or isolated HTTP error does not establish that a vacancy expired; mark it unverified and try the employer board or browser.
3. Prepare a report linking the issue and source, with the observed evidence, verification date and proposed correction or closure. Flag duplicate source keys/URLs across open and closed issues. Do not infer that a closed issue should be reopened.
4. When maintenance writes are authorized, update the source record and matching issue together. Render record-backed bodies and labels through `scripts/jobs.py` rather than duplicating its formatting. Preserve discussion and unrelated labels. Refresh `last_checked` only after live verification. Follow the README for closure reasons; never close issues solely because their original publication date is old.
5. Run the documented validation, verify the changed issues remotely, and report changed and unresolved items. Do not change the generated form directly or create status labels.

This workflow is agent-assisted and manual. It does not schedule checks, refresh dates automatically or claim live vacancy verification from local JSON validation.
