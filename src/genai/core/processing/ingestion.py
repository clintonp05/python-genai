from fastapi import HTTPException
import time
import json
import requests
import os
from src.genai.core.connectors.http_connector import HTTPClient

from typing import Any, Dict, List, Iterable, Literal

def divide_chunks(l: List, n: int) -> Iterable[List]:
    for i in range(0, len(l), n):
        yield l[i:i + n]

def upload_in_chunks(
    index_name: str, 
    batch_array: List[Dict],
    action: str = "upload"
) -> List[bytes]:
    """
    Uploads a list of embeddings in chunks to Azure Search.
    
    Args:
    index_name (str): The Azure Search index name.
    batch_array (List[Dict]): The list of embeddings to be uploaded.
    action (str, optional): The action to be performed on the index. Defaults to "upload".
    
    Returns:
    List[bytes]: A list of the responses from Azure Search, one for each chunk.
    """
    try:
        chunked_list = list(divide_chunks(batch_array, BATCH_SIZE))
        result = []
        for list_item in enumerate(chunked_list):
            time.sleep(SLEEP_TIME_SEC)
            uploaded_list = upload_embeddings(index_name, list_item[1], action)
            result.append(uploaded_list)
        return result  
    except Exception as e:
        raise e

def upload_embeddings(
    index_name: str, 
    embeddings_list: List[Dict[str, Any]], 
    action: str = "upload"
) -> bytes:
    """
    Uploads a list of embeddings to Azure Search.

    Args:
    index_name (str): The Azure Search index name.
    embeddings_list (List[Dict[str, Any]]): The list of embeddings to be uploaded.
    action (str, optional): The action to be performed on the index. Defaults to "upload".

    Returns:
    bytes: The response from Azure Search.
    """
    url = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/indexes/{index_name}/docs/index"
    querystring = {"api-version": "2023-07-01-Preview"}
    headers = {
        'api-key': AZURE_SEARCH_KEY,
        'content-type': "application/json"
    }
    proxies = { 
        "http": PROXY_URL,
        "https": PROXY_URL
    }
    for embed_obj in embeddings_list:
        embed_obj.update({"@search.action": action})

    payload = {"value": embeddings_list}
    try:
        response = HTTPClient().execute_request(
            method='POST',
            url=url,
            headers=headers,
            body=payload,
            params=querystring,
            proxies=proxies if ENABLE_PROXY == "True" else None,
            verify=False
        )
        return response.content
    except Exception as e:
        raise e

def start_ingestion(index_name, path):
    upload_result = []
    try:
        files = os.scandir(path)
        for entry in files:
            if entry.is_file():
                with open(entry.path) as json_file:
                    embeddings_list = json.load(json_file)
                upload_result.append(upload_in_chunks(index_name, embeddings_list["upload_embeddings_list"]))
        return upload_result
    except FileNotFoundError as ferror:
        raise HTTPException(detail=str(ferror))

def start_ingestion_v1(
    index_name: str, 
    file_path: str, 
    action: Literal["upload", "merge", "mergeOrUpload"] = "upload"
) -> List[bytes]:
    """
    Uploads a list of embeddings to Azure Search.

    Args:
    index_name (str): The Azure Search index name.
    file_path (str): The path to the folder containing the JSON files.
    action (Literal["upload", "merge", "mergeOrUpload"], optional): The action to be performed on the index. Defaults to "upload".

    Returns:
    List[bytes]: The responses from Azure Search.
    """
    upload_result: List[bytes] = []
    try:
        for file in os.listdir(file_path):
            with open(os.path.join(file_path, file)) as json_file:
                embeddings_list: Dict[str, List[Dict[str, Any]]] = json.load(json_file)
            upload_result.append(upload_in_chunks(index_name, embeddings_list["upload_embeddings_list"], action))
        return upload_result
    except FileNotFoundError as ferror:
        raise HTTPException(detail=str(ferror))
