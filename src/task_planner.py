class TaskPlanner:
    def plan(self, parsed):
        plan = []
        if "extract" in parsed["action"] or "search" in parsed["action"]:
            plan.append({"env": "browser", "task": f"fetch {parsed['target']}"})
        if "extract_details" in parsed["action"]:
            plan.append({"env": "browser", "task": f"extract pros/cons from {parsed['target']}"} )
        if "analyze" in parsed["action"]:
            plan.append({"env": "terminal", "task": f"analyze {parsed['target']}"} )
        if "summarize" in parsed["action"]:
            plan.append({"env": "terminal", "task": f"summarize {parsed['target']}"} )
        if "save" in parsed["action"]:
            filename = f"{parsed['target'].replace(' ', '_')}.{parsed['format']}"
            plan.append({"env": "filesystem", "task": f"save to {filename}"})

        print("Planned tasks:", plan)  # ✅ Add this for debugging
        return plan
