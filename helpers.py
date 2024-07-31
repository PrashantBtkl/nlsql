from ai_assistant import local_llm, groq

async def run_inference(model_path: str, prompt: str) -> str:
    if model_path == None:
        print("model not found, using groq to run inference")
        return await groq.LLM().run_inference(prompt)
    return local_llm.LLM(model_path).run_inference(prompt)

def tables_txt(results) -> str:
    tables = ""
    for _, row in enumerate(results):
        tables += f"table: {row[0]}\ncolumns:\n{row[1]}\n\n"
    return tables
