import json
import logging
from itertools import islice

import feedparser
from Entry import Entry
from Logging import logging_decorator


class Handler:
    """class for handling different options: --version, --json, --limit Limit"""
    @logging_decorator
    def __init__(self, source: str, limit: int, version: float):
        self.source = source
        self.limit = limit
        self.version = version
        self.parsed = feedparser.parse(self.source)
        logging.info("Handler object created")

    # options of command line:
    @logging_decorator
    def option_version(self) -> None:
        print("version ", self.version)

    @logging_decorator
    def option_json(self) -> None:
        for entry in islice(self.gen_entries(), 0, self.limit):
            self.print_to_json(self.convert_to_dict(entry))

    @logging_decorator
    def option_default(self) -> None:
        self.print_feed()
        for entry in islice(self.gen_entries(), 0, self.limit):
            entry.print_title()
            entry.print_date()
            entry.print_link()
            entry.print_summary()
            entry.print_links()

    @logging_decorator
    def gen_entries(self) -> Entry:
        """generation instances of Entry class for farther handling them"""
        for ent in self.parsed.entries:
            entry = Entry(ent.title, ent.published, ent.link, ent.summary, tuple([link["href"] for link in ent.links]))
            yield entry

    @logging_decorator
    def print_feed(self) -> None:
        logging.info("function \"print_feed\" started")
        print("Feed: ", self.parsed.feed.title, '\n')
        logging.info("function \"print_feed\" finished")

    @logging_decorator
    def print_to_json(self, obj: dict) -> None:
        print(json.dumps(obj, indent=2))

    @logging_decorator
    def convert_to_dict(self, entry: Entry) -> dict:
        entry_dict = {
            "Feed": self.parsed.feed.title,
            "Title": entry.title,
            "Date": entry.date,
            "Link": entry.article_link,
            "Links": entry.links
        }
        return entry_dict
