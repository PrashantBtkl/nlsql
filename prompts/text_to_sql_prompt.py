from jinja2 import Environment, FileSystemLoader

def generate_prompt(tables: str, question: str) -> str:
    """
    Renders a Jinja2 template with provided variables.

    Args:
        tables (str): Content for the 'Tables' section.
        question (str): Content for the 'Question' section.

    Returns:
        str: Rendered template.
    """
    template_source = """
    You are a PostgreSQL expert.

    Please help to generate a PostgreSQL query to answer the question. Your response should ONLY be based on the given context and follow the response guidelines and format instructions.

    ===Tables
    {{ tables }}

    ===Response Guidelines
    1. If the provided context is sufficient, please generate a valid query without any explanations for the question. The query should start with a comment containing the question being asked.
    2. If the provided context is insufficient, please explain why it can't be generated.
    3. Please use the most relevant table(s).

    ===Question
    {{ question }}
    """

    env = Environment(loader=FileSystemLoader(""))
    template = env.from_string(template_source)
    rendered_template = template.render(tables=tables, question=question)
    return rendered_template
