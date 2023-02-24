from __future__ import annotations
from typing import List
from aiohttp import ClientSession
from orjson import dumps
from enum import Enum


class Attribute(Enum):
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


class Perspective:
    __slots__ = ("__key", "session", "attributes")

    def __init__(self, key: str):
        self.__key: str = key

    async def score(
        self, message: str, attributes: List[Attribute] = [Attribute.toxicity]
    ) -> Score:
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
