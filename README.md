# 📖 Interactive Book Page Crop & Unwarp Tool

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
