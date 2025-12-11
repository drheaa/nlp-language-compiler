import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Maps friendly names → lightweight local models
MODEL_MAP = {
    "qwen-mini": "Qwen/Qwen2.5-0.5B-Instruct",
    "phi-mini": "microsoft/Phi-3.5-mini-instruct"
}


class LMProvider:
    """
    Lightweight LM interface for local, CPU-friendly open-source models.
    No API, no HF authentication needed.
    """

    def __init__(self, model: str = "qwen-mini"):
        # Map friendly names to full HuggingFace model paths
        if model in MODEL_MAP:
            self.model_name = MODEL_MAP[model]
        else:
            self.model_name = model  # allow full HF path

        print(f"[LMProvider] Loading local model: {self.model_name}")

        # Always use CPU for universal compatibility
        device = "cpu"
        torch_dtype = torch.float32  # safe for CPU

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        # Load model locally, CPU only
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            torch_dtype=torch_dtype,
            device_map={"": device}
        )

        # Generation pipeline
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            do_sample=False,          # deterministic output
            temperature=0.1,           # controlled randomness
            max_new_tokens=256        # safe default
        )

    def complete(self, prompt: str, **kwargs) -> str:
        """
        Generate text using a lightweight local model.
        """
        max_tokens = kwargs.get("max_tokens", 256)

        output = self.pipe(
            prompt,
            max_new_tokens=max_tokens,
            do_sample=False,
            temperature=0.1
        )[0]["generated_text"]

        # Remove the prompt prefix if model echoes it
        if output.startswith(prompt):
            output = output[len(prompt):]

        return output.strip()
