# Interview Transcript Summarizer

A small CLI script that reads an interview transcript and returns a structured summary with topics covered, a candidate profile, and a short candidate summary.

## Setup

- Python 3.9+
- Install dependency:
  - `pip install openai`

### API key

Set your Azure OpenAI API key as an environment variable (recommended):

PowerShell:
```
$env:AZURE_OPENAI_API_KEY = "YOUR_API_KEY"
$env:AZURE_OPENAI_ENDPOINT = "https://YOUR-RESOURCE.cognitiveservices.azure.com/"
$env:AZURE_OPENAI_DEPLOYMENT = "gpt-5.4-pro"
$env:AZURE_OPENAI_API_VERSION = "2025-04-01-preview"
```

Or create a `.env` file in the repo root:
```
AZURE_OPENAI_API_KEY=YOUR_API_KEY
AZURE_OPENAI_ENDPOINT=https://YOUR-RESOURCE.cognitiveservices.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-5.4-pro
AZURE_OPENAI_API_VERSION=2025-04-01-preview
```

## Run

```
python summarizer.py sample_transcript_assignment_1.txt
python summarizer.py sample_transcript_assignment_2.txt
```

Optional flags:
```
python summarizer.py sample_transcript_assignment_1.txt --endpoint https://YOUR-RESOURCE.cognitiveservices.azure.com --deployment gpt-5.4-pro --api-version 2025-04-01-preview
```

## LLM provider and model

- Provider: Azure OpenAI
- Deployment: gpt-5.4-pro

## Reflection (short)

What surprised me was how much the output quality depended on strict structure and grounding rules rather than model choice. With a loose prompt, the model drifted into extra narrative and implied seniority without evidence. With a stricter JSON schema and explicit instructions for handling missing info, the summaries became consistent and easier to parse.

Given another day, I would add a second pass that extracts evidence snippets for each topic and the profile justification, then validate the output against a JSON schema. The main limitation of the current prompt is that it can still make mild inferences (for example, role level) when the transcript does not explicitly state them.
