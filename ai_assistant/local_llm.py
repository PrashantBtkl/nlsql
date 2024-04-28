from llama_cpp import Llama

class LLM:
    def __init__(self, model_path: str):
        """
        Initializes local llm of choice
        :param: model_path: path to local llm *.gguf
        """
        self.llm = Llama(
            model_path=model_path,
            n_ctx=5000,
            n_threads=5,
            n_gpu_layers=32,
            logits_all=True
        )

    def run_inference(self, prompt: str) -> str:
        """
        Executes query for llm
        :param: prompt: natural language query to run inference on
        """
        generation_kwargs = {
            "max_tokens":15000,
            "stop":["</s>"],
            "echo":False,
            "top_k":1
        }
        res = self.llm(prompt, **generation_kwargs)
        return res["choices"][0]["text"]
