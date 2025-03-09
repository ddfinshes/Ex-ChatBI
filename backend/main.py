from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.llm_deepseck import DeepSeek_Coder_LLM
import uvicorn 
from typing import Dict, Any
from pydantic import BaseModel, Field
import re
import logging
from db.connect import excute_sql
from LightRAG.examples.lightrag_openai_compatible_demo import query

app = FastAPI(
    title="NL2BI Backend",
    description="NL2BI系统的转换接口",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["POST", "GET"],  
    allow_headers=["*"],
)
def get_sql_code(sql_response):
    sql_pattern = r"```sql\n(.*?)\n```"

    sql_code_blocks = re.findall(sql_pattern, sql_response, re.DOTALL)
    sql_code_blocks = [f"```sql\n{sql_code}\n```" for sql_code in sql_code_blocks]
    
    return sql_code_blocks

# 存储对话历史
conversation_history = []  # 列表存储历史查询
# model = SentenceTransformer('all-MiniLM-L6-v2')  # 加载预训练模型计算相似度

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
        sql_code = await query(user_query)

        # 3. 执行生成的sql 代码
        excute_sql_output = excute_sql(sql_code.replace('```sql\n', '').replace('\n```', ''))
        final_response = {
            "code": sql_code,
            "data": excute_sql_output,
        }
        
        # 添加当前查询到历史
        conversation_history.append(user_query)

        # 计算与历史查询的相似度
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
        #
        # # 按相似度降序排序并取 Top K（例如 K=3）
        # top_k = sorted(history_with_similarity, key=lambda x: x["similarity"], reverse=True)[:3]

        # return {
        #     "sql_output": excute_sql_output,
        #     "top_k_similar": top_k  # 返回 Top K 相似历史查询
        # }

        # 4. chart准备数据
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
        return {"response": final_response, "top_k_similar": 3} # modified
    
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