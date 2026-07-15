from rag.report_generator import ReportGenerator

generator = ReportGenerator()

report = generator.create_report(
    package_name="numpy",
    documentation="Official docs say NumPy supports fast numerical arrays.",
    github_info="290k stars, active repository, latest commit 3 days ago.",
    web_results="No major security issues reported recently."
)

print(report)