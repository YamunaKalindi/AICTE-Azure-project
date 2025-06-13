# The Smart Task Executor

ATES is a Python-based system designed to autonomously execute tasks across multiple environments (Browser, Terminal, File System). It interprets natural language instructions, plans tasks, and generates outputs like text files or PDFs with charts. Built as a deployable project, it showcases web scraping, data processing, and report generation.

## Features
- **Basic Task**: _"Find top 5 AI headlines and save to file"_  
  - Scrapes Google News for AI headlines and saves them to `ai_headlines.txt`.
- **Intermediate Task**: _"Search smartphone reviews, extract pros/cons, create summary"_  
  - Fetches reviews from TechRadar, extracts pros/cons, and saves a formatted summary to `smartphone_reviews.txt`.
- **Advanced Task**: _"Research renewable energy, analyze trends, create PDF with charts"_  
  - Scrapes renewable energy data from Macrotrends, analyzes trends, and generates `renewable_energy_trends.pdf` with a chart.

## Project Structure
```
ATES/
├── src/
│   ├── instruction_parser.py   # Parses user instructions
│   ├── task_planner.py         # Plans task execution steps
│   ├── environments/
│   │   ├── browser.py          # Web scraping with Selenium
│   │   ├── terminal.py         # Data analysis and chart generation
│   │   └── filesystem.py       # File output (text, PDF)
│   ├── integration.py          # Orchestrates environments
│   └── main.py                 # Entry point
├── tests/
│   └── test_all.py             # Basic test case
├── config.yaml                 # Configuration (not fully utilized)
├── .gitignore                  # Ignores venv, output files
└── README.md                   # This file
```

## Prerequisites
- **Python**: 3.9+ (tested on Windows)
- **Chrome Browser**: Required for Selenium
- **ChromeDriver**: Automatically managed by `webdriver-manager`

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd ATES
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment:**
   ```bash
   venv\Scripts\activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install selenium webdriver-manager pandas matplotlib reportlab
   ```

## Usage

To run the system, execute the `main.py` file inside the `src` folder:

```bash
python src/main.py
```

The system will prompt you to enter a task in natural language (e.g.,  
`"Search smartphone reviews, extract pros/cons, and save a summary"`)

It will then:
- Parse your instruction
- Plan the steps needed
- Use appropriate environments (Browser, Terminal, File)
- Generate outputs in the `output/` directory

## Outputs

| Task                    | Output File                   | Format |
|-------------------------|-------------------------------|--------|
| AI Headlines            | `ai_headlines.txt`            | `.txt` |
| Smartphone Reviews      | `smartphone_reviews.txt`      | `.txt` |
| Renewable Energy Trends | `renewable_energy_trends.pdf` | `.pdf` |

## How It Works

### Instruction Parsing
- `instruction_parser.py` interprets the natural language command.

### Task Planning
- `task_planner.py` maps the instruction to a sequence of subtasks.

### Execution
- `browser.py`: Scrapes data from Google News, TechRadar, and Macrotrends.
- `terminal.py`: Analyzes trends using `pandas`, creates charts using `matplotlib`.
- `filesystem.py`: Writes results to `.txt` and `.pdf` using standard I/O and `reportlab`.

### Integration
- `integration.py` coordinates execution across environments.

## Output Files
- `ai_headlines.txt`: Top 5 AI headlines.
- `smartphone_reviews.txt`: Formatted pros/cons and summary.
- `renewable_energy_trends.pdf`: Trend analysis and chart.
- `trend_chart.png`: Temporary chart image used in the PDF.

## Troubleshooting
- **SSL Errors**: Retry or check network connectivity.
- **NoSuchElementException**: Website layout may have changed—update selectors in `browser.py`.
- **Data Format Errors**: Ensure scraped data follows the `Year,Value` format (e.g., `2015,15.34`).

## Future Improvements
- Enhance `config.yaml` for more dynamic control.
- Add better error handling and retry logic.
- Extend support to APIs, databases, and cloud outputs.

## License
This project is licensed under the [MIT License](LICENSE).
