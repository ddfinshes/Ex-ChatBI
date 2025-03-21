import os
import asyncio
import traceback

from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.utils import EmbeddingFunc
import numpy as np
import nest_asyncio

nest_asyncio.apply()
dr = os.path.dirname(os.path.abspath(__file__))  # 获取脚本所在目录
WORKING_DIR = dr + "\dickens"  # 生成正确路径
print(dr, WORKING_DIR)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await openai_complete_if_cache(
        "gpt-4o",
        prompt,
        system_prompt=system_prompt,
        history_messages=history_messages,
        api_key = 'sk-rzf6y244hnAJPxUE5eA02e5bA4Dd4098A3C21f96CeCe7a6f',
        #api_key='sk-234NEybMLmKyfLjp0bD64709016c4b67B0Cf405a2f90Ba7b',
        base_url='https://ai-yyds.com/v1',
        **kwargs,
    )


async def embedding_func(texts: list[str]) -> np.ndarray:
    return await openai_embed(
        texts,
        model="text-embedding-3-large",
        api_key='sk-dHMDhf5KdHlpA0XOE2Bd778f95C84431966d340fFdE56a26',
        base_url='https://ai-yyds.com/v1',
    )


async def get_embedding_dim():
    test_text = ["This is a test sentence."]
    embedding = await embedding_func(test_text)
    embedding_dim = embedding.shape[1]
    return embedding_dim


# function test
async def test_funcs():
    result = await llm_model_func("How are you?")
    print("llm_model_func: ", result)

    result = await embedding_func(["How are you?"])
    print("embedding_func: ", result)

async def query(prompt : str):
    embedding_dimension = await get_embedding_dim()
    rag = LightRAG(
        working_dir=WORKING_DIR,
        llm_model_func=llm_model_func,
        embedding_func=EmbeddingFunc(
            embedding_dim=embedding_dimension,
            max_token_size=8192,
            func=embedding_func,
        ),
    )
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path_1 = os.path.join(script_dir, "technical_terms.txt")
    file_path_2 = os.path.join(script_dir, "schema_information.txt")
    with open(file_path_1, "r", encoding="utf-8") as f:
        await rag.ainsert(f.read(), split_by_character="(****)\n")
    # with open("./sql_sample_kb-1.txt", "r", encoding="utf-8") as f:
    #     await rag.ainsert(f.read(), split_by_character="\n;")
    # Perform naive search
    # print(
    #     await rag.aquery(
    #         "You are a data analysis expert. Generate SQL code to calculate WTD Sales vs Target. Today is 2025/2/20, Thursday", param=QueryParam(mode="naive")
    #     )
    # )
    #
    # # Perform local search
    # print(
    #     await rag.aquery(
    #         "You are a data analysis expert. Generate SQL code to calculate WTD Sales vs Target. Today is 2025/2/20, Thursday", param=QueryParam(mode="local")
    #     )
    # )

    # Perform global search
    return  await rag.aquery(
            "You are a data analysis expert. Generate SQL code to calculate What is the sales MOM% for APAC EC?. Today is 2025/2/20, Thursday",
            param=QueryParam(mode="global")
    )

    # Perform hybrid search
    # print(
    #     await rag.aquery(
    #         "You are a data analysis expert. Generate SQL code to calculate WTD Sales vs Target. Today is 2025/2/20, Thursday",
    #         param=QueryParam(mode="hybrid"),
    #     )
    # )


# traceback.print_exc()

async def main():
    try:
        embedding_dimension = await get_embedding_dim()
        print(f"Detected embedding dimension: {embedding_dimension}")

        rag = LightRAG(
            working_dir=WORKING_DIR,
            llm_model_func=llm_model_func,
            embedding_func=EmbeddingFunc(
                embedding_dim=embedding_dimension,
                max_token_size=8192,
                func=embedding_func,
            ),
        )
        script_dir = os.path.dirname(os.path.abspath(__file__))  # 获取脚本所在目录
        file_path = os.path.join(script_dir, "technical_terms.txt")  # 生成正确路径

        with open(file_path, "r", encoding="utf-8") as f:
            await rag.ainsert(f.read(), split_by_character="(****)")
        # with open("./sql_sample_kb-1.txt", "r", encoding="utf-8") as f:
        #     await rag.ainsert(f.read(), split_by_character="\n;")
        # Perform naive search
        # print(
        #     await rag.aquery(
        #         "You are a data analysis expert. Generate SQL code to calculate WTD Sales vs Target. Today is 2025/2/20, Thursday", param=QueryParam(mode="naive")
        #     )
        # )
        #
        # # Perform local search
        # print(
        #     await rag.aquery(
        #         "You are a data analysis expert. Generate SQL code to calculate WTD Sales vs Target. Today is 2025/2/20, Thursday", param=QueryParam(mode="local")
        #     )
        # )

        # Perform global search
        # print(
        #     await rag.aquery(
        #         "You are a data analysis expert. Generate SQL code to calculate WTD Sales vs Target. Today is 2025/2/20, Thursday",
        #         param=QueryParam(mode="local"),
        #     )
        # )

        print(await query('abc'))
        # Perform hybrid search
        # print(
        #     await rag.aquery(
        #         "You are a data analysis expert. Generate SQL code to calculate WTD Sales vs Target. Today is 2025/2/20, Thursday",
        #         param=QueryParam(mode="hybrid"),
        #     )
        # )
    except Exception as e:
        print(f"An error occurred: {e}")
        # traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
