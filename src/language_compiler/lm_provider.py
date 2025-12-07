import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


# Maps friendly model names → HuggingFace weights
MODEL_MAP = {
    "deepseek": "deepseek-ai/deepseek-coder-1.3b-instruct",
    "qwen": "Qwen/Qwen2.5-1.5B-Instruct"
}


class LMProvider:
    """
    Unified LM interface for local, open-source LLMs.
    Supports:
        - Phi-3 Micro (default)
        - DeepSeek Coder 1.3B
        - Qwen2.5-1.5B
    """

    def __init__(self, model="deepseek"):
        if model in MODEL_MAP:
            self.model_name = MODEL_MAP[model]
        else:
            self.model_name = model

        print(f"[LMProvider] Loading model: {self.model_name}")

        dtype = torch.float16 if torch.cuda.is_available() else torch.float32

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float32,
            device_map="cpu"
        )

        # Create generation pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            do_sample=False,
            temperature=0.2,
            max_new_tokens=64
        )

    def complete(self, prompt: str, **kwargs) -> str:
        """
        Generate text for any of the supported models.
        """
        output = self.pipe(
            prompt,
            max_new_tokens=kwargs.get("max_tokens", 512),
            temperature=kwargs.get("temperature", 0.2),
            do_sample=False
        )[0]["generated_text"]
        
        # Remove the prompt from the output
        if output.startswith(prompt):
            output = output[len(prompt):]

        return output.strip()
