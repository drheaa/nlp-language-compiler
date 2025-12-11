import streamlit as st
from src.language_compiler.pipeline import LanguageCompiler

st.set_page_config(
    page_title="Language Compiler",
    page_icon="🧩",
    layout="centered"
)

st.title("Language Compiler")
st.caption("Turn natural language → logic → pseudocode → optional Python code using free, local models.")

# --- Sidebar ---
with st.sidebar:
    st.subheader("Model Settings")

    model_choice = st.selectbox(
        "Choose Local Model",
        ["qwen-mini", "phi-mini"],
        index=0,
        help="Both are free and run on CPU. 'qwen-mini' is smallest and fastest."
    )

    gen_python = st.checkbox(
        "Generate Python code",
        value=False,
        help="Optional: Converts pseudocode → runnable Python stubs."
    )

    interactive_mode = st.checkbox(
        "Interactive (show missing clarifications)",
        value=True,
        help="Shows which thresholds or values are missing (e.g., TODO fields)."
    )

st.write("### Enter your instruction:")
user_input = st.text_area(
    "",
    height=150,
    placeholder="Example:\nIf the queue gets too long, open another counter after a while."
)

if st.button("Compile"):
    if not user_input.strip():
        st.error("Please enter an instruction.")
    else:
        with st.spinner(f"Compiling with {model_choice}..."):
            compiler = LanguageCompiler(model=model_choice)
            out = compiler.compile(
                user_input.strip(),
                to_code=gen_python,
                interactive=interactive_mode
            )

        # --- Reasoning Output ---
        st.subheader("Reasoning (Logic Plan)")
        if not out.reasoning.steps:
            st.warning("Model returned no reasoning steps. Try rephrasing.")
        else:
            for step in out.reasoning.steps:
                deps = f" → depends on: {', '.join(step.depends_on)}" if step.depends_on else ""
                st.markdown(f"- **[{step.role}]** `{step.id}`: {step.text}{deps}")

        # --- Pseudocode ---
        st.subheader("Pseudocode")
        st.code(out.pseudocode.code, language="text")

        # --- Missing Clarifications ---
        if interactive_mode and out.clarifications_needed:
            st.subheader("Missing Clarifications")
            st.warning(
                "The instruction contains ambiguous terms. Please provide values for:"
            )
            for f in out.clarifications_needed:
                st.markdown(f"- **{f}**")

        # --- Python Code ---
        if gen_python and out.code:
            st.subheader("Python Code")
            st.code(out.code.code, language="python")

st.markdown("---")
st.caption("Runs 100% locally on lightweight CPU models (Qwen2.5-0.5B, Phi-3.5-mini). No paid APIs.")
