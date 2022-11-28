"""Web content scraper."""

# Import from standard library
import requests
import random

# Import from 3rd party libraries
from bs4 import BeautifulSoup


class Scraper:
    """Simple web scraper."""

    AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
    ]
    agent = AGENTS[random.randint(0, len(AGENTS) - 1)]

    @staticmethod
    def set_option(options, current):
        """Select next option list element."""
        i = options.index(current)
        return options[0] if i + 1 == len(options) else options[i + 1]

    def switch_agent(self) -> None:
        """Switch to next agent to avoid blocking."""
        self.agent = self.set_option(self.AGENTS, self.agent)

    def request_url(self, url) -> requests.Response:
        """Request URL with agent."""
        try:
            response = requests.get(
                url, headers={"User-Agent": self.agent, "Connection": "close"}
            )
            self.switch_agent()
            return response
        except Exception as exception:
            return exception

    def extract_content(self, html: requests.Response) -> str:
        """Extract plain text from html."""
        soup = BeautifulSoup(html.text, "html.parser")
        elements = [
            element.text for element in soup.find_all(["h1", "h2", "h3", "p"])
            if len(element.text) > 5
        ]
        return "\n\n".join(elements)
