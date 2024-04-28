import argparse

from db import psql
import llm
from prompts import text_to_sql_prompt

def main():
    parser = argparse.ArgumentParser(description="Convert natural language into SQL query")
    parser.add_argument("-m", "--model-path", type=str, required=False,
                        help="Path to the model file (in gguf format), if not provided it uses groq api for inference")
    parser.add_argument("-d", "--db-url", type=str, required=True,
                        help="PostgreSQL database URL link")
    parser.add_argument("-q", "--question", type=str, required=True,
                        help="Question to generate a SQL query")
    args = parser.parse_args()

    conn = psql.Database(args.db_url)
    results = conn.get_tables()
    tables = tables_txt(results)
    prompt = text_to_sql_prompt.generate_prompt(tables, args.question)
    result = llm.LLM(args.model_path).run_inference(prompt)
    print(result)
    conn.disconnect()

def tables_txt(results):
    tables = ""
    for _, row in enumerate(results):
        tables += f"""
        table: {row[0]}
        columns: {row[1]}
        """
    return tables

if __name__ == "__main__":
    main()

