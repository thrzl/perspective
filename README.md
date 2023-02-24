# 💖 perspective
a strongly typed wrapper for google's perspective api

## 🪴 example
```py
from perspective import Perspective, Attribute
from asyncio import get_event_loop

p = Perspective(key="...")

async def main():
    s = await p.score(
        "your message here", attributes=(Attribute.flirtation, Attribute.sexually_explicit)
    )
    print(s.flirtation) 
    print(s.sexually_explicit)
```