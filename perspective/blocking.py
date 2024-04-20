# from __future__ import annotations
from typing import List
from typing import Dict
from httpx import Client
from .models import Attribute, Score


class Perspective:
    """The Perspective API client.

    Args:
        key (str): Your Perspective API key.
    """

    __slots__ = ("__key", "session", "attributes", "__client")

    def __init__(self, key: str):
        self.__key: str = key
        self.__client = Client()

    def score(
        self, message: str, attributes: List[Attribute] = [Attribute.TOXICITY]
    ) -> Score:
        """Makes a request to the Perspective API.

        Args:
            message (str): The message to scan.
            attributes (List[Attribute], optional): The attributes to scan the messages for. Defaults to [Attribute.TOXICITY].

        Raises:
            ValueError: If the attributes are invalid.

        Returns:
            Score: The attribute scores of the scanned message.
        """
        attributes = list(attributes)

        if not all(isinstance(attribute, Attribute) for attribute in attributes):
            raise ValueError("Attributes are invalid!")

        requested_attributes: Dict[str, dict] = {
            attribute.name: {} for attribute in attributes
        }

        payload = dict(
            languages=["en"],
            comment={"text": message},
            requestedAttributes=requested_attributes,
        )
        res = self.__client.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            json=payload,
            params={"key": self.__key},
        )
        return Score(res.json())
