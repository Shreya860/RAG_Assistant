from rag.report_generator import ReportGenerator

generator = ReportGenerator()

report = generator.create_report(
    package_name="numpy",
    docs="Official docs say NumPy supports fast numerical arrays.",
    github="290k stars, active repository, latest commit 3 days ago.",
    web="No major security issues reported recently."
)

print(report)