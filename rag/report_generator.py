from rag.ai_assistant import GeminiAssistant


class ReportGenerator:

    def __init__(self):
        self.ai = GeminiAssistant()

    def create_report(
        self,
        package_name,
        documentation,
        github_info,
        web_results
    ):
        return self.ai.generate_report(
            package_name=package_name,
            documentation=documentation,
            github_info=github_info,
            web_results=web_results
        )