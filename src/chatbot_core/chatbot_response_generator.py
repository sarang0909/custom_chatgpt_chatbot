"""A module to access and generate openai apis responses"""

import openai
from openai.embeddings_utils import distances_from_embeddings
from src.utility.utils import config
from src.utility import constants
from src.utility.loggers import logger


class ChatbotCore:
    """A class for chatgpt/openai API access"""

    def __init__(self) -> None:
        """A class constructor"""
        # Set initial context for Chatgpt
        self.chat_messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant.if you don't know the answer or need more context, say \"I don't know\" and nothing else",
            },
        ]
        self.model = config.get(constants.CHAT_MODEL)

    def create_context(self, question, df, max_len=1800, size="ada"):
        """
        Create a context for a question by finding the most similar context from the dataframe
        """

        # Get the embeddings for the question
        q_embeddings = openai.Embedding.create(
            input=question, engine="text-embedding-ada-002"
        )["data"][0]["embedding"]

        # Get the distances from the embeddings
        df["distances"] = distances_from_embeddings(
            q_embeddings, df["embeddings"].values, distance_metric="cosine"
        )

        returns = []
        cur_len = 0

        # Sort by distance and add the text to the context until the context is too long
        for i, row in df.sort_values("distances", ascending=True).iterrows():
            # Add the length of the text to the current length
            cur_len += row["n_tokens"] + 4

            # If the context is too long, break
            if cur_len > max_len:
                break

            # Else add it to the text that is being returned
            returns.append(row["text"])

        # Return the context
        return "\n\n###\n\n".join(returns)

    def answer_question(
        self,
        df,
        question,
        max_len=1800,
        size="ada",
        debug=False,
        max_tokens=150,
        stop_sequence=None,
    ):
        """A method to return response of chatbot based on model selected

        Args:
            df (pandas dataframe): Context text embeddings
            moel (str, optional): A chatbot model either gpt-3.5-turbo or text-davinci-003 . Defaults to "text-davinci-003".
            max_len (int, optional): A maximum context length. Defaults to 1800.
            size (str, optional): Size. Defaults to "ada".
            debug (bool, optional): Debug mode. Defaults to False.
            max_tokens (int, optional): maximum tokens ina query. Defaults to 150.
            stop_sequence (_type_, optional): Where to stop bot response. Defaults to None.

        Returns:
            answer(str): A bot response to a query
        """

        try:
            if self.model == "gpt-3.5-turbo":
                self.chat_messages.append(
                    {"role": "user", "content": question}
                )
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=self.chat_messages,
                )
                response_message = response["choices"][0]["message"]["content"]
                negative_responses = [
                    "I don't know",
                    "AI language model",
                    "I don't know.",
                    "I do not know",
                    "sorry",
                ]
                if any(ele in response_message for ele in negative_responses):
                    # Answer a question based on the most similar context from the dataframe texts

                    context = self.create_context(
                        question,
                        df,
                        max_len=max_len,
                        size=size,
                    )
                    # logger.info("Context:\n" + context)

                    self.chat_messages.append(
                        {
                            "role": "user",
                            "content": f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\" and nothing else \n\n Context: {context}\n\n---\n\nQuestion: {question}\n Answer:",
                        }
                    )
                    response = openai.ChatCompletion.create(
                        model=self.model,
                        messages=self.chat_messages,
                    )
                    response_message = response["choices"][0]["message"][
                        "content"
                    ]
                    self.chat_messages.append(
                        {"role": "assistant", "content": response_message}
                    )
                else:
                    self.chat_messages.append(
                        {"role": "assistant", "content": response_message}
                    )

                return response_message
            elif self.model == "text-davinci-003":
                # Create a completions using the questin and context
                response = openai.Completion.create(
                    prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't know\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\nAnswer:",
                    temperature=0,
                    max_tokens=max_tokens,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    stop=stop_sequence,
                    model=self.model,
                )
                # print(response["choices"][0]["text"].strip())
                return response["choices"][0]["text"].strip()
        except Exception as e:
            logger.error(e)
            return ""
