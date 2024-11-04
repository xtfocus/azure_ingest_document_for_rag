# Ingestion pipeline for Azure RAG application

Currently, the ingestion is performed in two ways:
- During initialization of the container app
- Using the UI from Azure portal

I aim to ease this by creating a webapp with CRUD operation for the search indexes. Benefits:
- don't have to visit the portal (which is visually cluttered and takes forever to load).
- separate functionality from the api (hosted on the container app)

To achieve my goal, I refer to following Azure-Samples:
- https://github.com/Azure-Samples/multimodal-rag-code-execution/
- https://github.com/Azure-Samples/rag-as-a-service-with-vision/

