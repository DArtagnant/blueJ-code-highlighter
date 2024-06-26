# BlueJ-code-highlighter

Format java code in html, imitating the style of the blue-J IDE.

> [!NOTE]
> I have no affiliation or relationship with Blue-J. This is a personal project.


> [!CAUTION]
> THIS CODE IS GIVEN WITHOUT ANY WARRANTY. Use at your own risk.

## Using _BlueJ-code-highlighter_

### Installing

_BlueJ-code-highlighter_ has the following dependencies :

* Python >= 3.10 (tested on 3.11)
* pygments (tested on 2.18.0)

To install pygments run :

```shell
>> pip install Pygments
```

Download the project :

```shell
>> git clone https://github.com/DArtagnant/blueJ-code-highlighter.git
```

### Usage

Once you have downloaded the project, open or import `highlight.py`. Then you can modify the call of the `from_file` function.

The first argument is the path where is store the java code, the second the path where you want the html output to be.

By example :

```python
from_file("input.txt", "output.html")
```

will read a file named `input.txt` and located in the current directory and write the output in `output.html`.

#### Flags

`from_file` has three more optional parameters :

* `border_radius` set the radius of the rounded corners of the output. default 15.
* `functions_always_in_class` when `True`, allows to render uncomplete code with a class indentation. _You should not mix uncomplete code and classes._ default `True`
* `change_escape_char` when `True`, allows to use classical characters for `&`, `<`, `>`, `"` and `'` instead of an encoding like `&quot;` for `"`. This functionality is based on a specific private implementation of pygments `HtmlFormatter` and may not work in newer versions. default `False`
* `credits` when `False` allows to mask the credits at the bottom of the render. Please read _About BlueJ-code-highlighter_. If you disable this option, you have to mention the formatter source (link to the github page) and author's name (DArtagnant) somewhere in the page in accordance with the free license chosen for this project. default `True`

Example :

```python
from_file("input.txt", "output.html", credits=True, border_radius=20, functions_always_in_class=False)
```

## Contributing

Feel free to open a github issue, I will reply as soon as possible.

## Building

Run `build.bat` to build the GUI into a .exe

## About _BlueJ-code-highlighter_

This project was originally a utility code written by DArtagnant as a favor to a friend.

It is therefore a hobby, and this code is given without any guarantee of operation or future support. It probably contains a few bugs. In any case, and without committing myself, I will do my best to avoid these inconveniences and improve this project while taking into account my other activities.

> [!NOTE]
> Project under GPL-3.0 license.
