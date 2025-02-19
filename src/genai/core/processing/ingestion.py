from fastapi import HTTPException
import time
import json
import requests
import os

def divide_chunks(l, n): 
    logger.info({"message":"divide_chunks ","data":{"l":l,"n":n}})
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n]    

def upload_in_chunks(index_name,batch_array,action="upload"):
    logger.info({"message":"divide_chunks ","data":{"index_name":index_name,"batch_array":batch_array}})
    try :
        chunked_list = list(divide_chunks(batch_array, BATCH_SIZE))
        logger.info({ "message":"chunked_list ", "data":len(chunked_list)})
        result = []
        for list_item in enumerate(chunked_list):
            time.sleep(SLEEP_TIME_SEC)
            uploaded_list = upload_embeddings(index_name,list_item[1],action)
            logger.info({"message" :"upload_in_chunks result ","data" : uploaded_list})
            result.append(uploaded_list)
        return result  
    except Exception as e:
        raise e

def upload_embeddings(index_name, embeddings_list,action="upload"):
    logger.info({"message":"upload_embeddings ","data":{"index_name":index_name,"embeddings_list":embeddings_list}})	
    url = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/indexes/{index_name}/docs/index"
    querystring = {"api-version":"2023-07-01-Preview"}
    headers = {
        'api-key': AZURE_SEARCH_KEY,
        'content-type': "application/json"
    }
    proxies = { 
        "http"  : PROXY_URL,
        "https"  : PROXY_URL
    }
    logger.info({"message": "check len", "data":len(embeddings_list)})
    for idx,embed_obj in enumerate(embeddings_list):
        embed_obj.update({"@search.action": action})

    logger.info({"message":"upload_embeddings ","data":{"url":url,"proxies":proxies}})
    payload = {"value" : embeddings_list}
    logger.info({"message" :"payload ","data" : payload})
    try:
        response = requests.request("POST", url, data=json.dumps(payload), headers=headers, params=querystring,proxies=proxies if ENABLE_PROXY == "True" else None,verify=False)
        logger.info({"message" :"upload_embeddings response ","data" : {"response":response}})
        return response.content
    except Exception as e:
        logger.error({"message":"error in upload embedding","data":e.__str__(),"statusCode":500})


def start_ingestion(index_name,path):
    logger.info( {"message":"start_ingestion","data":{"request":index_name,"path":path}})
    upload_result = []
    try :
        for idx,file in enumerate(os.listdir(path)):
            logger.info({"message" :"starting to ingest ","data" : file})
            with open(path+file) as json_file:
                embeddings_list = json.load(json_file)
            json_file.close()    
            upload_result.append(upload_in_chunks(index_name, embeddings_list["upload_embeddings_list"]))
            logger.info( {"message":"start_ingestion","data":{"upload_result":upload_result,"len":len(upload_result)}})
        return upload_result
    except FileNotFoundError as ferror:
        logger.info({"message" :"FileNotFoundError ","data" : ferror})
        return HTTPException(detail = FileNotFoundError)

def start_ingestion_v1(index_name,file_path,action="upload"):
    logger.info( {"message":"start_ingestion","data":{"request":index_name,"path":file_path}})
    upload_result = []
    try :
        for idx,file in enumerate(os.listdir(file_path)):
            logger.info({"message" :"starting to ingest ","data" : file})
            with open(file_path+"/"+file) as json_file:
                embeddings_list = json.load(json_file)
            json_file.close()    
            upload_result.append(upload_in_chunks(index_name, embeddings_list["upload_embeddings_list"],action))
            logger.info( {"message":"start_ingestion","data":{"upload_result":upload_result,"len":len(upload_result)}})
        return upload_result
    except FileNotFoundError as ferror:
        logger.info({"message" :"FileNotFoundError ","data" : ferror})
        raise ferror
