# MockIT Ideathon Demo MVP

MockIT is a front-end demo MVP for an AI-assisted recruiting platform built for an ideathon.

The project demonstrates the recruiter journey from onboarding to candidate review, interview workflow, reporting, and billing through a connected multi-page interface.

## Project Overview

MockIT is a recruiter-focused hiring workspace concept designed to reduce manual screening time and make evaluation more structured.

The demo covers:

- recruiter onboarding
- workspace setup
- vacancy management
- candidate review
- AI-style resume analysis
- live interview support
- final summary reporting
- billing and subscription overview

## Problem

Recruiting teams often lose time across multiple disconnected steps:

- manual screening takes too long
- interview quality is inconsistent
- hiring managers and recruiters are not always aligned
- candidate evaluation is often subjective
- reporting is fragmented across tools

## Solution

MockIT brings the hiring workflow into one product experience:

- guided onboarding for recruiters
- structured hiring workflow setup
- vacancy and pipeline visibility
- AI-assisted candidate analysis
- live interview workspace with structured notes
- summary reporting for decision making
- billing visibility for team usage

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

## Tech Stack

- HTML
- CSS
- Vanilla JavaScript
- localStorage for demo state persistence

## Current Scope

This ideathon version is intentionally focused on the front-end and product flow.

What is already implemented:

- connected multi-page product flow
- consistent UI across onboarding and recruiter workspace
- lightweight demo interactivity
- local state persistence across screens

What is planned next:

- React migration
- backend/API layer
- authentication
- database storage
- real AI integrations
- production-ready billing and analytics

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

## Key Demo Highlights

- `welcome.html` shows the onboarding setup experience
- `vacancies.html` demonstrates recruiter vacancy management
- `resume-analysis.html` shows AI-assisted candidate review
- `live-workspace.html` simulates a live interview workflow
- `summary-report.html` closes the loop with a hiring recommendation

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

## Future Improvements

- convert the multi-page static flow into a React application
- connect onboarding and candidate flows to a backend
- add real auth and user roles
- support real resume upload and parsing
- connect AI analysis and scoring to production APIs
- add persistent recruiter and vacancy data
