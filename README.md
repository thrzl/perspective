# 💖 perspective
a strongly typed wrapper for google's perspective api

## 📦 installation
```sh
pip install perspectiveapi
```

## 🪴 example
```py
from perspective import Perspective, Attribute
from asyncio import get_event_loop

p = Perspective(key="...")

async def main():
    s = await p.score(
        "your message here", attributes=(Attribute.flirtation, Attribute.all())
    )
    print(s.flirtation) 
    print(s.severe_toxicity)
```