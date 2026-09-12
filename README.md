# IMG to PDF Converter

A modern Python desktop application with a graphical user interface (GUI) to seamlessly convert a folder of manga images into a single, high-quality PDF file.

## Features
- **Natural Sorting**: Automatically sorts pages correctly (e.g., page 2 comes before page 10) instead of alphabetical sorting.
- **Lossless Conversion**: Uses `img2pdf` to embed images directly without recompression or quality loss.

## Requirements
- Python 3.6+
- `img2pdf`
- `Pillow` (PIL)

## Installation
1. Clone this repository or download the source code.
2. Install the required Python packages:
   ```bash
   pip install img2pdf Pillow
   ```
3. Ensure you have an `assets` folder in the same directory as the script containing your `folder_icon.png`. *(Optional)*

## Usage
Run the application from your terminal or command prompt:
```bash
python main.py
```
1. Click the **Browse** button next to "Select Images Folder" to choose the directory with your manga images.
2. Click the **Browse** button next to "Select Output PDF" to choose the destination and name of the resulting PDF.
3. Click **Convert to PDF** and wait for the process to finish.


[[Last](https://github.com/TrueYahir/IMG-PDF/releases/tag/v1.0)](https://github.com/TrueYahir/IMG-PDF/releases/tag/v1.0)