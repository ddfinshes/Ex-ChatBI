from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from LightRAG.examples.lightrag_openai_compatible_demo import query
# lightrag have error for import 
# from lightrag_deepseek import my_lightrag
import uvicorn  # FastAPI推荐的生产级服务器
# from LightRAG.examples.lightrag_openai_compatible_demo import query
# lightrag have error for import 
# from lightrag_deepseek import my_lightrag
import uvicorn  # FastAPI推荐的生产级服务器
from typing import Dict, Any
from pydantic import BaseModel, Field
import re
import logging
from db.connect import excute_sql
# from utils.getVisTag import get_vis_tag
from decimal import Decimal
# from sentence_transformers import SentenceTransformer, util
# from db.connect import excute_sql
# from utils.get_sql2json import sql2json
import json
import LightRAG.examples.lightrag_openai_compatible_demo as rag
# from utils.get_NLExplain import ExplainAgent
# from utils.get_user_sql import SQLExtractAgent
from openai import OpenAI
import csv
from io import StringIO

# 初始化FastAPI应用
app = FastAPI(
    title="NL2BI Backend",
    description="NL2BI系统的转换接口",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # 根据实际需求调整
    allow_headers=["*"],
)

# 存储对话历史
conversation_history = []  # 列表存储历史查询
# model = SentenceTransformer('all-MiniLM-L6-v2')  # 加载预训练模型计算相似度
user_query = ""
sql_code = ""
excute_sql_output = {}

def get_extracted_sql(text):
    # 匹配获取sqlcode
    sql_code = re.search(r'```sql\n(.*?)\n```', text, re.DOTALL)
    if sql_code:
        extracted_sql = sql_code.group(1)
        print("提取的SQL代码:")
        print(extracted_sql)
    else:
        print("未找到SQL代码块")
    return extracted_sql


def analyze_relation(understanding : str, knowledge_base : list):
    client = OpenAI(
        base_url='https://api.nuwaapi.com/v1',
        api_key='sk-3El3h3N2q539ah6ofrqA1vQTm8iudtnQUQzhp9SsTltxeFNk'
    )



    result = []
    for i in range(len(knowledge_base)):
        result.append([])
        for j in range(2):
            print(knowledge_base[i][j])
            prompt = f'''I will provide you with two sentences. Please follow the process below to evaluate the two sentences:

            Identify and label which word or words in the first sentence are specialized terms that need explanation.

            Determine whether the second sentence provides an explanation for the terms in the first sentence.

            If an explanation is provided, label which parts of the second sentence contain the explanation.(you may label only a few words)
            Your response should follow the format below:
            If there is no relevance, answer "none".
            If there is relevance, first state the term(s), and in the next line, provide the part of the sentence that explains it. Do not include any additional content in your response!
            Please notice that, only when there's strong relation between two sentences should you reply content, or you reply none!!!!!
            first sentence: {understanding}
            second sentence: {knowledge_base[i][j]}'''
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are an expert in data analysis"},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
            result[i].append(response.choices[0].message.content)
    return result



# @app.post("/api/sql2json")
# async def get_sql2json():
#     try:
#         sql_code = "select * from chatbi"
#         sqljson = sql2json(sql_code)
#         print("Response data:", sqljson)
#         return sqljson
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))
#
# def get_extracted_sql(text):
#     # 匹配获取sqlcode
#     sql_code = re.search(r'```sql\n(.*?)\n```', text, re.DOTALL)
#     if sql_code:
#         extracted_sql = sql_code.group(1)
#         print("提取的SQL代码:")
#         print(extracted_sql)
#     else:
#         print("未找到SQL代码块")
#     return extracted_sql



# @app.post("/api/sql2json")
# async def get_sql2json(sql_code):
#     try:
#         explain = ExplainAgent(model_name="o3-mini")
#         explain.run(str(sql_code))
#         report = explain.getLeastAnalysisReport()
#         print(report, type(report))
#         return report
#     except Exception as e:
#         import traceback
#         traceback.print_exc()
#         raise HTTPException(status_code=500, detail=str(e))

