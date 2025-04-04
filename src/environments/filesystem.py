from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

class FileSystemExecutor:
    def execute(self, task, data):
        if "save to" in task:
            filename = task.split("save to ")[1]
            if filename.endswith(".pdf"):
                doc = SimpleDocTemplate(filename, pagesize=letter)
                styles = getSampleStyleSheet()
                story = [Paragraph(line, styles["Normal"]) for line in data]
                if "trend_chart.png" in " ".join(data):
                    story.append(Image("trend_chart.png", width=200, height=150))
                doc.build(story)
            else:
                with open(filename, "w") as f:
                    f.write("\n".join(data))
            return f"Saved to {filename}"
        return "No file operation"