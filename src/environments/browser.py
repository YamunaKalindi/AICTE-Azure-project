from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from collections import Counter
import re

class BrowserExecutor:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")  
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(options=options)

    def close_popup(self):
        """Attempts to close cookie popups and overlays."""
        try:
            time.sleep(2)  
            popup_buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
            for button in popup_buttons:
                if "accept" in button.text.lower() or "close" in button.text.lower():
                    button.click()
                    print("Closed popup!")
                    time.sleep(1)
                    break  
        except Exception as e:
            print("No popup found or failed to close:", e)

    def execute(self, task):
        """Handles tasks dynamically."""
        if "fetch smartphone reviews" in task:
            return self.fetch_smartphone_reviews()
        elif "extract pros/cons" in task:
            return self.extract_pros_cons()
        elif "summarize smartphone reviews" in task:
            return self.summarize_reviews()
        elif "fetch" in task:
            topic = task.split("fetch ")[1]
            if "renewable energy" in topic:
                return self.fetch_renewable_energy_data()
            else:
                return self.fetch_news_headlines(topic)
        else:
            print("Invalid task:", task)
            return None

    def fetch_smartphone_reviews(self):
        """Fetches top smartphone review links from TechRadar."""
        print("Opening TechRadar review page...")
        self.driver.get("https://www.techradar.com/phones/reviews")
        time.sleep(5)  
        self.close_popup()

        try:
            review_links = self.driver.find_elements(By.CSS_SELECTOR, "a.article-link")[:5]
            review_urls = [link.get_attribute("href") for link in review_links if link.get_attribute("href")]

            if not review_urls:
                print("No review links found!")
                return []

            return review_urls

        except Exception as e:
            print("Error fetching review links:", e)
            return []

    def extract_pros_cons(self):
        """Extracts pros and cons from TechRadar smartphone reviews."""
        review_urls = self.fetch_smartphone_reviews()  

        all_pros, all_cons = [], []

        for url in review_urls:
            self.driver.get(url)
            time.sleep(3)  
            self.close_popup()

            try:
                pros_section = self.driver.find_element(By.CSS_SELECTOR, "div.pretty-verdict__pros ul")
                cons_section = self.driver.find_element(By.CSS_SELECTOR, "div.pretty-verdict__cons ul")

                pros = [p.text.strip() for p in pros_section.find_elements(By.TAG_NAME, "li")]
                cons = [c.text.strip() for c in cons_section.find_elements(By.TAG_NAME, "li")]

                all_pros.extend(pros)
                all_cons.extend(cons)

            except Exception as e:
                print(f"Failed to extract pros/cons from {url}:", e)

        return {"pros": all_pros or ["No pros found"], "cons": all_cons or ["No cons found"]}

    def summarize_reviews(self):
        """Summarizes extracted smartphone review pros and cons with frequency analysis."""
        extracted_data = self.extract_pros_cons()

        if not extracted_data:
            return "No data extracted."

        pros = extracted_data.get("pros", [])
        cons = extracted_data.get("cons", [])

        # Format output for better readability
        pros_summary = f"Pros:\n" + "\n".join(f"+ {p}" for p in pros)
        cons_summary = f"Cons:\n" + "\n".join(f"- {c}" for c in cons)

        # Frequency analysis for key terms
        key_terms = ["performance", "battery", "charging", "display", "camera", "heat", "software"]
        all_words = " ".join(pros + cons).lower().split()
        term_counts = Counter(word for word in all_words if word in key_terms)

        if term_counts:
            most_frequent = term_counts.most_common(2)
            frequent_summary = "\nMost mentioned aspects:\n" + "\n".join(f"- {k}: {v} times" for k, v in most_frequent)
        else:
            frequent_summary = "\nNo dominant terms found."

        summary = f"{pros_summary}\n\n{cons_summary}\n{frequent_summary}"

        print("Summarization complete!")
        return summary

    def save_summary(self):
        """Saves the summarized smartphone reviews to a text file with better formatting."""
        summary = self.summarize_reviews()

        if summary.strip():  # Ensure the file isn't empty
            try:
                with open("smartphone_reviews.txt", "w", encoding="utf-8") as f:
                    f.write(summary)
                print("Saved to smartphone_reviews.txt")
            except Exception as e:
                print("Error saving file:", e)
        else:
            print("No content to save!")

    def fetch_news_headlines(self, topic):
        """Fetches news headlines for a given topic from Google News."""
        print(f"Fetching headlines for: {topic}")
        self.driver.get("https://news.google.com")
        try:
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Search for topics, locations & sources']"))
            )
            search_box.send_keys(topic + " 2025")
            search_box.send_keys(Keys.ENTER)
            time.sleep(5)
            headline_elements = self.driver.find_elements(By.CSS_SELECTOR, "a.JtKRv")
            headlines = [h.text.strip() for h in headline_elements if h.text.strip()]
            return headlines[:5] if headlines else ["No headlines found!"]
        except Exception as e:
            print("Search failed:", e)
            return []

    def fetch_renewable_energy_data(self):
        """Fetches renewable energy trend data from macrotrends.net."""
        print("Fetching renewable energy trends from macrotrends.net...")
        self.driver.get("https://www.macrotrends.net/global-metrics/countries/ind/india/renewable-energy-statistics")
        time.sleep(5)
        self.close_popup()

        try:
            # Find the <ul> containing the data points
            ul_element = self.driver.find_element(By.CSS_SELECTOR, "ul[style='margin-top:10px;']")
            list_items = ul_element.find_elements(By.TAG_NAME, "li")

            # Parse each <li> using regex
            trend_data = []
            for item in list_items[:5]:  # Limit to 5 years
                text = item.text.strip()
                match = re.search(r"(\d{4})\s+was\s+([\d.]+)%", text)
                if match:
                    year, value = match.groups()
                    trend_data.append(f"{year},{value}")
                else:
                    print("Skipping invalid line:", text)

            if not trend_data:
                print("No trend data found, using dummy data.")
                return ["2023,20", "2024,25", "2025,30"]

            return trend_data

        except Exception as e:
            print("Failed to fetch renewable energy data:", e)
            return ["2023,20", "2024,25", "2025,30"]  # Fallback dummy data


    def close(self):
        """Close the browser if it's still open."""
        if self.driver.service.process is not None:
            self.driver.quit()

# Run the script
if __name__ == "__main__":
    executor = BrowserExecutor()

    # Fetch and save smartphone reviews
    executor.save_summary()

    executor.close()