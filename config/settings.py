import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database and Image paths
DB_PATH = os.path.join(BASE_DIR, "data", "db")
IMAGE_FOLDER = os.path.join(BASE_DIR, "data", "images")

# Ensure the data directories exist
os.makedirs(DB_PATH, exist_ok=True)
os.makedirs(IMAGE_FOLDER, exist_ok=True)