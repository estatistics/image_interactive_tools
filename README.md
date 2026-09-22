# A) 📖 Interactive Book Page Crop & Unwarp Tool
(Cut_Interactive)

An interactive Python utility designed for scanning and digitizing book pages. It allows you to select quadrilateral page bounds, perspective-correct (unwarp) tilted or skewed pages, and batch-process entire scans with persistent bounding boxes and extended canvas margins.

---

## ✨ Features

- **Interactive Box Dragging:** Seamlessly align page edges using 4 draggable corner handles (`TL`, `TR`, `BR`, `BL`).
- **Perspective Correction (Unwarping):** Automatically flattens tilted or angled page scans into straight, orthogonal rectangles.
- **20% Padded Canvas:** Extends the window workspace by 20% around the image so you can position handles outside the frame without cutting off text margins.
- **Smart Background Matching:** Any cropped outer space is automatically filled using the natural paper/page color sampled directly from the scan edges.
- **Persistent Bounding Box:** Bounding positions carry over from image to image, requiring only slight adjustments per page.
- **Multiple Output Formats:** Choose between high-quality **JPG**, **Lossy WebP**, **Lossless WebP**, or **PNG**.
- **Dynamic Window Title:** Shows progress, file names, and hotkey instructions right in the top bar.

---

## 💻 Requirements & Installation

This script runs on **Windows**, **macOS**, and **Linux** (e.g., Ubuntu, Debian, Arch).

### Prerequisites
- Python 3.7 or higher

### Install Dependencies
Open your terminal or command prompt and run:

```bash
pip install opencv-python numpy
```

---

## 🚀 How to Use

1. **Place your script** in the folder containing your scanned page images (`.jpg`, `.png`, `.webp`, etc.).
2. **Launch the tool**:

```bash
python cut_interactive_flow.py
```

3. **Adjust & Process:**
- A window displaying the **first image** and an adjustable green bounding box will open.
- Click and drag the red corner handles (`TL`, `TR`, `BR`, `BL`) to align with the edges of your book page.
- Press **`ENTER`** or **`SPACE`** to process, unwarp, and save the image.
- The tool will automatically open the **next image**, keeping the bounding box in the same relative position for quick adjustments!

---

## ⌨️ Controls & Shortcuts

| Key / Action | Function |
| :--- | :--- |
| **Left Click + Drag** | Drag any of the 4 corner handles (`TL`, `TR`, `BR`, `BL`) |
| **`ENTER`** / **`SPACE`** | Confirm crop, perform unwarping, save image, and advance to next |
| **`R`** | Reset current bounding box handles to default position |
| **`ESC`** | Skip the current image without processing |

---

## ⚙️ Configuration Options

You can adjust export options inside `cut_interactive_flow.py` by opening the script in any text editor:

### 1. Change Save Format & Quality
Modify the `SAVE_FORMAT` variable at the top of the file:

```python
# Options: "JPG", "WEBP_LOSSY", "WEBP_LOSSLESS", "PNG"
SAVE_FORMAT = "JPG"
```

| Option | Mode | Recommended Use Case |
| :--- | :--- | :--- |
| `"JPG"` | Lossy | High-quality compact photos (Quality: 95) |
| `"WEBP_LOSSY"` | Lossy | Modern web compression with small file size (Quality: 90) |
| `"WEBP_LOSSLESS"` | Lossless | Perfect archival quality without artifacting |
| `"PNG"` | Lossless | Standard uncompressed raster images |

### 2. Adjust Canvas Padding Space
Change `PAD_RATIO` to give yourself more or less workspace outside the original image boundary:

```python
PAD_RATIO = 0.20  # Adds 20% extra space on all sides (Default: 0.20)
```

---

## 📂 Output Folder Structure

Processed images are automatically created and saved inside a subfolder named `cropped_unwarped/`:

```text
your_project_folder/
│
├── cut_interactive_flow.py
├── page_001.jpg
├── page_002.jpg
└── cropped_unwarped/
    ├── page_001.jpg
    └── page_002.jpg
```

---

## 🐧 OS-Specific Notes

- **Linux (X11 / Wayland):** If OpenCV windows fail to open, ensure GUI backends are installed:
```bash
sudo apt-get install python3-opencv
```
- **macOS:** Ensure Terminal or your IDE has permission to access the folder containing your photos.
- **Windows:** Supports all standard file paths and image formats out of the box.# 📖 Interactive Book Page Crop & Unwarp Tool

An interactive Python utility designed for scanning and digitizing book pages. It allows you to select quadrilateral page bounds, perspective-correct (unwarp) tilted or skewed pages, and batch-process entire scans with persistent bounding boxes and extended canvas margins.

---

## ✨ Features

