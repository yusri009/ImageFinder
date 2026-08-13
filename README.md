````markdown
# ImageFinder

A privacy-focused **offline multimodal image search engine** that allows users to search local image collections using either:

- **Visual concepts** — e.g. `dog playing outside`, `car on a road`, `person sitting`
- **Text inside images** — e.g. `invoice`, `university`, `receipt`

ImageFinder combines **OpenCLIP**, **EasyOCR**, and **ChromaDB** to understand both the visual content and embedded text within images while keeping processing and storage local.

---

## Features

### Semantic Image Search

Search images using natural-language descriptions instead of filenames.

Example queries:

```text
person sitting
car on a road
food on a table
dog outside
````

OpenCLIP generates vector embeddings for images and search queries, allowing ImageFinder to retrieve visually relevant images based on semantic similarity.

---

### OCR-Based Text Search

ImageFinder extracts visible text from images using **EasyOCR** during indexing.

This allows users to search screenshots, documents, receipts, posters, and other images containing text.

Example queries:

```text
invoice
university
receipt
IPM
```

Text matching is case-insensitive and operates on OCR metadata stored alongside each indexed image.

---

### Offline and Privacy-Focused

ImageFinder is designed to process images locally.

Image embeddings, OCR text, and image paths are stored in a persistent local **ChromaDB** database rather than being uploaded to an external search service.

---

### GPU-Accelerated Visual Embeddings

The current implementation uses:

```text
EasyOCR   → CPU
OpenCLIP  → NVIDIA GPU / CUDA
```

OpenCLIP uses GPU acceleration for image and text embedding generation, while OCR processing runs on the CPU.

---

### Persistent Vector Database

ChromaDB is used to store:

* Image embeddings
* Image file paths
* Extracted OCR text
* Associated metadata

The database persists locally, allowing previously indexed images to be searched without recreating the entire index every time.

---

### Fault-Tolerant Indexing

If an image cannot be processed, ImageFinder skips the failed image and continues indexing the remaining files instead of terminating the entire process.

Supported image formats include:

```text
.png
.jpg
.jpeg
.webp
```

---

# How It Works

ImageFinder operates in two main stages:

1. Image indexing
2. Image searching

---

## 1. Image Indexing

Images are loaded from:

```text
data/images/
```

Each image is processed through two pipelines:

```text
                 ┌────────────────────┐
                 │    Local Image     │
                 └─────────┬──────────┘
                           │
                ┌──────────┴───────────┐
                │                      │
                ▼                      ▼
         ┌─────────────┐        ┌─────────────┐
         │   EasyOCR   │        │  OpenCLIP   │
         │    (CPU)    │        │   (CUDA)    │
         └──────┬──────┘        └──────┬──────┘
                │                      │
                ▼                      ▼
         Extracted Text          Image Embedding
                │                      │
                └──────────┬───────────┘
                           ▼
                    ┌─────────────┐
                    │  ChromaDB   │
                    │ Local Index │
                    └─────────────┘
