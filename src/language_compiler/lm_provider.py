import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Maps friendly names → lightweight local models
MODEL_MAP = {
    "qwen-mini": "Qwen/Qwen2.5-0.5B-Instruct",
    "phi-mini": "microsoft/Phi-3.5-mini-instruct"
}

class LMProvider:
    """
    Lightweight LM interface for local, CPU/GPU-friendly open-source models.

    - Uses GPU automatically if available
    - Falls back to CPU on laptops without VRAM
    - No paid API, no HF authentication needed
    """

    def __init__(self, model: str = "qwen-mini"):
        # Map friendly names to HF paths
        if model in MODEL_MAP:
            self.model_name = MODEL_MAP[model]
        else:
            self.model_name = model  # full HF path

        print(f"[LMProvider] Loading local model: {self.model_name}")

        # ----------------------------------------------------
        # Device Selection (Hybrid: GPU if available, else CPU)
        # ----------------------------------------------------
        if torch.cuda.is_available():
            device = "cuda"
            torch_dtype = torch.float16
            print("[LMProvider] CUDA detected → using GPU acceleration.")
        else:
            device = "cpu"
            torch_dtype = torch.float32
            print("[LMProvider] No GPU detected → using CPU.")

        # ----------------------------------------------------
        # Load tokenizer
        # ----------------------------------------------------
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )

        # ----------------------------------------------------
        # Load model (GPU/CPU automatically)
        # ----------------------------------------------------
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            trust_remote_code=True,
            torch_dtype=torch_dtype,
            device_map="auto"
        )

        # ----------------------------------------------------
        # Generation Pipeline
        # ----------------------------------------------------
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            do_sample=False,      # deterministic output
            temperature=0.1,      # good for JSON/pseudocode stability
            max_new_tokens=256    # safe default
        )

    def complete(self, prompt: str, **kwargs) -> str:
        """
        Generate text from the local model with deterministic output.
        """

        max_tokens = kwargs.get("max_tokens", 256)

        output = self.pipe(
            prompt,
            max_new_tokens=max_tokens,
            do_sample=False,
            temperature=0.1
        )[0]["generated_text"]

        # Remove prompt echo (common on small models)
        if output.startswith(prompt):
            output = output[len(prompt):]

        return output.strip()
