"""
File: azure_pdf_container_client.py
Desc: handling I/O tasks with Blob Storage

"""

import os
from typing import List, Optional, Tuple

from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from loguru import logger


class AzurePDFContainerClient:
    def __init__(
        self,
        connection_string: str,
        container_name: str = "default_container",
        root_path_ingestion: str = "../",
    ):
        """
        Initialize the Azure PDF container client with a specified container name.

        Args:
            container_name (str): Name of the container to manage. Defaults to "default_container".
        """
        self.client: BlobServiceClient = BlobServiceClient.from_connection_string(
            connection_string
        )
        self.container_name: str = container_name
        self.root_path_ingestion = root_path_ingestion
        self._ensure_container_exists()

    def _ensure_container_exists(self) -> None:
        """Check if the container exists and create it if not."""
        container_client: ContainerClient = self.client.get_container_client(
            self.container_name
        )
        if not container_client.exists():
            container_client.create_container()
            logger.info(f"Container '{self.container_name}' created.")
        else:
            logger.info(f"Container '{self.container_name}' already exists.")

    def list_pdf_files(self) -> List[str]:
        """List all PDF files in the container."""
        container_client: ContainerClient = self.client.get_container_client(
            self.container_name
        )
        return [
            blob.name
            for blob in container_client.list_blobs()
            if blob.name.endswith(".pdf")
        ]

    def download_file(self, blob_name: str) -> Optional[bytes]:
        """Download a file from the container.

        Args:
            blob_name (str): The name of the blob to download.

        Returns:
            Optional[bytes]: The content of the blob if found, otherwise None.
        """
        try:
            container_client: ContainerClient = self.client.get_container_client(
                self.container_name
            )
            blob_client: BlobClient = container_client.get_blob_client(blob_name)
            return blob_client.download_blob().readall()
        except Exception as e:
            logger.error(f"Error downloading blob '{blob_name}': {e}")
            return None

    def ensure_download_directory(self, download_dir_name_: str) -> Tuple[str, str]:
        """Ensure download directory exists and return paths to the ingestion and download directories.

        Args:
            index_name (str): The name of the index to create a unique download directory.

        Returns:
            Tuple[str, str]: Paths to the ingestion and download directories.
        """
        # Get current working directory
        logger.info(f"Current working directory: {os.getcwd()}")

        # Construct ingestion and download directories
        ingestion_directory = os.path.join(self.root_path_ingestion, download_dir_name_)
        download_directory = os.path.join(ingestion_directory, "downloads")

        # Log the directories
        logger.info(f"Root ingestion path: {self.root_path_ingestion}")
        logger.info(f"Ingestion directory: {ingestion_directory}")
        logger.info(f"Download directory: {download_directory}")

        # Ensure the download directory exists
        os.makedirs(download_directory, exist_ok=True)

        return ingestion_directory, download_directory
