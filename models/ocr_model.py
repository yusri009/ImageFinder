import easyocr

print("Loading OCR Model on CPU...")
# Add gpu=False to stop EasyOCR from stealing VRAM
reader = easyocr.Reader(['en'], gpu=False)

def get_ocr_text(filepath):
    ocr_result = reader.readtext(filepath, detail=0)
    return " ".join(ocr_result).lower()