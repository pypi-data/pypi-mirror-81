from crawliexpress.exceptions import CrawliexpressException
from crawliexpress.feedback import Feedback

from bs4 import BeautifulSoup
import re


class FeedbackPage:
    feedbacks = None
    page = None
    known_pages = None

    def from_html(self, html):
        soup = BeautifulSoup(html, "lxml")

        # feedbacks
        feedbacks = self.feedbacks = list()
        for node in soup.find_all("", class_="feedback-item"):
            feedback = Feedback()
            feedback.from_node(node)
            feedbacks.append(feedback)

        # page
        node_pages = soup.find("", class_="ui-pagination-navi")
        if node_pages is None:
            raise CrawliexpressException("could not find pagination node")

        node_page = node_pages.find("", class_="ui-pagination-active")
        if node_page is None:
            raise CrawliexpressException("could not find current page")
        page = node_page.text
        if re.match(r"^\d+$", page) is None:
            raise CrawliexpressException("current page is not a number")
        self.page = int(page)

        # pages
        known_pages = self.known_pages = list()
        for node_page in node_pages.find_all("", class_="ui-goto-page"):
            page = node_page.text
            if re.match(r"^\d+$", page) is not None:
                known_pages.append(int(page))

    def has_next_page(self):
        has = False
        for page in self.known_pages:
            if page >= self.page:
                has = True
                break

        return has

    def __iter__(self):
        yield "feedbacks", [dict(feedback) for feedback in self.feedbacks]
        yield "page", self.page
        yield "known_pages", self.known_pages
        yield "has_next_page", self.has_next_page()
