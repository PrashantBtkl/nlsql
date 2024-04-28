import argparse

import helpers
from api import server
from db import psql
from ai_assistant import local_llm, groq
from prompts import text_to_sql_prompt

def main():
    parser = argparse.ArgumentParser(description="Convert natural language into SQL query")
    parser.add_argument("-m", "--model-path", type=str, required=False,
                        help="Path to the model file (in gguf format), if not provided it uses groq api for inference")
    parser.add_argument("-d", "--db-url", type=str, required=False,
                        help="PostgreSQL database URL link")
    parser.add_argument("-q", "--question", type=str, required=False,
                        help="Question to generate a SQL query")
    parser.add_argument("-s", "--server", action='store_true', required=False,
                        help="Serve nlsql as http server")
    args = parser.parse_args()

    while args.server == True:
        s = server.API()
        s.run()

    conn = psql.Database(args.db_url)
    results = conn.get_tables()
    tables = helpers.tables_txt(results)
    prompt = text_to_sql_prompt.generate_prompt(tables, args.question)
    result = helpers.run_inference(args.model_path, prompt)
    conn.disconnect()
    print(result)

if __name__ == "__main__":
    main()

