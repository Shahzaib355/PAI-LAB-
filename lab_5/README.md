# GitHub Repository
> 🔗 **GitHub:** [Add your GitHub link here]

# Lab 5 — OpenCV Functions in Jupyter Notebook
**Programming for Artificial Intelligence**
**Superior University Lahore**

## What This Project Does
Demonstrates all main OpenCV functions in an interactive
Jupyter Notebook. No external image needed — everything runs out of the box.

---

## Setup & Run

### Step 1: Install uv
```bash
pip install uv
```

### Step 2: Install dependencies & Run
```bash
uv sync
uv run python3 -m jupyter notebook
```

Then open `lab5_opencv.ipynb` in the browser and click **Cell → Run All**.

---

## Topics Covered
| # | Topic | Functions Used |
|---|---|---|
| 1 | Reading & Writing Images | `cv2.imread()`, `cv2.imwrite()` |
| 2 | Displaying Images | `cv2.cvtColor()` + matplotlib |
| 3 | Resizing & Cropping | `cv2.resize()`, array slicing |
| 4 | Color Spaces | BGR, Grayscale, HSV, LAB |
| 5 | Drawing Shapes | `cv2.line()`, `cv2.rectangle()`, `cv2.circle()`, `cv2.putText()` |
| 6 | Thresholding | `cv2.threshold()`, `cv2.adaptiveThreshold()` |
| 7 | Edge Detection | `cv2.Canny()`, Sobel, Laplacian |
| 8 | Contours | `cv2.findContours()`, `cv2.drawContours()` |
| 9 | Face Detection | `cv2.CascadeClassifier()` |
| 10 | Bonus: Blurring | Gaussian, Median, Bilateral |

---

## Reference
https://www.geeksforgeeks.org/opencv-python-tutorial/
