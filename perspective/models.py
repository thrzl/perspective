from __future__ import annotations
from typing import List
from aiohttp import ClientSession
from orjson import dumps
from enum import Enum


class Attribute(Enum):
    """
    An Enum class containing attributes to scan text for.
    """
    __slots__ = (
        "toxicity",
        "severe_toxicity",
        "insult",
        "threat",
        "sexually_explicit",
        "flirtation",
    )
    toxicity = "TOXICITY"
    severe_toxicity = "SEVERE_TOXICITY"
    insult = "INSULT"
    threat = "THREAT"
    sexually_explicit = "SEXUALLY_EXPLICIT"
    flirtation = "FLIRTATION"

    @classmethod
    def all(cls) -> List[Attribute]:
        """Returns all possible attributes to scan for.
        """
        return [
            Attribute[attr] for attr in Attribute.__members__.keys()
        ]



class Perspective:
    """The Perspective API wrapper. 

    Parameters:
    -----------
        key (str): Your Perspective API key.
    
    """
    __slots__ = ("__key", "session", "attributes")

    def __init__(self, key: str):
        self.__key: str = key

    async def score(
        self, message: str, attributes: List[Attribute] = [Attribute.toxicity]
    ) -> Score:
        """Makes a request to the Perspective API.
            
        Parameters:
        -----------
            message (str): The message to scan.
            attributes (List[Attribute]): The attributes to scan the message for. Defaults to only toxicity.
        """
        if isinstance(attributes, Attribute):
            attributes = [attributes]

        if not all(isinstance(attribute, Attribute) for attribute in attributes):
            raise ValueError("Attributes are invalid!")

        requested_attributes = {attribute.value: {} for attribute in attributes}

        payload = dumps(
            dict(
                languages=["en"],
                comment={"text": message},
                requestedAttributes=requested_attributes,
            )
        )
        async with ClientSession() as session:
            res = await session.post(
                f"https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze",
                data=payload,
                params={"key": self.__key},
            )
        return Score(await res.json())


class Score:
    """The attribute score of the scanned message.
    You should never have to intialize this class yourself.

    Attributes:
    -----------
        toxicity (float): The toxicity score of the message.
        severe_toxicity (float): The severe toxicity score of the message.
        insult (float): The insult score of the message.
        threat (float): The threat score of the message.
        sexually_explicit (float): The sexually explicit score of the message.
        flirtation (float): The flirtation score of the message.
    """
    __slots__ = (
        "toxicity",
        "severe_toxicity",
        "insult",
        "threat",
        "sexually_explicit",
        "flirtation",
    )

    def __init__(self, res: dict):
        self.toxicity: float
        self.severe_toxicity: float
        self.insult: float
        self.sexually_explicit: float
        self.flirtation: float

        for i in Attribute.__members__:
            setattr(
                self,
                i.lower(),
                res["attributeScores"]
                .get(str(i).upper(), {})
                .get("summaryScore", {})
                .get("value", None),
            )
