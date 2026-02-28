# pyqt6-icon-theme

[English](../README.md) | 繁體中文

<p>
  <a href="https://pypi.org/project/pyqt6-icon-theme/">
    <img src="https://img.shields.io/pypi/v/pyqt6-icon-theme">
  </a>
  <a href="https://www.python.org/">
    <img src="https://img.shields.io/badge/python-≥3.10-blue">
  </a>
  <a href="https://codecov.io/gh/JW5123/pyqt6-icon-theme">
    <img src="https://codecov.io/gh/JW5123/pyqt6-icon-theme/branch/main/graph/badge.svg">
  </a>
  <a href="https://pypi.org/project/pyqt6-icon-theme/">
    <img src="https://img.shields.io/pypi/dm/pyqt6-icon-theme">
  </a>
  <a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/badge/License-MIT-yellow.svg">
  </a>
</p>

**PyQt6 動態圖示主題工具** — 支援 svg 自動亮色/暗色主題切換、自訂顏色效果

## 功能展示
<img src="pyqt6_icon_theme_demo.gif" width="350">


## 功能特色

- **SVG 動態染色** — 自動去除原始 fill/stroke，套用任意自訂顏色
- **主題感知** — 自動在黑色（亮色主題）和白色（暗色主題）之間切換 (未自訂svg顏色時)
- **Hover 效果** — 滑鼠移入/移出時切換圖示顏色
- **PNG / JPG 支援** — 以任意尺寸渲染點陣圖，保留原始顏色
- **快取機制** — 以 `(name, color, size, keep_original)` 為 key 快取，避免重複渲染

## 安裝

```bash
pip install pyqt6-icon-theme
```

## 使用說明

引入函式庫
```python
from pyqt6_icon_theme import IconManager, IconButton
```
建立圖示資料夾路徑 (支援 .svg、.png、.jpg、.jpeg)，路徑名稱可自訂
```py
IconManager.set_icon_dir("icons")
```

### IconButton
- 第一個參數為圖示檔名名稱，可不用輸入副檔名
- 第二個參數為調整圖示像素大小
- 第三個參數為調整圖示自訂顏色，若設定 `None` 則自動偵測視窗背景亮度，亮色背景套用黑色、暗色背景套用白色
- 第四個參數為調整圖示 `hover` 自訂顏色，若設定 `None` 則不變色
- 第五個參數為保留 `svg` 圖示原始顏色，若設定為 `True` 則 `normal_color` 和 `hover_color` 不會套用自訂顏色，不設定參數預設為 `False`
```python
IconButton(name, size=16, normal_color=None, hover_color=None, keep_original=False)
```

### 範例

```python
# 跟隨主題自動變色（亮色=黑、暗色=白）
btn = IconButton("user.svg", size=30)

# 指定顏色 + hover 效果
btn = IconButton("add.svg", size=36, normal_color="#49ADF0", hover_color="#F08884")

# 保留 SVG 原始顏色（不受主題影響）
btn = IconButton("edit.svg", size=40, keep_original=True)

# PNG/JPG — 永遠顯示原始顏色
btn = IconButton("delete.png", size=40)
```

### 完整範例

請參考 example 資料夾

## 參數行為對照表

| 情境 | `normal_color` | `hover_color` | `keep_original` | 結果 |
|------|---------------|---------------|-----------------|------|
| SVG 未指定顏色 | `None` | `None` | `False` | 跟隨主題（黑/白） |
| SVG 指定顏色 | `"#49ADF0"` | `"#F08884"` | `False` | 自訂顏色 + hover |
| SVG 保留原色 | — | — | `True` | SVG 原始渲染 |
| PNG / JPG | 忽略 | 忽略 | 忽略 | 永遠原始顏色 |


## 圖示資料夾結構

```
your_project/
├── icons/
│   ├── user.svg
│   ├── add.svg
│   ├── edit.svg
│   └── delete.png
└── main.py
```

資料夾內所有 `.svg`、`.png`、`.jpg`、`.jpeg` 檔案都會自動載入。

## 授權

MIT © [JW5123](https://github.com/JW5123)