# pgex
 A Python PyGame package extension.

## Desription
Pgex is a package that will help you to create games with PyGame easier and more convenient. There is no longer any need to register the functionality of text fields, buttons and other widgets each time. Everything has already been done for you! 

## Installation
Package is uploaded on PyPI and can be downloaded through
```bash
pip install pgex
```

## Links
Link on PyPI: https://pypi.org/project/pgex/ \
GitHub Repository: https://github.com/IvanFoke/pgex

## Usage
**1. Text creation**\
Before you start creating any project on PyGame, you must initialize it. Use standard commands like screen creation and title setting.\
All widgets in pgex are stored in _pgex.widgets_. For example, let's import Text widget.
Pgex also describes a large number of different colors. They can be found in _pgex.parameters_.
```python
import pygame as pg
from pgex.widgets import Text
from pgex.parameters import colors

pg.init()
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Pgex Example")
clock = pg.time.Clock()

txt = Text("SomeText", r'Crushez.ttf', 100, font_color=colors["dark_gray"], bg_color=colors["white"], border_width=1)

game = True
while game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game = False
            break
    screen.fill(colors["light_blue"])
    txt.draw(screen, (100, 300))
    pg.display.update()
    clock.tick(30)
```

As you can see in the example, text widget is created with Text class. First 3 arguments are the text, the path to a font and the font size. Result of the work of this program:

![python_RdNLxTmrXB](https://user-images.githubusercontent.com/58694429/86750802-e296d180-c046-11ea-84c8-2f6855004769.png)

**2. A Button that gets a value of an Entry field**\
Button and Entry are another widgets from pgex. They also can be imported from _pgex.widgets_.\
A distinctive feature of the Button is the passing of a function into it through the _action_ argument, which will be called when the user clicks on it.\
The Entry requires the passing of PyGame events. This allows widget to intercept the data entered in the field. Field supports backspace key. To stop entering the text in field, you can press escape, enter, or simply click the left mouse button outside the field.

```python
from pgex.widgets import Button
from pgex.widgets import Entry


def get_entry_value():
    global entry
    print(f"Got text: {entry.text}")


entry = Entry(200, 50, r'Crushez.ttf', 20, centralized=True)
btn = Button(200, 100, "Btn", r'Crushez.ttf', 40, r'button.wav', action=get_entry_value, centralized=True)

def handle_events(events):
    for event in events:
        if event.type == pg.QUIT:
            return False
    return True

# ... in game cycle
while True:
    # ...
    events = pg.event.get()
    if not handle_events(events):
        break
    btn.draw(screen, (500, 100))
    entry.draw(screen, (100, 200), events)      
```

Result:\
![python_cr2iYoWarZ](https://user-images.githubusercontent.com/58694429/86750792-e165a480-c046-11ea-8d28-22c2d5885678.png)


Full example can be seen in examples folder.\
All other possibilities will be described soon.
