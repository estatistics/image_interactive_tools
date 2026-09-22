# 📖 Interactive Book Page Crop & Unwarp Tool
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
