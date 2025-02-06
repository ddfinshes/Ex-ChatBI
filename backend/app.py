from flask import Flask, request, jsonify
from flask_cors import CORS
from models.llm_deepseck import DeepSeek_Coder_LLM
from crag import CRAG
from get_llm_deepseek import LLM
from lightrag_deepseek import my_lightrag

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化DeepSeek模型
# llm = DeepSeek_Coder_LLM(mode_name_or_path="/root/UIST2025/Ex-ChatBI/deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct")

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query', '')
    rag_response = my_lightrag(user_query)
    # print('***rag_response*** ', rag_response)

    # 调用DeepSeek模型处理用户查询
    query = f"Generate executable PostgreSQL code that correctly answers {user_query} based on {rag_response}. You only need to return the SQL section, without any other text." 

    response = LLM(query)
    print('***response*** ', response)

    # 返回模型的响应
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)