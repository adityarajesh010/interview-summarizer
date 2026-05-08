# Interview Transcript Summarizer

A Python-based CLI and web application that processes raw interview transcripts and extracts a structured JSON summary (topics covered, candidate profile, and editorial summary) using Azure OpenAI (gpt-5.4-pro).

## Architecture & Tech Stack
- **Backend**: Flask + Python. Exposes a single /api/summarize REST endpoint. Uses the official openai Python SDK.
- **Frontend**: Vanilla HTML/JS and Tailwind CSS. The UI is based on a pre-existing "Newsprint" design system template I had on hand. Hooking it up to the API took barely a single prompt.
- **Prompting Strategy**: Zero-shot prompt enforcing strict JSON output. We parse the Responses API output and use custom logic to strip markdown code fences to ensure reliable decoding, since we aren't enforcing Structured Outputs (yet).

## Setup Instructions

1. **Install dependencies:**
   `powershell
   python -m venv .venv
   .venv\Scripts\activate
   pip install openai flask python-dotenv
   `

2. **Environment Variables:**
   Create a .env file in the project root. **Do NOT commit this file.**
   `ini
   AZURE_OPENAI_API_KEY=your_production_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
   AZURE_OPENAI_DEPLOYMENT=gpt-5.4-pro
   AZURE_OPENAI_API_VERSION=2025-04-01-preview
   `

3. **Run the application:**
   - **Web UI Mode**: python app.py (then navigate to http://127.0.0.1:5000)
   - **CLI Mode**: python summarizer.py sample_transcript_assignment_1.txt

## Reflections & Limitations

The core challenge was preventing the LLM from outputting conversational filler and hallucinating seniority levels not present in the text. Enforcing a strict JSON schema and explicit "do not infer" rules within the prompt solved the formatting consistency issues.

One technical hurdle encountered was the Azure OpenAI Responses endpoint for the newer gpt-5.4-pro model—it explicitly rejects the 	emperature parameter, which required a small SDK code adjustment. In a production scenario, I would swap the raw JSON parsing out for Pydantic using OpenAI's Structured Outputs, mapping the exact object shape natively.
