import pandas as pd
import matplotlib.pyplot as plt
import re

class TerminalExecutor:
    def execute(self, task, data):
        if "analyze" in task and "renewable energy" in task:
            try:
                if not data or len(data) == 0:
                    raise ValueError("No data to analyze.")

                # Unified parsing logic (handles both comma and % based data)
                df = None
                trend = "unknown"

                # Case 1: Year,Percentage format (Macrotrends-style or fallback)
                if all("," in d and re.match(r"\d{4},\d", d) for d in data):
                    years = []
                    percentages = []
                    for row in data:
                        year, value = row.strip().split(",")
                        years.append(int(year.strip()))
                        percentages.append(float(value.strip()))
                    df = pd.DataFrame({"Year": years, "Renewable %": percentages}).sort_values("Year")
                    trend = "growing" if df["Renewable %"].iloc[-1] > df["Renewable %"].iloc[0] else "declining"

                # Case 2: State,Installed,Potential format (India RE installed vs potential)
                elif all("," in d and len(d.split(",")) == 3 for d in data):
                    states, installed, potential = zip(*[d.split(",") for d in data])
                    df = pd.DataFrame({
                        "State": [s.strip() for s in states],
                        "Installed (MW)": [float(i.strip()) for i in installed],
                        "Potential (MW)": [float(p.strip()) for p in potential],
                    })
                    trend = "growing" if df["Installed (MW)"].sum() / df["Potential (MW)"].sum() >= 0.5 else "underutilized"

                else:
                    raise ValueError("Unsupported data format for analysis.")

                # Plotting
                plt.figure(figsize=(10, 6))
                chart_path = "trend_chart.png"

                if "Year" in df.columns:
                    df.plot(x="Year", y="Renewable %", kind="line", marker='o', legend=False)
                    plt.ylabel("Renewable Energy (%)")
                else:
                    df.plot(x="State", y=["Installed (MW)", "Potential (MW)"], kind="bar")
                    plt.ylabel("Capacity (MW)")

                plt.title("Renewable Energy Trend Analysis")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.savefig(chart_path)
                plt.close()

                return [
                    f"Trend: Renewable energy is {trend}",
                    f"Data:\n{df.to_string(index=False)}",
                    f"Chart saved as {chart_path}"
                ]

            except Exception as e:
                print("Analysis failed:", e)
                return ["Error in analysis", f"Details: {str(e)}"]

        # Default case: Print data line by line
        return [f"{i+1}. {line}" for i, line in enumerate(data)]
