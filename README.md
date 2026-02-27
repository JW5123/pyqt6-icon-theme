# pyqt6-icon-theme

English | [繁體中文](doc/README.zh-TW.md)

<p>
  <a href="https://pypi.org/project/pyqt6-icon-theme/"><img src="https://img.shields.io/pypi/v/pyqt6-icon-theme"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/python-≥3.10-blue"></a>
  <a href="https://pypi.org/project/pyqt6-icon-theme/"><img src="https://img.shields.io/pypi/dm/pyqt6-icon-theme"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
</p>

**PyQt6 Dynamic Icon Theme Toolkit** — Support automatic light/dark theme switching for SVG icons, with customizable color effects.

## Demo
<img src="doc/pyqt6_icon_theme_demo.gif" width="350">


## Features

- **SVG Dynamic Recoloring** — Automatically strips original fill/stroke and applies any custom color
- **Theme Awareness** — Automatically switches between black (light theme) and white (dark theme) when no custom color is set
- **Hover Effect** — Switches icon color on mouse enter/leave
- **PNG / JPG Support** — Renders raster images at any size while preserving original colors
- **Caching** — Icons are cached by `(name, color, size, keep_original)` to avoid redundant rendering

## Installation

```python
pip install pyqt6-icon-theme
```

## Usage

Import the library:
```python
from pyqt6_icon_theme import IconManager, IconButton
```

Set the icon directory (supports `.svg`, `.png`, `.jpg`, `.jpeg`); the path name is customizable:
```python
IconManager.set_icon_dir("icons")
```

### IconButton

- 1st parameter: icon file name — extension is optional
- 2nd parameter: icon size in pixels
- 3rd parameter: icon color in normal state — if `None`, the color is automatically detected from the window background (black on light, white on dark)
- 4th parameter: icon color on hover — if `None`, no color change on hover
- 5th parameter: preserve the SVG's original colors — if `True`, `normal_color` and `hover_color` are ignored; defaults to `False`

```python
IconButton(name, size=16, normal_color=None, hover_color=None, keep_original=False)
```

### Examples

```python
# Auto color based on theme (light = black, dark = white)
btn = IconButton("user.svg", size=30)

# Custom color + hover effect
btn = IconButton("add.svg", size=36, normal_color="#49ADF0", hover_color="#F08884")

# Preserve SVG original colors (unaffected by theme)
btn = IconButton("edit.svg", size=40, keep_original=True)

# PNG/JPG — always displays original colors
btn = IconButton("delete.png", size=40)
```

### Full Example

See the `example` folder.

## Parameter Behavior Reference

| Scenario | `normal_color` | `hover_color` | `keep_original` | Result |
|----------|---------------|---------------|-----------------|--------|
| SVG, no color specified | `None` | `None` | `False` | Follows theme (black/white) |
| SVG, custom color | `"#49ADF0"` | `"#F08884"` | `False` | Custom color + hover |
| SVG, original colors | — | — | `True` | SVG rendered as-is |
| PNG / JPG | ignored | ignored | ignored | Always original colors |

## Icon Directory Structure

```
your_project/
├── icons/
│   ├── user.svg
│   ├── add.svg
│   ├── edit.svg
│   └── delete.png
└── main.py
```

All `.svg`, `.png`, `.jpg`, `.jpeg` files in the directory are loaded automatically.

## License

MIT © [JW5123](https://github.com/JW5123)