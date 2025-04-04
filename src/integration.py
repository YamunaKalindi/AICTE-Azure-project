from src.environments.browser import BrowserExecutor
from src.environments.terminal import TerminalExecutor
from src.environments.filesystem import FileSystemExecutor


class IntegrationLayer:
    def __init__(self):
        self.browser = BrowserExecutor()
        self.terminal = TerminalExecutor()
        self.filesystem = FileSystemExecutor()

    def run(self, plan, parsed):
        data = None
        report = [f"Task: {parsed['target']}"]
        for step in plan:
            env = step["env"]
            task = step["task"]
            try:
                if env == "browser":
                    data = self.browser.execute(task)
                elif env == "terminal":
                    data = self.terminal.execute(task, data)
                elif env == "filesystem":
                    result = self.filesystem.execute(task, data)
                    report.append(result)
                report.append(f"{env.capitalize()} task '{task}' completed")
            except Exception as e:
                report.append(f"Error in {env}: {str(e)}")
        self.browser.close()
        return "\n".join(report)