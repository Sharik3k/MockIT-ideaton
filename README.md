# MockIT Ideathon Demo MVP

MockIT is a front-end demo MVP for an AI-assisted recruiting platform built for an ideathon.

The project demonstrates the recruiter journey from onboarding to candidate review, interview workflow, reporting, and billing through a connected multi-page interface.

## What This Demo Includes

- Landing page
- Login flow
- Recruiter onboarding flow
- Dashboard
- Vacancies management
- Candidate profile
- Resume analysis
- Live interview workspace
- Interview summary report
- Billing and usage

## Demo Nature

This repository is a front-end MVP and clickable demo.

It includes:

- static HTML pages
- shared CSS styling
- lightweight JavaScript demo interactions
- local state persistence for demo flow

It does not yet include:

- real backend integration
- production authentication
- database persistence
- actual AI processing
- live billing infrastructure

## Project Files

- [index.html](./index.html)
- [login.html](./login.html)
- [welcome.html](./welcome.html)
- [company.html](./company.html)
- [hiring.html](./hiring.html)
- [invite.html](./invite.html)
- [dashboard.html](./dashboard.html)
- [vacancies.html](./vacancies.html)
- [candidate-overview.html](./candidate-overview.html)
- [resume-analysis.html](./resume-analysis.html)
- [live-workspace.html](./live-workspace.html)
- [summary-report.html](./summary-report.html)
- [billing.html](./billing.html)
- [styles.css](./styles.css)
- [script.js](./script.js)

## Recommended Demo Flow

1. `login.html`
2. `welcome.html`
3. `company.html`
4. `hiring.html`
5. `invite.html`
6. `dashboard.html`
7. `vacancies.html`
8. `candidate-overview.html`
9. `resume-analysis.html`
10. `live-workspace.html`
11. `summary-report.html`
12. `billing.html`

## Run Locally

You can open the files with any local static server.

Example:

```bash
python3 -m http.server 4173
```

Then open:

```text
http://localhost:4173/login.html
```

If you use VS Code, Live Server also works.

## Notes

- Demo interactions are implemented in `script.js`
- Styling is centralized in `styles.css`
- Some visual sections use PNG assets exported from design references

