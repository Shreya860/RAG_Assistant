from rag.ai_assistant import GeminiAssistant


class ReportGenerator:

    def __init__(self):
        self.ai = GeminiAssistant()

    def create_report(
        self,
        package_name,
        docs,
        github,
        web
    ):
        return self.ai.generate_report(
            package_name,
            docs,
            github,
            web
        )