# Create the main project directory and navigate into it
mkdir -p ingestion_app && cd ingestion_app

# Create the main app directory and subdirectories
mkdir -p app/models app/services app/utils

# Create all the Python files in the app directory
touch app/main.py app/config.py

# Create files in models directory
touch app/models/__init__.py
touch app/models/schemas.py

# Create files in services directory
touch app/services/__init__.py
touch app/services/blob_storage.py
touch app/services/text_detection.py
touch app/services/processing_plan.py
touch app/services/ocr_processing.py
touch app/services/embedding.py
touch app/services/indexing.py

# Create files in utils directory
touch app/utils/__init__.py
touch app/utils/pdf_utils.py

# Create root level files
touch requirements.txt README.md
