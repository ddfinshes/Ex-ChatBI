## Step
1. Start backend
conda activate dbgpt_env
<!-- uvicorn main:app --reload --host 0.0.0.0 --port 5000 -->
uvicorn main:app --loop asyncio --host 0.0.0.0 --port 5000
uvicorn main:app --reload --host 127.0.0.1 --port 8000 | cat
2. Start frontend
```bash
cd ./frontend
npm install # you may omit if have run it.
npm run serve
# or
npm run dev
```

get_sql_rag.py：sql example做few-shot
get_LLM4SQL.py: NL2SQL

# 测试语句
curl -X POST 'http://127.0.0.1:8000/api/query' \
  -H 'Content-Type: application/json' \
  -d '{"query":"what is the MTD sales achievement for China FP?"}'

curl -s -X POST 'http://127.0.0.1:8000/api/query?query=what%20is%20the%20MTD%20sales%20achievement%20for%20China%20FP%3F'