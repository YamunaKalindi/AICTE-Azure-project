import re

class InstructionParser:
   def parse(self, instruction):
        instruction = instruction.lower()
        parsed = {"action": [], "target": None, "output": None, "format": "text"}

        # Detect actions
        if "find" in instruction:
            parsed["action"].append("extract")
        if "search" in instruction:
            parsed["action"].append("search")
        if "extract" in instruction:
            parsed["action"].append("extract_details")  # For pros/cons
        if "analyze" in instruction:
            parsed["action"].append("analyze")
        if "create" in instruction or "save" in instruction:
            parsed["action"].append("save")
        if "summary" in instruction:
            parsed["action"].append("summarize")

        # Extract target
        if "headlines" in instruction:
            parsed["target"] = "AI headlines"
            parsed["count"] = int(re.search(r"top (\d+)", instruction).group(1)) if "top" in instruction else 5
        elif "reviews" in instruction:
            parsed["target"] = "smartphone reviews"  # ✅ This is correctly detected
        elif "renewable energy" in instruction:
            parsed["target"] = "renewable energy trends"

        # Determine output and format
        if "file" in instruction:
            parsed["output"] = "file"
        if "summary" in instruction:
            parsed["output"] = "summary"
        if "pdf" in instruction:
            parsed["output"] = "pdf"
            parsed["format"] = "pdf"
        if "charts" in instruction:
            parsed["features"] = ["charts"]

        print("Parsed instruction:", parsed)  # ✅ Add this for debugging
        return parsed

    
    # "Find top 5 AI headlines and save to file"
    # "Search smartphone reviews, extract pros/cons, create summary"
    # "Research renewable energy, analyze trends, create PDF with charts"