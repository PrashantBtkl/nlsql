import os
from groq import Groq

class LLM():
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    async def run_inference(self, prompt: str) -> str:
        chat_completion = self.client.chat.completions.create(
        messages=[
             {
                 "role": "user",
                 "content": prompt,
             }
        ],
        model="llama3-70b-8192",
        )
        return chat_completion.choices[0].message.content
