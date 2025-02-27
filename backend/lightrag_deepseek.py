import asyncio
import os
import inspect
import logging
from LightRAG.lightrag import LightRAG, QueryParam
from LightRAG.lightrag.llm.ollama import ollama_model_complete, ollama_embed
from LightRAG.lightrag.utils import EmbeddingFunc

def my_lightrag(user_query):
    WORKING_DIR = "./dickens/sql_sample_kb_glm"

    logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.INFO)

    if not os.path.exists(WORKING_DIR):
        os.mkdir(WORKING_DIR)
    # "deepseek-r1m:7b"
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=ollama_model_complete,
        llm_model_name="glm4",
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

    # 指定chunk分类标准
    # with open("./knowledge-base/sql_sample_kb2.txt", "r", encoding="utf-8") as f:
    #     rag.insert(f.read(), split_by_character="###", split_by_character_only=True)

    # Perform naive search
    # user_query ='Which store has the best wow sales growth%?'
    print('-------',
        # rag.query(prompt="Analyze the keywords in the query that may need to be retrieved and find out the meaning of these keywords in the knowledge base. The returned results only provide the searched keywords and their definitions.", query=user_query, param=QueryParam(mode="hybrid", top_k=10))
        rag.query(prompt="Based on the following information, write executable postgresql code that answers this question '%s'. WTD: From the first day (Sunday) of the current week to yesterday."%(user_query), query=user_query, param=QueryParam(mode="naive", top_k=5))
    )

    # # stream response
    try:
        resp = rag.query(
            user_query,
            param=QueryParam(mode="naive", stream=True),
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
my_lightrag("WTD sales vs Target? ")