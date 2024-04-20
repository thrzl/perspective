# 💖 perspective
a strongly typed wrapper for google's perspective api

## 📦 installation
```sh
pip install perspectiveapi
```

## 🪴 example
### async
```py
from perspective import Perspective, Attribute

p = Perspective(key="...")

async def main():
    s = await p.score(
        "your message here", attributes=(Attribute.flirtation, Attribute.all())
    )
    print(s.flirtation) 
    print(s.severe_toxicity)
```

### blocking
```py
from perspective.blocking import Perspective, Attribute

p = Perspective(key="...")

def main():
    s = p.score(
        "your message here", attributes=(Attribute.flirtation, Attribute.all())
    )
    print(s.flirtation) 
    print(s.severe_toxicity)
```