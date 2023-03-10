"""A core NLP module to process bot query and return response
"""


import os
from urllib.parse import urlparse
from src.chatbot_core.chatbot_response_generator import ChatbotCore
from src.data_collection import web_crawler
from src.data_collection.data_processor import DataProcessor
from src.utility.utils import config
from src.utility import constants
from src.utility.loggers import logger


class NLPCore:
    """A core NLP class having methods to generate bot response"""

    def __init__(self) -> None:
        """Class constructor"""
        self.dataset_embeddings = None
        self.data_processor = None
        self.full_url = None
        self.local_domain = None

    def set_website_name(self, website_name):
        """A method to set website name and initialise data processor to process website texts

        Args:
            website_name (str): A website name to give a chatbot the context
        """
        if self.full_url != website_name:
            self.full_url = website_name
            self.local_domain = urlparse(self.full_url).netloc
            self.data_processor = DataProcessor(self.full_url)
        logger.info("Website entered:%s", website_name)

    def core_method(self, question):
        """A method to generate bot response based on query

        Args:
            question (str): A user query

        Returns:
            answer (str): A bot response to user query
        """

        answer = ChatbotCore().answer_question(
            self.data_processor.get_embeddings(),
            question=question,
            debug=True,
        )
        logger.info("User Query: " + question)
        logger.info("Chatbot Response: " + answer)
        return answer
