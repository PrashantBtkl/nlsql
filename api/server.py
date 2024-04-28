from fastapi import FastAPI
from pydantic import BaseModel

import helpers
from db import psql
from ai_assistant import groq
from prompts import text_to_sql_prompt

class QueryRequest(BaseModel):
    question: str
    db_url: str
    use_local_llm: bool = False

class QueryResponse(BaseModel):
    result: str | None = None

class API:
    def __init__(self):
        self.app = FastAPI()

        @self.app.post("/query/")
        async def generate_query(request: QueryRequest):
            conn = psql.Database(request.db_url)
            results = conn.get_tables()
            tables = helpers.tables_txt(results)
            prompt = text_to_sql_prompt.generate_prompt(tables, request.question)
            result = await groq.LLM().run_inference(prompt)
            conn.disconnect()

            response = QueryResponse()
            response.result = result.replace("\n", " ")
            return response

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
