## Step
1. Start backend
uvicorn main:app --reload --host 0.0.0.0 --port 5000
uvicorn main:app --loop asyncio --host 0.0.0.0 --port 5000
2. Start frontend
```bash
cd ./frontend
npm install # you may omit if have run it.
npm run serve
# or
npm run dev
```