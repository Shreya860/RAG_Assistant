import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiAssistant:

    def __init__(self, api_key=None):
        api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key)

    def generate_report(
        self,
        package_name,
        documentation,
        github_info,
        web_results
    ):

        prompt = f"""
You are an expert Open Source Dependency Security Auditor.

Analyze the package below.

PACKAGE
{package_name}

OFFICIAL DOCUMENTATION
{documentation}

GITHUB INFORMATION
{github_info}

WEB SEARCH
{web_results}

Generate a professional report.

Use exactly these headings:

## Summary

## Security Risks

## Maintenance Status

## Community Popularity

## Recommendation

## Risk Score (0-10)

Give clear reasoning.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text