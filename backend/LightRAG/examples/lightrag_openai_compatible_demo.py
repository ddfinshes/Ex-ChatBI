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
WORKING_DIR = dr + "/dickens"  # 生成正确路径
print(dr, WORKING_DIR)

if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)


async def llm_model_func(
    prompt, system_prompt=None, history_messages=[], keyword_extraction=False, **kwargs
) -> str:
    return await openai_complete_if_cache(
        "o3-mini",
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
    # prompt = "WTD sales vs Target?"

    """

    
    """
    return  await rag.aquery(
            f"""You are a data analysis expert tasked with generating executable PostgreSQL code to calculate {prompt}. 

            Follow these steps: 
                1. Identify Query Constraints: 
                - For week-based date restrictions (e.g., "WTD" or "last week"), excluding weekid (e.g., "week 45"), convert them into a specific date range. Do not use built-in date functions.
                    - Example: If today is February 20, 2025, and the user asks for "WTD: From Sunday of this week to yesterday," use February 16 to February 19, 2025.
                - For weekid (e.g., "week 45"), use the format weekid = 202545 in the SQL code.
                2. Generate SQL: Write clear, executable PostgreSQL code to answer the user's query: {prompt}.
                3. Notice: Today is Thursday, February 20, 2025, and this week's weekid is 202545 (week 45).
                4. Output Format: Provide a clearly, understandable response including:
                    - Analysis: Clearly explain how the query is understood and the steps to solve it.
                    - SQL Code: Enclose the code in sql marks.
                    - Explanation: Clarify the SQL output for business users.
                5. You should strictly follow the output format.
                
                ***User Input Example:***
                this month's weekly comp growth % for sales.

                ***Output Example:***
                Analysis: .... ////Your(LLM's) understanding about this user question, analysis flow about how to solve this question.
                SQL Code:
                ```sql
                 SELECT 
                    week_id,
                        SUM(amt) as sales_amt,  
                        SUM(amt_notax) as Sales_notax , 
                        SUM(amt_notax)/SUM(lyd_amt_notax)-1 as sales_comp_per ,    
                    FROM 
                        dm_fact_sales_chatbi 
                    WHERE 
                        date_code between '2025-02-01' and '2025-02-28'
                        AND comp_flag ='Y' -- The store participating in the comp. 
                    GROUP BY 
                        week_id
                    ;
                ```
                Explanation: .... ////Answer Explain:Explain about this sql output help business user understanding why generate this sql output. 
            """,
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
