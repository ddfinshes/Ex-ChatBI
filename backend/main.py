from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from models.llm_deepseck import DeepSeek_Coder_LLM
# from utils.get_llm_deepseek import LLM
# from utils.getVisTag import get_vis_tag
from LightRAG.examples.lightrag_openai_compatible_demo import query
# lightrag have error for import 
# from lightrag_deepseek import my_lightrag
import uvicorn  # FastAPI推荐的生产级服务器
from typing import Dict, Any
from pydantic import BaseModel, Field
import re
import logging
from db.connect import excute_sql
from utils.getVisTag import get_vis_tag
from decimal import Decimal
from sentence_transformers import SentenceTransformer, util
# from db.connect import excute_sql

# 初始化FastAPI应用
app = FastAPI(
    title="NL2BI Backend",
    description="NL2BI系统的转换接口",
    version="1.0.0"
)

# 配置跨域请求（CORS）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["POST", "GET"],  # 根据实际需求调整
    allow_headers=["*"],
)


# 初始化DeepSeek模型（保持与原始代码相同的初始化方式）
# 注意：如果实际使用时需要保持模型实例，建议使用lifespan管理
# llm = DeepSeek_Coder_LLM(mode_name_or_path="/root/...")

# 获取LLM response中SQL 代码部分
def get_sql_code(sql_response):
    # 定义正则表达式模式来匹配```sql```代码块
    sql_pattern = r"```sql\n(.*?)\n```"

    # 使用re.findall()提取所有SQL代码块
    sql_code_blocks = re.findall(sql_pattern, sql_response, re.DOTALL)
    sql_code_blocks = [f"```sql\n{sql_code}\n```" for sql_code in sql_code_blocks]
    
    return sql_code_blocks

# 存储对话历史
conversation_history = []  # 列表存储历史查询
model = SentenceTransformer('all-MiniLM-L6-v2')  # 加载预训练模型计算相似度

@app.post("/api/query")
async def query_handler(request: Dict[str, Any]):
    """
    处理自然语言查询的核心端点
    参数:
    - data: 包含用户查询的JSON对象，格式示例: {"query": "显示季度销售额"}
    
    返回:
    - JSON响应: {"response": "生成的SQL语句"}
    """
    try:
        # 1. 参数提取与验证
        user_query = request['query']
        if not user_query:
            raise HTTPException(status_code=400, detail="Missing query parameter")
        
        # 2. 知识库检索+生成sql代码
        ###
        # rag_response: {
        # user_query_understanding: "",
        # thinking_flow: "",
        # final_sql_code: ""
        #  }
        ###
        print("==========================my_lightrag========================================")
        # sql_code = my_lightrag(user_query)

        sql_code = await query(user_query)

        # 3. 执行生成的sql 代码
        # excute_sql_output = excute_sql(sql_code.replace('```sql\n', '').replace('\n```', ''))

        excute_sql_output = {'column': ['month_id', 'sales_amt', 'sales_notax', 'sales_notax_mom_per'], 'data': [(202502, Decimal('-5235'), Decimal('-4634'), Decimal('-1.00029011188026305147'))]}

        final_response = {
            "code": sql_code,
            "data": excute_sql_output,
        }
        
        # 添加当前查询到历史
        conversation_history.append(user_query)

        # 计算与历史查询的相似度
        if len(conversation_history) > 1:
            # 生成当前查询的嵌入
            current_embedding = model.encode(user_query, convert_to_tensor=True)
            # 历史查询嵌入
            history_embeddings = model.encode(conversation_history[:-1], convert_to_tensor=True)
            # 计算余弦相似度
            similarities = util.cos_sim(current_embedding, history_embeddings)[0].tolist()
        else:
            similarities = []

        # 准备返回数据：历史查询和相似度
        history_with_similarity = [
            {"query": q, "similarity": sim}
            for q, sim in zip(conversation_history[:-1], similarities)
        ] if similarities else []

        # 按相似度降序排序并取 Top K（例如 K=3）
        top_k = sorted(history_with_similarity, key=lambda x: x["similarity"], reverse=True)[:3]

        # return {
        #     "sql_output": excute_sql_output,
        #     "top_k_similar": top_k  # 返回 Top K 相似历史查询
        # }

        # 4. chart准备数据
        # 思路：将用户query和查询得到的数据给到LLM，让其推荐可视化的格式（柱状图、折线图、饼状图）
        # user_query之后需要改成LLM理解过后的
        user_query = "What is the sales MOM% for APAC EC?"
        vis_data = get_vis_tag(user_query, excute_sql_output)
        # ===========================================================
        # vis_data = {
        #     "vis_tag": "bar-chart",
        #     "x": ["sales_amt", "sales_notax"],
        #     "y": [-5235, -4634],
        #     "title": "202502's sales for APAC EC",
        #     "x-legend": "class",
        #     "y-legend": "sales",
        #     "tooltip": "sales_notax_mom_per:-1.000290111880263"
        # }
        final_response['vis_data'] = vis_data

        # 返回标准化响应
        return {"response": final_response, "top_k_similar": top_k}
    
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
    # 生产部署推荐使用: 
    # uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
    # 确保这里的第一个参数是 app 对象
    uvicorn.run(
        app=app,  # 直接传递应用实例
        host="0.0.0.0",
        port=5000,
        reload=False  # 开发时启用热重载
    )