"""A module to crwal website to get text data
"""

from html.parser import HTMLParser
import requests
import re
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
from collections import deque
from src.utility.nlp_text_cleaner import remove_unicode
from src.utility.utils import config
from src.utility import constants

# Regex pattern to match a URL
HTTP_URL_PATTERN = r"^http[s]*://.+"


class HyperlinkParser(HTMLParser):
    """A class to parse the HTML and get the hyperlinks

    Args:
        HTMLParser (HTMLParser): Extend HTML parser class
    """

    def __init__(self):
        """A class constructor"""
        super().__init__()
        # Create a list to store the hyperlinks
        self.hyperlinks = []

    #
    def handle_starttag(self, tag, attrs):
        """A method to Override the HTMLParser's handle_starttag method to get the hyperlinks

        Args:
            tag (str): HTML tag
            attrs (list): HTML tag attributes
        """
        attrs = dict(attrs)

        # If the tag is an anchor tag and it has an href attribute, add the href attribute to the list of hyperlinks
        if tag == "a" and "href" in attrs:
            self.hyperlinks.append(attrs["href"])


def get_hyperlinks(url):
    """A method to get the hyperlinks from a URL

    Args:
        url (str): A website URL

    Returns:
        hyperlinks (list): A list of hyperlinks
    """
    # Try to open the URL and read the HTML
    try:
        # Open the URL and read the HTML
        with urllib.request.urlopen(url) as response:
            # If the response is not HTML, return an empty list
            if not response.info().get("Content-Type").startswith("text/html"):
                return []

            # Decode the HTML
            html = response.read().decode("utf-8")
    except Exception as e:
        print(e)
        return []

    # Create the HTML Parser and then Parse the HTML to get hyperlinks
    parser = HyperlinkParser()
    parser.feed(html)

    return parser.hyperlinks


def get_domain_hyperlinks(local_domain, url):
    """A method to get the hyperlinks from a URL that are within the same domain

    Args:
        local_domain (str): only domain name of URL
        url (str): A complete website URL

    Returns:
        clean links(list): A list of links within the same domain
    """
    clean_links = []
    for link in set(get_hyperlinks(url)):
        clean_link = None

        # If the link is a URL, check if it is within the same domain
        if re.search(HTTP_URL_PATTERN, link):
            # Parse the URL and check if the domain is the same
            url_obj = urlparse(link)
            if url_obj.netloc == local_domain:
                clean_link = link

        # If the link is not a URL, check if it is a relative link
        else:
            if link.startswith("/"):
                link = link[1:]
            elif link.startswith("#") or link.startswith("mailto:"):
                continue
            clean_link = "https://" + local_domain + "/" + link

        if clean_link is not None:
            if clean_link.endswith("/"):
                clean_link = clean_link[:-1]
            clean_links.append(clean_link)

    # Return the list of hyperlinks that are within the same domain
    return list(set(clean_links))


def crawl(url):
    """A method to crawal website and generate text files of each page

    Args:
        url (str): A complete website URL
    """
    # Parse the URL and get the domain
    local_domain = urlparse(url).netloc

    # Create a queue to store the URLs to crawl
    queue = deque([url])

    # Create a set to store the URLs that have already been seen (no duplicates)
    seen = set([url])

    # Create a directory to store the text files
    if not os.path.exists(
        config.get(constants.TEXT_DATA_PATH) + local_domain + "/"
    ):
        os.makedirs(config.get(constants.TEXT_DATA_PATH) + local_domain + "/")

    # Create a directory to store the csv files
    if not os.path.exists(
        config.get(constants.EMBEDDINGS_DATA_PATH) + local_domain + "/"
    ):
        os.makedirs(
            config.get(constants.EMBEDDINGS_DATA_PATH) + local_domain + "/"
        )

    # While the queue is not empty, continue crawling
    while queue:
        # Get the next URL from the queue
        url = queue.pop()
        print(url)  # for debugging and to see the progress

        # Save text from the url to a <url>.txt file
        file_name = remove_unicode(url[8:])
        """with open(
            "text/" + local_domain + "/" + url[8:].replace("/", "_") + ".txt",
            "w",
            encoding="UTF-8",
        ) as f:"""
        with open(
            config.get(constants.TEXT_DATA_PATH)
            + local_domain
            + "/"
            + file_name
            + ".txt",
            "w",
            encoding="UTF-8",
        ) as f:
            # Get the text from the URL using BeautifulSoup
            soup = BeautifulSoup(requests.get(url).text, "html.parser")

            # Get the text but remove the tags
            text = soup.get_text()

            # If the crawler gets to a page that requires JavaScript, it will stop the crawl
            if "You need to enable JavaScript to run this app." in text:
                print(
                    "Unable to parse page "
                    + url
                    + " due to JavaScript being required"
                )

            # Otherwise, write the text to the file in the text directory
            f.write(text)

        # Get the hyperlinks from the URL and add them to the queue
        for link in get_domain_hyperlinks(local_domain, url):
            if link not in seen:
                queue.append(link)
                seen.add(link)
