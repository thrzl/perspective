# from __future__ import annotations
from typing import List
from enum import Enum
from typing import Dict
from httpx import AsyncClient

Attribute = Enum(
    "Attribute",
    [
        "TOXICITY",
        "SEVERE_TOXICITY",
        "INSULT",
        "THREAT",
        "SEXUALLY_EXPLICIT",
        "FLIRTATION",
    ],
)
"""An Enum containing the attributes to scan text for. This controls the requestedAttributes field of the request.

Raises:
    AttributeError: If the attributes are invalid.
"""


class Score:
    """The attribute score of the scanned message. You should never have to intialize this class yourself."""

    __slots__ = (
        "toxicity",
        "severe_toxicity",
        "insult",
        "threat",
        "sexually_explicit",
        "flirtation",
    )

    def __init__(self, res: Dict[str, dict]):
        self.toxicity: float
        self.severe_toxicity: float
        self.insult: float
        self.sexually_explicit: float
        self.flirtation: float

        for attribute in Attribute:
            setattr(
                self,
                attribute.name.lower(),
                res["attributeScores"]
                .get(attribute.name.upper(), {})
                .get("summaryScore", {})
                .get("value"),
            )


class Perspective:
    """The Perspective API client.

    Args:
        key (str): Your Perspective API key.
    """

    __slots__ = ("__key", "session", "attributes", "__client")

    def __init__(self, key: str):
        self.__key: str = key
        self.__client = AsyncClient()

    async def score(
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
        res = await self.__client.post(
            "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
            json=payload,
            params={"key": self.__key},
        )
        return Score(res.json())
