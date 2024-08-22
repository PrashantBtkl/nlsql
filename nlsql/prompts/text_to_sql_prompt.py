from jinja2 import Environment, FileSystemLoader

def generate_prompt(tables: str, question: str) -> str:
    template_source = """
    You are a PostgreSQL expert.

    Please help to generate a PostgreSQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions.
    Tables columns will be given in '<column_name> <data_type>' format

    ===Tables
    {{ tables }}

    ===Response Guidelines
    1. If the provided context is sufficient, please generate a valid query without any explanations for the question.
    2. If the provided context is insufficient, please explain why it can't be generated.
    3. Please use the most relevant table(s).
    4. Response should ONLY have SQL and no other text, SQL SHOULD NOT be in code block

    ===Response JSON Format
        {
            "sql": "A generated SQL query when context is sufficient. By default return empty string",
            "error_message": "An explanation of failing to generate the query. By default return empty string"
        }

    ===Question
    {{ question }}
    """

    env = Environment(loader=FileSystemLoader(""))
    template = env.from_string(template_source)
    rendered_template = template.render(tables=tables, question=question)
    return rendered_template
