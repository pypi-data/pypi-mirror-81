# ipyumbrella
Improved ipywidgets for collections.

Making widgets in Jupyter is super helpful and it unlocks a lot of potential. But I often find that they can be really cumbersome to work with and I'm constantly writing wrapper functions to capture output, add them to tabs, and set the title (using the child index..... ugh).

This wraps much of that functionality up so that you can wrap a for loop without thinking and each iteration will output to a new tab, parsing the title from the iterable elements. YAY!


```python
N = 6
def plot_something(i=0, n=N):
    plt.plot([min(i, n/2), min(n - i, n/2)])
    plt.ylim(0, n/2+1)
    plt.title('i={}'.format(i))
```


```python
import ipyumbrella as uw
import matplotlib.pyplot as plt


for i in uw.Carousel().D.items(range(N)):
    plot_something(i)
```

## Install

```bash
pip install ipyumbrella
```


## Usage

### Widgets
 - **Carousel**: sideways scrolling outputs
 - **Tabs**: same as ipywidgets
 - **Accordion**: same as ipywidgets

All of the described methods work for all widgets here. So you can interchange any of the widgets in the example.

#### Convenient inline display
I come from Javascript so I've grown quite accustomed to chaining. You can use either `.display()` or `.D` inline to display your widget before any items are added to it. This saves you from having to make a new line to store to a variable and a new line to display the widget.

Displaying the widget before you start is essential for longer running tasks so you can see the progress as it's running.


```python
carousel = uw.Carousel()
with carousel.D.item():
    plot_something()

# all equivalent - should display 5 times (including the time above)
carousel.display()
carousel.D
display(carousel)
carousel # last line in cell
```

#### Iterable (`.items(iterable)`)
Sometimes you have a list or generator of items that you want to show in tabs or a carousel. This is useful when you're plotting like 20 graphs and doing them one on top of the other makes navigating the notebook insufferable. You can optionally set a title function which will receive the current iterable item as input.


```python
uw.h4('Carousel').display()
for i in uw.Carousel().D.items(range(N), title='item {}'.format):
    plot_something(i)

uw.h4('Tabs').display()
for i in uw.Tabs().D.items(range(N), title='this is tab {}'.format):
    plot_something(i)
    
uw.h4('Accordion').display()
for i in uw.Accordion().D.items(range(N), title='see: {}'.format):
    plot_something(i)
```

#### Function capturing (`@.function`)
This gives you a bit more flexibility than wrapping an iterable. Anything from this function will be added to it's own tab.


```python
tb = uw.Tabs().D
@tb.function(title='plotting {}'.format)
def tabfunc(i, **kw):
    plot_something(i, **kw)

tabfunc(3)
tabfunc(4, n=5)
tabfunc(5)
```

#### Context Manager (`with .item():`)
This is the underlying mechanics for the other functions. What it does is, makes a new tab and append a ipywidgets.Output widget. It then uses the output widget to capture all output, like prints and plt.show() so it can display it in a tab.


```python
carousel = uw.Carousel().D
for i in range(N):
    with carousel.item():
        plot_something(i)
        
acc = uw.Accordion().D
for i in range(N):
    with acc.item(title='Item {}'.format(i)):
        plot_something(i)
```

Internally, it's doing this. So if you want to, you can to.


```python
# manually add an output as a tab above
tabs = uw.Tabs().D
with tabs.append(uw.Output(), title='something'):
    plot_something(2)
```