```

During indexing:

1. Images are discovered from the configured image directory.
2. EasyOCR extracts visible text from each image.
3. OpenCLIP generates semantic image embeddings.
4. Image embeddings and OCR metadata are stored in ChromaDB.
5. Failed images are skipped without interrupting the indexing process.

---

# 2. Searching

ImageFinder supports two search mechanisms.

## Visual Search

Visual search accepts a natural-language description.

Example:

```python
search_visuals("person sitting")
```

The text query is converted into an OpenCLIP embedding and compared with the stored image embeddings.

ChromaDB then returns the most semantically similar images.

---

## OCR Text Search

Text search finds images containing specific visible words or phrases.

Example:

```python
search_text("invoice")
```

ImageFinder searches the OCR metadata generated during indexing and returns images containing matching text.

---

# Project Structure

```text
ImageFinder/
│
├── config/
│   └── settings.py
│
├── models/
│   ├── ocr_model.py
│   └── vector_db.py
│
├── services/
│   ├── indexer.py
│   └── searcher.py
│
├── data/
│   ├── images/
│   └── db/
│
├── main.py
├── .gitignore
└── README.md
```

---

## Project Components

### `config/settings.py`

Contains configuration for:

* Image directory
* ChromaDB storage directory
* Local folder creation

---

### `models/ocr_model.py`

Initializes **EasyOCR** and extracts text from images.

OCR processing is configured to run on the CPU.

---

### `models/vector_db.py`

Handles:

* ChromaDB initialization
* Persistent vector storage
* OpenCLIP embedding generation
* Image loading
* CUDA-based model execution

---

### `services/indexer.py`

Responsible for indexing images.

The indexer:

1. Finds supported image files.
2. Runs OCR extraction.
3. Generates image embeddings.
4. Stores embeddings and metadata in ChromaDB.
5. Handles failed image processing gracefully.

---

### `services/searcher.py`

Provides the two main search functions:

```python
search_visuals()
search_text()
```

`search_visuals()` performs semantic vector similarity search.

`search_text()` searches OCR metadata for matching text.

---

### `main.py`

Acts as the main application entry point for indexing and performing searches.

---

# Technology Stack

| Technology | Purpose                                        |
| ---------- | ---------------------------------------------- |
| Python     | Core application                               |
| OpenCLIP   | Image and text embeddings                      |
| ChromaDB   | Vector storage and semantic similarity search  |
| EasyOCR    | Text extraction from images                    |
| PyTorch    | Deep-learning model execution and CUDA support |

---

# Requirements

* Python 3.9+
* NVIDIA GPU
* CUDA-compatible PyTorch installation
* ChromaDB
* OpenCLIP
* EasyOCR

> The current implementation initializes OpenCLIP using CUDA, so an NVIDIA GPU with a compatible CUDA-enabled PyTorch installation is required.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yusri009/ImageFinder.git
cd ImageFinder
```

---

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install chromadb easyocr open_clip_torch
```

You will also need to install a **PyTorch version compatible with your CUDA environment**.

---

# Usage

## Step 1 — Add Images

Place the images you want to search inside:

```text
data/images/
```

Example:

```text
data/images/
├── beach.jpg
├── receipt.png
├── screenshot.png
└── dog.webp
```

---

## Step 2 — Index Images

Import the indexer:

```python
from services.indexer import index_images
from config.settings import IMAGE_FOLDER

index_images(IMAGE_FOLDER)
```

Then run:

```bash
python main.py
```

During indexing, ImageFinder will:

1. Detect supported image files.
2. Extract visible text using EasyOCR.
3. Generate OpenCLIP embeddings.
4. Store vectors and OCR metadata in ChromaDB.

---

# Visual Search

Import the visual search function:

```python
from services.searcher import search_visuals
```

Search using a natural-language description:

```python
search_visuals("person sitting")
```

Example output:

```text
--- Best Visual Match for 'person sitting' ---

Match: /path/to/data/images/example.jpg
Distance Score: 0.7421
```

Multiple results can be requested using:

```python
search_visuals("person sitting", max_results=5)
```

---

# Text Search

Import the text search function:

```python
from services.searcher import search_text
```

Search for text appearing inside indexed images:

```python
search_text("invoice")
```

Example output:

```text
--- Text Matches for 'invoice' ---

Match: /path/to/data/images/receipt.jpg
```

Multiple matches can be requested using:

```python
search_text("invoice", max_results=5)
```

---

# Example

Suppose an image has the filename:

```text
IMG_4837.jpg
```

The filename provides very little information about its contents.

If the image contains a dog outdoors, ImageFinder allows you to search:

```text
dog outside
```

and retrieve the image using semantic similarity.

If the image contains visible text such as:

```text
University of Moratuwa
```

you can instead search:

```text
University
```

using OCR-based text search.

---

# Future Improvements

Possible future extensions include:

* Desktop or web-based graphical interface
* Automatic directory monitoring
* Incremental indexing
* CPU fallback for OpenCLIP
* Combined OCR and semantic ranking
* Search-result image previews
* Recursive folder indexing
* Duplicate-image detection
* Batch processing
* Multilingual OCR
* Metadata filtering
* Configurable OpenCLIP models
* Standalone desktop packaging

---

# Privacy

ImageFinder follows a local-first design.

Images are processed on the user's machine, while the vector database is stored locally under:

```text
data/db/
```

The image collection does not need to be uploaded to an external search API for indexing or searching.

---

# Author

**Yusri Ahamed**

Computer Science & Engineering Undergraduate
University of Moratuwa

```
```
