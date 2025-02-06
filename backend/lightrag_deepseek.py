import asyncio
import os
import inspect
import logging
from LightRAG.lightrag import LightRAG, QueryParam
from LightRAG.lightrag.llm.ollama import ollama_model_complete, ollama_embed
from LightRAG.lightrag.utils import EmbeddingFunc

def my_lightrag(user_query):
    WORKING_DIR = "./dickens"

    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

    if not os.path.exists(WORKING_DIR):
        os.mkdir(WORKING_DIR)

    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="deepseek-r1m:7b",
        llm_model_max_async=4,
        llm_model_max_token_size=32768,
        llm_model_kwargs={"host": "http://localhost:11434", "options": {"num_ctx": 32768}},
        embedding_func=EmbeddingFunc(
            embedding_dim=768,
            max_token_size=8192,
            func=lambda texts: ollama_embed(
                texts, embed_model="nomic-embed-text", host="http://localhost:11434"
            ),
        ),
    )

    # with open("./knowledge-base/kathy50_V8.txt", "r", encoding="utf-8") as f:
    #     rag.insert(f.read())

    # Perform naive search
    # print(
    #     rag.query("WTD sales vs Target?", param=QueryParam(mode="naive"))
    # )

    print(
        rag.query(user_query, param=QueryParam(mode="hybrid"))
    )

    # # stream response
    try:
        resp = rag.query(
            user_query,
            param=QueryParam(mode="hybrid", stream=True),
        )
    except Exception as e:
        print(f"Error: {e}")
        resp = "Error: " + str(e)
    return resp


    # async def print_stream(stream):
    #     async for chunk in stream:
    #         print(chunk, end="", flush=True)


    # if inspect.isasyncgen(resp):
    #     asyncio.run(print_stream(resp))
    # else:
    #     print(resp)
# my_lightrag("WTD sales vs Target?")