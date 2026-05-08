import argparse
import json
import os
import sys
from typing import Optional


def load_dotenv(path: str = ".env") -> None:
    if not os.path.isfile(path):
        return

    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def build_prompt(transcript: str) -> str:
    return (
        "You are a careful interview transcript summarizer.\n"
        "Your task is to produce a structured summary with three parts:\n"
        "1) topics_covered: 3-8 short strings describing the main themes.\n"
        "2) profile: an object with role, level, and justification fields.\n"
        "3) candidate_summary: 3-6 sentences summarizing background, strengths, concerns, and overall impression.\n\n"
        "Rules:\n"
        "- Use only information from the transcript. Do not invent facts.\n"
        "- If information is missing, say 'Unknown' or 'Not enough info'.\n"
        "- Keep language concise and professional.\n"
        "- Output valid JSON only. No code fences. No extra text.\n\n"
        "Transcript:\n"
        f"{transcript}\n"
    )


def normalize_endpoint(endpoint: str) -> str:
    endpoint = endpoint.strip()
    if not endpoint:
        return endpoint

    endpoint = endpoint.split("?", 1)[0]
    if "/openai/" in endpoint:
        endpoint = endpoint.split("/openai/", 1)[0]
    return endpoint.rstrip("/")


def extract_text(response: object) -> str:
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text.strip()

    try:
        output = []
        for item in response.output:
            if not hasattr(item, "content"):
                continue
            for part in item.content:
                text = getattr(part, "text", None)
                if text:
                    output.append(text)
        return "".join(output).strip()
    except Exception:
        return ""


def try_parse_json(text: str) -> Optional[object]:
    # Try stripping potential markdown code blocks first
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    if cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def generate_summary(
    transcript: str,
    endpoint: str,
    api_key: str,
    deployment: str,
    api_version: str,
    max_output_tokens: int,
    temperature: float = None,
) -> str:
    try:
        from openai import AzureOpenAI
    except ImportError:
        print("Missing dependency: pip install openai", file=sys.stderr)
        sys.exit(1)

    if not endpoint:
        print("Missing AZURE_OPENAI_ENDPOINT. Set it in the environment or pass --endpoint.", file=sys.stderr)
        sys.exit(1)

    if not api_key:
        print("Missing AZURE_OPENAI_API_KEY. Set it in the environment or a .env file.", file=sys.stderr)
        sys.exit(1)

    if not deployment:
        print("Missing AZURE_OPENAI_DEPLOYMENT. Set it in the environment or pass --deployment.", file=sys.stderr)
        sys.exit(1)

    endpoint = normalize_endpoint(endpoint)
    prompt = build_prompt(transcript)
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )

    response = client.responses.create(
        model=deployment,
        input=prompt,
        max_output_tokens=max_output_tokens,
    )

    text = extract_text(response)
    if not text:
        print("No text returned from model.", file=sys.stderr)
        sys.exit(1)

    parsed = try_parse_json(text)
    if parsed is not None:
        return json.dumps(parsed, indent=2, ensure_ascii=True)

    print("Warning: model output was not valid JSON. Printing raw output.", file=sys.stderr)
    return text


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Summarize an interview transcript with Azure OpenAI.")
    parser.add_argument("transcript_path", help="Path to the transcript .txt file")
    parser.add_argument(
        "--endpoint",
        default=os.getenv("AZURE_OPENAI_ENDPOINT"),
        help="Azure OpenAI endpoint (e.g., https://your-resource.cognitiveservices.azure.com)",
    )
    parser.add_argument(
        "--deployment",
        default=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        help="Azure OpenAI deployment name (e.g., gpt-5.4-pro)",
    )
    parser.add_argument(
        "--api-version",
        default=os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview"),
        help="Azure OpenAI API version (default: 2025-04-01-preview)",
    )
    parser.add_argument("--max-output-tokens", type=int, default=2000)
    args = parser.parse_args()

    if not os.path.isfile(args.transcript_path):
        print(f"File not found: {args.transcript_path}", file=sys.stderr)
        sys.exit(1)

    with open(args.transcript_path, "r", encoding="utf-8") as handle:
        transcript = handle.read().strip()

    if not transcript:
        print("Transcript file is empty.", file=sys.stderr)
        sys.exit(1)

    output = generate_summary(
        transcript=transcript,
        endpoint=args.endpoint,
        api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
        deployment=args.deployment,
        api_version=args.api_version,
        max_output_tokens=args.max_output_tokens,
    )

    print(output)


if __name__ == "__main__":
    main()
