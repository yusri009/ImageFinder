# ImageFinder

# Local Image & Text Search Engine

A 100% offline, privacy-focused multimodal search engine for your local images. This tool allows you to search through your local photo folders using either **visual concepts** (e.g., "a dog playing in a park") or **exact text matches** (e.g., "invoice", "starbucks") found inside the images.

It uses **OpenCLIP** for understanding visual content and **EasyOCR** for reading text, storing everything locally in a **ChromaDB** vector database.

## Features
* **100% Local & Private:** No internet connection required after the initial model downloads. Your photos never leave your device.
* **Hybrid Search:** Search for "things" using AI embeddings, or search for "words" using Optical Character Recognition (OCR).
* **Optimized for Low VRAM:** Explicitly designed to prevent CUDA Out-of-Memory (OOM) errors on GPUs like the NVIDIA MX550 by splitting the workload (OpenCLIP on GPU, EasyOCR on CPU).
* **Robust Indexing:** Automatically skips corrupted files or massive 4K wallpapers that usually crash computer vision libraries.

## Prerequisites
* Python 3.9+
* An NVIDIA GPU with CUDA support (optional, but highly recommended for fast embedding generation)

## Installation

1. **Clone or create the project directory:**
   ```bash
   mkdir local_search_project
   cd local_search_project