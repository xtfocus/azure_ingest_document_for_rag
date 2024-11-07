# Azure OpenAI Custom Inference API

## Local Development

### Prerequisites
- Python 3.8+
- pip
- virtualenv

### Setup
1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with required environment variables:
```
AZURE_OPENAI_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here
```

### Running Locally

1. Development server:
```bash
uvicorn app:app --reload --port 8000
```

2. Production server using Gunicorn (Linux/Mac):
```bash
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Azure Container Apps Deployment

### Prerequisites
- Azure CLI
- Docker

### Deployment Steps

1. Login to Azure:
```bash
az login
```

2. Create Resource Group (if needed):
```bash
az group create --name myResourceGroup --location eastus
```

3. Create Azure Container Registry:
```bash
az acr create --resource-group myResourceGroup --name myacrname --sku Basic
az acr login --name myacrname
```

4. Build and push Docker image:
```bash
docker build -t myacrname.azurecr.io/customskill:v1 .
docker push myacrname.azurecr.io/customskill:v1
```

5. Create Container App:
```bash
az containerapp create \
  --name my-container-app \
  --resource-group myResourceGroup \
  --image myacrname.azurecr.io/customskill:v1 \
  --target-port 8000 \
  --ingress external \
  --env-vars \
    AZURE_OPENAI_KEY=your_key_here \
    AZURE_OPENAI_ENDPOINT=your_endpoint_here
```

### Testing Deployment
```bash
curl https://your-app-url/api/health
```

3. Create a Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
```
