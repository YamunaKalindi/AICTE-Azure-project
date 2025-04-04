import sys
from src.instruction_parser import InstructionParser
from src.task_planner import TaskPlanner
from src.integration import IntegrationLayer

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m src.main '<instruction>'")
        return

    instruction = sys.argv[1]
    
    parser = InstructionParser()
    planner = TaskPlanner()
    integrator = IntegrationLayer()

    parsed = parser.parse(instruction)
    plan = planner.plan(parsed)
    report = integrator.run(plan, parsed)
    print(f"Task Report:\n{report}")

if __name__ == "__main__":
    main()
