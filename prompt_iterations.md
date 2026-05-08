# Prompt Iterations

## Iteration 1

### Prompt
```
You are an interview summarizer. Read the transcript and provide:
1) Topics covered
2) Candidate profile
3) Candidate summary
Keep it brief.

Transcript:
[EXCERPT]
```

### Input (excerpt)
```
[13:06] Candidate: Hi sir. My name is Prasanna Kumar. I have around nine plus years of experience in software development. My core technical expertise is on Angular, React and Ionic framework. I'm working with the backend by using Node.js, Express and .NET Core.
[27:41] Candidate: Feature based reusable components. Feature modules like dashboard, reports, settings. Reusable components like cards, data table list, filters and loaders for lazy loading.
[30:52] Candidate: Mobile optimization — reduce bundle size, optimizing images, avoiding unnecessary plugins. Testing — emulators or mobile devices.
[44:59] Candidate: Modular architecture. Core principles — separation of folders, lazy loading for scalability, reusable shared components. Data flow between state management.
[53:51] Candidate: Splitting state. Global state — session, users token, theme preferences. Server state — data from back end, caching and re-fetching. Local UI state — component level, forms and modals.
```

### Output
```
Topics:
- AI-assisted coding workflow
- Ionic UI architecture and performance
- Capacitor plugins for camera and storage
- Tailwind-based design system approach
- Angular enterprise app structure
- React state management basics

Profile:
Senior Mobile/Frontend Engineer (Ionic/Angular/React)

Candidate summary:
Prasanna Kumar has 9+ years of experience focused on Ionic, Angular, and React with some backend exposure. He describes practical use of AI assistants for scaffolding forms, services, and state management. He emphasizes performance tactics like lazy loading and virtual scrolling for large datasets. He appears strongest in hybrid mobile architecture and reusable component design. He was less confident on some code-level details.
```

### What worked / what didn't
The high-level themes were captured, but the output was too free-form and hard to parse. It also inferred "senior" without explicit justification. I needed a stricter structure and an instruction to avoid speculation.

---

## Iteration 2

### Prompt
```
Summarize the interview transcript into three sections:
- Topics covered (bullet list)
- Profile (role + level + 1-sentence justification)
- Candidate summary (3-5 sentences)

Rules:
- Use only information from the transcript.
- If details are missing, say "Not enough info".
- Keep the summary concise and professional.

Transcript:
[EXCERPT]
```

### Input (excerpt)
```
[5:28] Candidate: From scratch to ISO certification. Building a CRM, drafting KRAs and KPIs, building dashboard for fraud detection.
[16:05] Candidate: I built my own score by giving weightages. Identified PIN codes from past data where customers pay one EMI and leave.
[19:30] Candidate: First, market research. Found minimum 4 to 5 vendors. Take feedback on efficiency, timely delivery, data security.
[27:33] Candidate: Initially I connect with all three teams. Understand requirement raised by business team. Break down into phases.
[36:25] Candidate: For sales team — number of hours active on dialer, working hours, connected talk time, effective calls more than 3 or 5 minutes.
```

### Output
```
Topics covered:
- Fraud detection program design and analytics
- CRM implementation and dashboarding
- Vendor onboarding and performance management
- Cross-team delivery and timeline management
- BPO/calling process optimization
- KPI tracking and executive reporting

Profile:
Program/Operations Manager - mid-level. Justification: Led end-to-end ops initiatives, vendor onboarding, and analytics-driven process improvements.

Candidate summary:
Krishna has a mechanical engineering background and moved into ed-tech operations in 2019. He led fraud detection initiatives, built CRM processes, and created dashboards and KPIs for leadership. He described vendor research, onboarding, and handling underperformance, as well as dialing process improvements. He appears strong in execution and stakeholder coordination. Communication clarity may be a concern based on the interviewer's feedback.
```

### What worked / what didn't
The sectioned output was easier to read, and the "no speculation" rule reduced hallucinations. However, the format still varied slightly and was not machine-parseable. I wanted a strict JSON schema for reliability and to avoid any extra text.

---

## Iteration 3 (final)

### Prompt
```
You are a careful interview transcript summarizer.
Your task is to produce a structured summary with three parts:
1) topics_covered: 3-8 short strings describing the main themes.
2) profile: an object with role, level, and justification fields.
3) candidate_summary: 3-6 sentences summarizing background, strengths, concerns, and overall impression.

Rules:
- Use only information from the transcript. Do not invent facts.
- If information is missing, say "Unknown" or "Not enough info".
- Keep language concise and professional.
- Output valid JSON only. No code fences. No extra text.

Transcript:
[EXCERPT]
```

### Input (excerpt)
```
[5:28] Candidate: From scratch to ISO certification. Building a CRM, drafting KRAs and KPIs, building dashboard for fraud detection.
[13:42] Candidate: I connected with Experian and CIBIL for credit score. Integrated with our app.
[21:24] Candidate: If a vendor is not giving timely reports... we went for alternate option and hired them.
[38:30] Candidate: Weekly business reviews, monthly business reviews — executive dashboards showing revenue, target achievement, refunds, customers retained.
[61:59] Interviewer: You use lot of jargons in Hindi... in leadership round, they look at confidence.
```

### Output
```json
{
  "topics_covered": [
    "fraud detection and prevention program design",
    "CRM and dashboard implementation",
    "vendor onboarding and underperformance handling",
    "stakeholder alignment and prioritization",
    "BPO/calling process optimization",
    "KPI tracking and executive reporting"
  ],
  "profile": {
    "role": "Program/Operations Manager",
    "level": "Mid-level",
    "justification": "Led end-to-end ops initiatives, vendor management, and analytics-driven process improvements in ed-tech operations."
  },
  "candidate_summary": "Krishna has a mechanical engineering background and moved into ed-tech operations in 2019, covering finance operations and fraud prevention. He describes end-to-end delivery experience, vendor research and onboarding, and building CRM workflows and dashboards. Strengths include process design, stakeholder management, and operational analytics. A concern is communication clarity and confidence at senior leadership levels, as noted by the interviewer. Overall, he fits a mid-level program or operations management role focused on execution."
}
```

### What worked / what didn't
The strict JSON schema made the output consistent and easy to parse. Explicit rules reduced speculation and kept summaries concise. I validated the same prompt on the technical transcript as well, and it produced consistent structure without drifting into extra narrative.
