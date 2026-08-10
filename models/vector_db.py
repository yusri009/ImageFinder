import chromadb
from chromadb.utils.embedding_functions import OpenCLIPEmbeddingFunction
from chromadb.utils.data_loaders import ImageLoader
from config.settings import DB_PATH

print("Initializing Vector Database and CLIP Model on GPU...")
client = chromadb.PersistentClient(path=DB_PATH)

# Add device="cuda" to explicitly route OpenCLIP to your MX550
clip_ef = OpenCLIPEmbeddingFunction(device="cuda")
image_loader = ImageLoader()

collection = client.get_or_create_collection(
    name="local_image_search",
    embedding_function=clip_ef,
    data_loader=image_loader
)

def get_collection():
    return collection