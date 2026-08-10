import os
import time
from models.vector_db import get_collection
from models.ocr_model import get_ocr_text

def index_images(folder_path):
    collection = get_collection()
    
    uris = []
    metadatas = []
    ids = []
    
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    filenames = [f for f in os.listdir(folder_path) if f.lower().endswith(valid_extensions)]
    
    if not filenames:
        print(f"No images found in {folder_path}")
        return

    print(f"\n[1/2] Running EasyOCR on CPU for {len(filenames)} images...")
    start_ocr = time.time()
    
    for i, filename in enumerate(filenames):
        filepath = os.path.join(folder_path, filename)
        
        try:
            ocr_text = get_ocr_text(filepath)
            
            # DIAGNOSTIC PRINT: See what text was extracted
            print(f"  [{filename}] -> Detected Text: \"{ocr_text}\"")
            
            uris.append(filepath)
            metadatas.append({"filepath": filepath, "ocr_text": ocr_text})
            ids.append(filename)
        except Exception as e:
            print(f"  -> Skipping bad file '{filename}': {e}")
            continue
            
    print(f"✓ EasyOCR finished in {time.time() - start_ocr:.2f} seconds.")
    
    # Only add to database if we actually successfully processed some images
    if ids:
        print(f"\n[2/2] Generating OpenCLIP embeddings on GPU...")
        start_gpu = time.time()
        
        collection.add(
            ids=ids,
            uris=uris,
            metadatas=metadatas
        )
        print(f"✓ GPU Embedding finished in {time.time() - start_gpu:.2f} seconds!")
    else:
        print("No valid images were processed. Database was not updated.")