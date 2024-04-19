import pytest
from perspective import Perspective
from os import environ


@pytest.mark.asyncio
async def test_perspective():
    key = environ.get("PERSPECTIVE_API_KEY")
    if not key:
        pytest.exit("PERSPECTIVE_API_KEY is not set!")

    p = Perspective(key)

    r = await p.score("you're awesome!")
    assert r.toxicity < 0.05