- **Interactive Box Dragging:** Seamlessly align page edges using 4 draggable corner handles (`TL`, `TR`, `BR`, `BL`).
- **Perspective Correction (Unwarping):** Automatically flattens tilted or angled page scans into straight, orthogonal rectangles.
- **20% Padded Canvas:** Extends the window workspace by 20% around the image so you can position handles outside the frame without cutting off text margins.
- **Smart Background Matching:** Any cropped outer space is automatically filled using the natural paper/page color sampled directly from the scan edges.
- **Persistent Bounding Box:** Bounding positions carry over from image to image, requiring only slight adjustments per page.
- **Multiple Output Formats:** Choose between high-quality **JPG**, **Lossy WebP**, **Lossless WebP**, or **PNG**.
- **Dynamic Window Title:** Shows progress, file names, and hotkey instructions right in the top bar.

---

## 💻 Requirements & Installation

This script runs on **Windows**, **macOS**, and **Linux** (e.g., Ubuntu, Debian, Arch).

### Prerequisites
- Python 3.7 or higher

### Install Dependencies
Open your terminal or command prompt and run:

```bash
pip install opencv-python numpy
```

-----------------------------------------------------------------------------------------------
# spot_removes.py

An interactive OpenCV-based Python tool designed to cleanly erase fingers, thumbs, and unwanted shadows from scanned book pages and documents. 

Unlike standard inpainting algorithms that cause ugly blurred blobs, `spot_removes.py` uses **Patch-Based Seamless Texture Cloning** (Poisson blending similar to GIMP's Clone/Heal tool) and **Pseudo-Canvas Border Padding** to ensure perfect paper grain restoration—even along the very top and side edges of your images.

---

## <h2>Key Features</h2>

* **Interactive Ellipse Selection:** Click and drag to draw selection circles over fingers or spots.
* **Undo & Reset Controls:** Press **`u`** to undo the last drawn circle or **`r`** to clear all selections on the active page.
* **External Texture Cloning:** Uses real paper grain from a sample image (e.g., `cloning.webp`) to fill selected zones seamlessly.
* **Edge & Corner Support (Pseudo-Canvas):** Applies temporary $8\%$ edge padding during cloning so selections touching image borders don't cut off or bleed unexpectedly.
* **Automatic Shadow Buffer:** Expands selections by an adjustable percentage to swallow soft outer finger shadows and vignetting.
* **Config Block Integration:** Configure output format (`jpg`, `webp`, `png`), compression quality, texture file paths, and padding directly inside the script.
* **Cross-Platform:** Suppresses Qt font warnings natively on Linux environments.

---

## <h2>Requirements</h2>

* Python 3.8+
* NumPy
* OpenCV (`opencv-python`)

Install dependencies via pip:

<pre><code>
pip install opencv-python numpy
</code></pre>

---

## <h2>Folder Structure Setup</h2>

Place your target images and texture reference in the same folder as `spot_removes.py`:

<pre><code>
project_directory/
│
├── spot_removes.py
├── page_001.jpg
├── page_002.png
│
└── cloning_image/
    └── cloning.webp
</code></pre>

---

## <h2>Configuration</h2>

Edit the `CONFIG` dictionary at the top of `spot_removes.py` to customize settings:

<pre><code>
CONFIG = {
    # Output format: "jpg", "webp", or "png"
    "OUTPUT_FORMAT": "jpg",
    
    # Quality settings (1-100 for JPG/WEBP | 0-9 for PNG compression)
    "QUALITY": 95,
    
    # Shadow Expansion Buffer (Expands circles by % to eat soft edge shadows)
    "EXPANSION_PCT": 0.20,
    
    # External Texture Options
    "USE_EXTERNAL_TEXTURE": True,
    "TEXTURE_FILENAME": "./cloning_image/cloning.webp",
    
    # Pseudo Canvas Padding Percentage (Allows blending on top/side edges)
    "PADDING_PCT": 0.08,
    
    # Output directory name
    "OUTPUT_FOLDER_NAME": "clean_pages_output",
}
</code></pre>

---

## <h2>Usage</h2>

Run the script from your terminal:

<pre><code>
python spot_removes.py
</code></pre>

### Interactive Controls

| Hotkey | Action |
| :--- | :--- |
| **Mouse Drag** | Draw a selection circle over a finger/shadow |
| **`u`** | **Undo** the last drawn circle |
| **`r`** | **Reset** all drawn circles on the current page |
| **`ENTER` / `SPACE`** | **Apply** cloning, save image, and load next page |
| **`s`** | **Skip** current image without saving changes |
| **`ESC`** | **Exit** script immediately |

---

## <h2>How It Works</h2>

1. **Expansion Buffer:** The script expands your drawn circles outward by `EXPANSION_PCT` ($20\%$) to absorb soft gradients and finger shadows.
2. **Pseudo-Canvas Padding:** The image is padded on all sides using edge replication (`PADDING_PCT`). This creates a border around selections touching the top, bottom, or side edges, allowing Poisson blending equations to calculate surrounding pixels.
3. **Texture Sampling:** Paper texture is retrieved from your custom `cloning.webp` image and resized to cover the mask zone.
4. **Poisson Seamless Blending:** OpenCV's `seamlessClone` matches the target page's local lighting and tone while keeping $100\%$ of the paper grain.
5. **Auto-Cropping:** The padded canvas is cropped back to its original dimensions before saving.
