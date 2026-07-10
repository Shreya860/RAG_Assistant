from rag.ai_assistant import GeminiAssistant

assistant = GeminiAssistant()

documentation = """
NumPy provides multidimensional arrays.
"""

github = """
Stars: 290000
Forks: 19000
Last Commit: 3 days ago
"""

web = """
No recent critical vulnerabilities.
"""

report = assistant.generate_report(
    package_name="numpy",
    documentation=documentation,
    github_info=github,
    web_results=web
)

print(report)