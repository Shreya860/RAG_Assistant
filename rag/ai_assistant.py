import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class GeminiAssistant:

    def __init__(self):
        self.client = client

    def generate_report(
        self,
        package_name,
        documentation,
        github_info,
        web_results
    ):

        prompt = f"""
You are an expert Open Source Dependency Auditor.

Use ONLY the information provided below.

PACKAGE
{package_name}

LOCAL DOCUMENTATION
{documentation}

GITHUB METRICS
{github_info}

LIVE WEB SEARCH
{web_results}

Generate a report with the following headings:

## Summary

## Security Risks

## Maintenance Status

## Community Popularity

## Recommendation

## Risk Score (0-10)

If information is unavailable, explicitly state that it is unavailable.
Do not invent facts.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text