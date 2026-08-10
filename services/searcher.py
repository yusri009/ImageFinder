from models.vector_db import get_collection

def search_visuals(query, max_results=1):
    """Searches the visual embeddings using CLIP and returns the best match."""
    collection = get_collection()
    
    results = collection.query(
        query_texts=[query],
        n_results=max_results,
        include=['uris', 'distances'] 
    )
    
    print(f"\n--- Best Visual Match for '{query}' ---")
    
    if not results.get('uris') or not results['uris'][0]:
        print("No matches found.")
    else:
        best_uri = results['uris'][0][0]
        best_distance = results['distances'][0][0]
        
        print(f"Match: {best_uri}")
        print(f"Distance Score: {best_distance:.4f}")

def search_text(word, max_results=3):
    """Searches the metadata for exact or partial words using Python string matching."""
    collection = get_collection()
    
    # Retrieve all items and their metadata from the collection
    results = collection.get(include=['uris', 'metadatas'])
    
    target_word = word.lower()
    matches = []
    
    if results and results.get('metadatas'):
        for uri, meta in zip(results['uris'], results['metadatas']):
            ocr_text = meta.get('ocr_text', '').lower()
            if target_word in ocr_text:
                matches.append((uri, ocr_text))
                
    print(f"\n--- Text Matches for '{word}' ---")
    if not matches:
        print("No matches found.")
    else:
        for uri, text in matches[:max_results]:
            print(f"Match: {uri}")
            # print(f"  -> Extracted Text found: \"{text}\"")