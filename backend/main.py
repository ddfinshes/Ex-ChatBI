from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.llm_deepseck import DeepSeek_Coder_LLM
from crag import CRAG
from get_llm_deepseek import LLM
from lightrag_deepseek import my_lightrag
import uvicorn  # FastAPI推荐的生产级服务器
from typing import Dict, Any
from pydantic import BaseModel, Field
import re
import logging
from db.connect import excute_sql

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
        # 参数提取与验证
        user_query = request['query']
        
        if not user_query:
            raise HTTPException(status_code=400, detail="Missing query parameter")
        
        # 知识库检索
        rag_response = my_lightrag(user_query)
        
        # 构造LLM提示词
        llm_prompt = (
            f"Generate executable PostgreSQL code that correctly answers {user_query} "
            f"based on {rag_response}. "
        )
        
        # 调用LLM生成SQL
        sql_response = LLM(llm_prompt)
        logging.info('*** Generated SQL ***', sql_response)
        
        # 提取SQL代码块
        sql_code_blocks = get_sql_code(sql_response)
        # logging.info('*** SQL Code ***', sql_code_blocks)

        # 执行SQL代码
        excute_sql_res = excute_sql(sql_code_blocks[0].replace('```sql\n', '').replace('\n```', ''))
        print('*** excute_sql_res ***', excute_sql_res)


        # 返回标准化响应
        return {"response": sql_code_blocks[0]}
    
    except Exception as e:
        # 异常处理与日志记录
        import traceback
        traceback.print_exc()  # 打印完整堆栈跟踪
        raise HTTPException(status_code=500, detail=str(e))

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