# @app.post("/api/relatsql")
# async def get_relatsql(sql_query: Dict[str, Any], query_out: Dict[str, Any], click_info: Dict[str, Any]): #
#     print("sql_query: ",sql_query['text'])
#     print("query_out: ",query_out)
#     print("click_info: ",click_info)
#     sql_query = sql_query['text']
#     extractagent = SQLExtractAgent()
#     extractagent.run(sql_query, query_out, click_info)
#     report = extractagent.getLeastAnalysisReport()
#     print(report, type(report))
#     return report
#     pass
@app.post("/api/query")
async def query_handler(request: Dict[str, Any]):
    try:
        # 1. 参数提取与验证
        user_query = request['query']
        print("=====================user query=============================", user_query)
        
        if not user_query:
            raise HTTPException(status_code=400, detail="Missing query parameter")
        
        # 2. 知识库检索+生成sql代码
        print("==========================my_lightrag========================================")
        rag_response, context = await rag.query(user_query)

        print("---------------context----------------\n")
        print(context)
        print("\n--------------context---------------------")
        # Extract knowledge base
        csv_file = StringIO(context.strip('"id", "content"\n'))

        csv_reader = csv.reader(csv_file)

        list_of_lists = [row[1].split("**SQL query sample**:") for row in csv_reader]


        print(list_of_lists)



        # print("rag_response: ", rag_response)
        understanding = rag_response.split('\n')[0]
        sql_code = get_extracted_sql(rag_response)
        explanation = rag_response.split("```")[-1]

        # Analyze relation here
        pair_relevance = analyze_relation(understanding, list_of_lists)
        print(pair_relevance)

        # Highlight words
        highlight_words = []
        highlight_knowledges = []
        for l in pair_relevance:
            for word in l:
                if word != 'none':
                    highlight_words.append(word.split('\n')[0].strip())
                    highlight_knowledges.append(word.split('\n')[1].strip())

        print(highlight_words)

        # 连线
        liners = []
        for i in range(len(list_of_lists)):
            if pair_relevance[i][0] != 'none':
                liners.append(i + 1)
        print(liners)

        # 3. 执行生成的sql 代码
        excute_sql_output = excute_sql(sql_code)
        print(excute_sql_output)

        # excute_sql_output = {'column': ['month_id', 'sales_amt', 'sales_notax', 'sales_notax_mom_per'], 'data': [(202502, Decimal('-5235'), Decimal('-4634'), Decimal('-1.00029011188026305147'))]}

        final_response = {
            "understanding": understanding,
            "explanation": explanation,
            "code": sql_code,
            "data": excute_sql_output,
            "context": list_of_lists,
            "pair_relevance": pair_relevance,
            "highlight_words": highlight_words,
            "highlight_knowledges": highlight_knowledges,
            "liners": liners,
            "list_of_lists": list_of_lists
        }
        
        # 添加当前查询到历史
        # conversation_history.append(user_query)

        # # 计算与历史查询的相似度
        # if len(conversation_history) > 1:
        #     # 生成当前查询的嵌入
        #     current_embedding = model.encode(user_query, convert_to_tensor=True)
        #     # 历史查询嵌入
        #     history_embeddings = model.encode(conversation_history[:-1], convert_to_tensor=True)
        #     # 计算余弦相似度
        #     similarities = util.cos_sim(current_embedding, history_embeddings)[0].tolist()
        # else:
        #     similarities = []


        # # 准备返回数据：历史查询和相似度
        # history_with_similarity = [
        #     {"query": q, "similarity": sim}
        #     for q, sim in zip(conversation_history[:-1], similarities)
        # ] if similarities else []

        # 按相似度降序排序并取 Top K（例如 K=3）
        # top_k = sorted(history_with_similarity, key=lambda x: x["similarity"], reverse=True)[:3]

        # 4. chart准备数据
        # vis_data = get_vis_tag(user_query, excute_sql_output)
        # ===========================================================
        vis_data = {
            "vis_tag": "bar-chart",
            "x": ["sales_amt", "sales_notax"],
            "y": [-5235, -4634],
            "title": "202502's sales for APAC EC",
            "x-legend": "class",
            "y-legend": "sales",
            "tooltip": "sales_notax_mom_per:-1.000290111880263"
        }
        final_response['vis_data'] = vis_data

        # 返回标准化响应
        return {"response": final_response, "top_k_similar": 3}
        # return final_response

    
    except Exception as e:
        # 异常处理与日志记录
        import traceback
        traceback.print_exc()  # 打印完整堆栈跟踪
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/executesql")
def execute_sql(sql_code):
    excute_sql_res = excute_sql(sql_code[0].replace('```sql\n', '').replace('\n```', ''))
    return {"response": excute_sql_res}

if __name__ == "__main__":
    uvicorn.run(
        app=app,  # 直接传递应用实例
        host="0.0.0.0",
        port=5000,
        reload=False  # 开发时启用热重载
    )