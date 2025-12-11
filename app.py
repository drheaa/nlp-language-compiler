import argparse
from src.language_compiler.pipeline import LanguageCompiler

def main():
    ap = argparse.ArgumentParser(
        description="Language Compiler: NL → Logic → Pseudocode → (Optional) Python"
    )

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
        "--interactive",
        action="store_true",
        help="Return missing clarification fields for ambiguous instructions"
    )

    ap.add_argument(
        "--model",
        type=str,
        default="qwen-mini",
        choices=["qwen-mini", "phi-mini"],
        help="Choose a lightweight local CPU model (default: qwen-mini)"
    )

    args = ap.parse_args()

    # Initialize compiler with selected model
    compiler = LanguageCompiler(model=args.model)

    # Run compile pipeline
    out = compiler.compile(
        args.instruction,
        to_code=args.code,
        interactive=args.interactive
    )

    # Print reasoning
    print("\n=== Reasoning (Logic Plan) ===")
    for step in out.reasoning.steps:
        deps = f"  depends_on={step.depends_on}" if step.depends_on else ""
        print(f"- [{step.role}] {step.id}: {step.text}{deps}")

    # Print pseudocode
    print("\n=== Pseudocode ===")
    print(out.pseudocode.code)

    # Print missing clarifications
    if out.clarifications_needed:
        print("\n=== Missing Clarifications ===")
        for f in out.clarifications_needed:
            print(f"- {f}")

    # Print Python code (optional)
    if out.code:
        print("\n=== Python Code ===")
        print(out.code.code)


if __name__ == "__main__":
    main()
