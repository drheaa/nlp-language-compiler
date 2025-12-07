import argparse
from src.language_compiler.pipeline import LanguageCompiler

def main():
    ap = argparse.ArgumentParser(description="Language Compiler: NL → Logic → Pseudocode → (Optional) Python")

    ap.add_argument(
        "instruction",
        type=str,
        help="Natural-language instruction to compile"
    )

    ap.add_argument(
        "--code",
        action="store_true",
        help="Also generate Python code from pseudocode"
    )

    ap.add_argument(
        "--model",
        type=str,
        default="phi",
        choices=["phi", "deepseek", "qwen"],
        help="Choose which local model to use (default: phi)"
    )

    args = ap.parse_args()

    # Initialize compiler using selected model
    compiler = LanguageCompiler(model=args.model)

    # Run compile pipeline
    out = compiler.compile(args.instruction, to_code=args.code)

    # Print reasoning
    print("\n=== Reasoning (Logic Plan) ===")
    for step in out.reasoning.steps:
        deps = f"  depends_on={step.depends_on}" if step.depends_on else ""
        print(f"- [{step.role}] {step.id}: {step.text}{deps}")

    # Print pseudocode
    print("\n=== Pseudocode ===")
    print(out.pseudocode.code)

    # Print python code (optional)
    if out.code:
        print("\n=== Python Code ===")
        print(out.code.code)


if __name__ == "__main__":
    main()
