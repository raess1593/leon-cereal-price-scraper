from bs4 import BeautifulSoup
import requests
from random import choice

class ScraperBot():
    """Fetch and parse the cereal market table from the target webpage."""

    def __init__(self):
        # Rotate browser user agents to reduce basic bot filtering.
        self.session = requests.Session()
        self.headers = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0"
        ]
        self.session.headers.update({"User-Agent": choice(self.headers)})

    def extract_raw(self, url: str) -> dict:
        """Return raw table rows keyed by cereal label, or None on failure."""

        try:
            print(f"Bot is in {url}")
            response = self.session.get(url, timeout=4)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            if not table:
                return None
            rows = table.find_all("tr")
            data = {}
            for row in rows:
                # Normalize row text into a predictable list-based payload.
                temp = row.get_text(separator="|").split(sep="|") 
                temp = list(filter(lambda x: x != '\n', temp))
                cereal = temp[0] 
                data[cereal] = temp[2:-1]
            return data
        except:
            return None

    def close(self):
        """Close the HTTP session explicitly to release network resources."""
        self.session.close()

if __name__ == "__main__":
    bot = ScraperBot()
    bot.extract_raw("https://www.lonjadeleon.es/lonja-de-cereal-25-03-2026")
    print()
    print()
    bot.extract_raw("https://www.lonjadeleon.es/lonja-de-cereales-07-06-2023")