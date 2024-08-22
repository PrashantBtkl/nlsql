from fastapi import FastAPI
from pydantic import BaseModel
import json

import nlsql.helpers
from nlsql.db import psql
from nlsql.ai_assistant import groq
from nlsql.prompts import text_to_sql_prompt

class QueryRequest(BaseModel):
    question: str
    db_url: str
    use_local_llm: bool = False

class QueryResponse(BaseModel):
    error: bool = False
    error_message: str | None = None
    sql: str | None = None

class API:
    def __init__(self):
        self.app = FastAPI()

        @self.app.post("/query")
        async def generate_query(request: QueryRequest):
            conn = psql.Database(request.db_url)
            results = conn.get_tables()
            tables = helpers.tables_txt(results)
            prompt = text_to_sql_prompt.generate_prompt(tables, request.question)
            result = await groq.LLM().run_inference(prompt)
            conn.disconnect()

            json_result = json.loads(result)
            response = QueryResponse()

            response.error_message = json_result["error_message"]
            if response.error_message != "":
                response.error = True
            response.sql = json_result["sql"].replace("\n", " ")

            return response

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8000)
