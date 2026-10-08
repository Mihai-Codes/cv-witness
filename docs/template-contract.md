# Repeatable CV template contract

Date: 2026-10-09
POC: Mihai-Alexandru Chindriș
TL;DR: One structured input, one print layout and four section-order presets. Every selected record is rendered and checked; page limits fail visibly instead of discarding content.

## Input

The version-1 JSON document supplies a `header` with a name and optional contact details, plus optional `summary`, `skills`, `experience`, `projects`, `education`, `certifications`, `languages` and `publications`.

Experience is a list of employers with a list of roles. Each role has a title, dates and a list of bullets. Empty optional sections produce no heading. Unknown fields or wrong types fail, rather than disappearing during rendering. The document contains approved wording, not a request to invent qualifications or rewrite a job posting.

## Presentation

- Engineering: summary, skills, experience, projects, education, certifications, publications, languages.
- Operations/Support: summary, experience, skills, certifications, projects, education, publications, languages.
- Research: summary, education, experience, publications, projects, skills, certifications, languages.
- Management: summary, experience, projects, skills, education, certifications, publications, languages.

Presets reorder complete sections only. They do not change dates, metrics, bullet text, role counts or qualifications. An explicit section-order override must include every nonempty section exactly once.

A shared HTML shell and print stylesheet use selectable text, inline metadata and a single column. A4 and Letter are explicit choices. The standard body size stays at 10.5pt. Long experience blocks may split across pages; headings and compact entries are kept together when space permits.

## Checks

The structured builder rejects unresolved markers, invalid Unicode, unsafe link schemes, duplicate/unknown keys, empty required values and invalid collection types. It escapes all supplied text.

The same export checker used by the legacy template verifies page geometry, live extracted text, unresolved markers, selected-posting overlap and the complete expected-text contract. Actual rendered variants must pass for each lane and paper format. Text extraction is also checked in section order.

The default page limit is one; a longer CV needs an explicit approved limit. No local test can promise 100% parsing across ATS platforms. Factual review and visual inspection are still required.

## Compatibility

`template.html` remains the legacy manual layout. `render.sh` remains the checked HTML-to-PDF entrypoint. The new structured command consumes the shared renderer rather than copying it into each lane.
