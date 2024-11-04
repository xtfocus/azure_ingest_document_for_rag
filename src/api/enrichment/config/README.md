# Enrichment Configuration

This module provides configuration options for the enrichment service. Configuration values are primarily loaded from environment variables, ensuring flexibility across different environments. Each configuration option is validated to ensure necessary values are set.

## Configuration Options

### Azure Machine Learning Large Model (MLLM) Configurations
- **`OPENAI_API_VERSION`**: Specifies the API version to use with Azure MLLM.  
- **`AZURE_OPENAI_API_KEY`**: The API key for authenticating requests to Azure MLLM.
- **`AZURE_OPENAI_ENDPOINT`**: The endpoint URL for the Azure OpenAI service.
- **`AZURE_MLLM_DEPLOYMENT_MODEL`**: The deployment model identifier for the Azure MLLM instance.

### Azure Computer Vision Configurations
- **`AZURE_COMPUTER_VISION_ENDPOINT`**: The endpoint URL for the Azure Computer Vision service.
- **`AZURE_COMPUTER_VISION_KEY`**: The API key for authenticating requests to Azure Computer Vision.

### Enrichment Caching Configurations
- **`COL_ENRICHMENT_CACHE`**: Identifier for the enrichment cache collection.
- **`ENRICHMENT_CACHE_MAX_EXPIRY_IN_SEC`**: Sets the maximum cache expiry time (in seconds). The default is `2592000` seconds (30 days).  
  - **Values**: Positive integer or `-1` for unlimited expiry.  
  - **Note**: A value of `0` or any invalid input will cause an error.

### Cosmos DB Configurations
- **`AZURE_COSMOS_DB_URI`**: The endpoint URI for accessing Azure Cosmos DB.
- **`AZURE_COSMOS_DB_KEY`**: The primary key for authenticating to Azure Cosmos DB.
- **`AZURE_COSMOS_DB_DATABASE`**: The name of the database in Cosmos DB to use.
- **`AZURE_COSMOS_DB_ENRICHMENT_CONTAINER`**: The container (or collection) within Cosmos DB for storing enrichment data.

### Classifier Configuration
- **`classifier_config_data`**: Loads classifier configuration data from a local file, located at `./enrichment/config/classifier_config.json`.

### Usage Example
The configuration options are accessed through the `EnrichmentConfig` class, which reads values from environment variables. For example:

```python
from enrichment.config import enrichment_config

# Access Azure MLLM endpoint
mllm_endpoint = enrichment_config.mllm_endpoint

# Retrieve Cosmos DB URI
cosmos_db_uri = enrichment_config.cosmos_db_uri
```

## Default Values
For caching, a default Time-To-Live (TTL) of 30 days (`2592000` seconds) is set unless overridden by the `ENRICHMENT_CACHE_MAX_EXPIRY_IN_SEC` environment variable.

## Notes
- **Classifier Configuration**: The classifier configuration is loaded from a local file and not an environment variable. Make sure that `classifier_config.json` is available in the expected directory.
- **Error Validation**: This module performs validation to ensure critical configurations are not left undefined.

This setup ensures that the enrichment service has all the necessary configurations to connect to Azure services, manage caching, and utilize Cosmos DB
