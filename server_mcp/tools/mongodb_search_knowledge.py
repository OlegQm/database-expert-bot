import logging
import base64
from datetime import datetime
from typing import Dict, Any, Optional

from bson import ObjectId, Binary

from app.database import mongo_db
from app.utils import try_decode_json, try_extract_pdf_text
from app.server_mcp.schemas import MongoDBSearchParams

logger = logging.getLogger(__name__)

class MongoDBKnowledgeTool:
    def __init__(self):
        self._client = mongo_db
        self._collection = None
        self._initialized = False

    async def initialize(self):
        """
        Initializes the MongoDB 'knowledge' collection
            if it has not been initialized yet.

        Checks if the collection is already initialized;
        if not, retrieves or creates the 'knowledge' collection
        and marks it as initialized. Logs the initialization status.
        """
        if self._initialized:
            logger.debug("Already initialized.")
            return

        self._collection = self._client.get_or_create_collection("knowledge")
        self._initialized = True
        logger.info("MongoDB 'knowledge' collection initialized.")

    async def close(self):
        """Closing MongoDB connection."""
        if self._client:
            self._client.close()
            logger.info("MongoDB connection closed.")

    def _encode_mongo_document(self, doc):
        """
        Recursively encodes a MongoDB document into JSON-serializable types,
        with special handling for PDF and JSON file contents.

        - For PDF files, extracts and replaces the content
            with extracted text.
        - For JSON files, decodes and replaces the content
            with parsed JSON.
        - Handles ObjectId, Binary, datetime, and bytes types
            for JSON serialization.

        Args:
            doc:
                The MongoDB document (dict, list, or primitive type) to encode.

        Returns:
            The encoded document with all values converted
                to JSON-serializable types.
        """

        if isinstance(doc, dict):
            file_type = doc.get("header", {}).get("type")
            file_name = doc.get("header", {}).get("file_name", "")
            new_doc = {k: self._encode_mongo_document(v) for k, v in doc.items()}

            if "content" in doc:
                content = doc["content"]
                if (
                    file_type == "application/pdf"
                    and isinstance(content, (bytes, Binary))
                ):
                    content_bytes = (
                        bytes(content)
                        if isinstance(content, Binary)
                        else content
                    )
                    new_doc["content"] = try_extract_pdf_text(content_bytes)
                    logger.debug(
                        f"Extracted text from PDF for file: {file_name}"
                    )
                elif (
                    file_type == "application/json"
                    or file_name.lower().endswith(".json")
                ) and isinstance(content, (bytes, Binary)):
                    content_bytes = (
                        bytes(content)
                        if isinstance(content, Binary)
                        else content
                    )
                    new_doc["content"] = try_decode_json(content_bytes)
                    logger.debug(f"Decoded JSON content for file: {file_name}")
            return new_doc

        elif isinstance(doc, list):
            return [self._encode_mongo_document(item) for item in doc]
        elif isinstance(doc, ObjectId):
            return str(doc)
        elif isinstance(doc, Binary):
            return base64.b64encode(doc).decode('ascii')
        elif isinstance(doc, datetime):
            return doc.isoformat()
        elif isinstance(doc, bytes):
            return base64.b64encode(doc).decode('ascii')
        else:
            return doc

    async def execute_operation(
        self,
        operation: str,
        filter_dict: Optional[Dict[str, Any]] = None,
        limit: int = 0,
        sort: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Executes a MongoDB operation.

        Args:
            operation (str):
                The MongoDB operation to perform.
                Supported operations are "find", "find_one", and "count".
            filter_dict (Optional[Dict[str, Any]]):
                The filter criteria for the operation.
                Defaults to an empty dictionary.
            limit (int):
                The maximum number of documents
                to return (only applicable for "find").
                Defaults to 0 (no limit).
            sort (Optional[Dict[str, Any]]):
                The sorting criteria for the operation.
                Should be a dictionary mapping field names to sort directions.

        Returns:
            Dict[str, Any]: The result of the MongoDB operation.
                The structure of the result depends on the operation:
                - For "find": {"results": List[Dict[str, Any]]}
                - For "find_one": {"result": Optional[Dict[str, Any]]}
                - For "count": {"count": int}
                - For unsupported operations or errors: {"error": str}
        """
        if not self._initialized:
            await self.initialize()

        filter_dict = filter_dict or {}

        logger.info(
            f"Executing operation: {operation} with filter: " \
            f"{filter_dict}, limit: {limit}, sort: {sort}"
        )

        if not operation:
            logger.error("Operation is required but not provided.")
            return {"error": "Operation is required"}

        try:
            if operation == "find":
                cursor = self._collection.find(filter_dict)

                if limit > 0:
                    cursor = cursor.limit(limit)
                if sort:
                    cursor = cursor.sort([(k, v) for k, v in sort.items()])

                results = []
                for doc in cursor:
                    doc = self._encode_mongo_document(doc=doc)
                    results.append(doc)
                logger.info(f"Found {len(results)} documents.")
                return {"results": results}

            elif operation == "find_one":
                result = self._collection.find_one(filter_dict)
                if result:
                    result = self._encode_mongo_document(result)
                    logger.info("Found one document.")
                else:
                    logger.info("No document found.")
                return {"result": result}

            elif operation == "count":
                count = self._collection.count_documents(filter_dict)
                logger.info(f"Counted {count} documents.")
                return {"count": count}

            else:
                logger.error(f"Operation '{operation}' is not supported")
                return {"error": f"Operation '{operation}' is not supported"}

        except Exception as e:
            logger.error(f"Error executing MongoDB operation: {e}")
            return {"error": f"Database operation failed: {str(e)}"}


mongodb_tool = MongoDBKnowledgeTool()

async def mongodb_search_knowledge(
    params: MongoDBSearchParams
) -> Dict[str, Any]:
    """
    Query or modify data in MongoDB knowledge collection.

    Args:
        params:
            Parameters containing operation, filter, limit, and sort criteria

    Returns:
        Dict containing the results of the operation
    """
    return await mongodb_tool.execute_operation(
        operation=params.operation,
        filter_dict=params.filter,
        limit=params.limit,
        sort=params.sort
    )
