from config.settings import IMAGE_FOLDER
from services.indexer import index_images
from services.searcher import search_visuals, search_text

def main():
    print("Welcome to the Local Image Search Engine")
    
    # Example Workflow:
    
    # 1. Index your images (Put some photos in data/images first!)
    # Uncomment the line below to run the indexer once
    # index_images(IMAGE_FOLDER)
    
    # 2. Search for visual concepts
    search_visuals("sit")
    
    # 3. Search for specific words in the images
    # search_text("ipm")

if __name__ == "__main__":
    main()