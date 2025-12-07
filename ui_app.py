import streamlit as st
from src.language_compiler.pipeline import LanguageCompiler

st.set_page_config(
    page_title="Language Compiler",
    page_icon="🧩",
    layout="centered"
)

st.title("Language Compiler")
st.caption("Turn natural language → logic → pseudocode → optional Python code")

# --- Sidebar ---
with st.sidebar:
    st.subheader("Model Settings")

    model_choice = st.selectbox(
        "Choose Local Model",
        ["phi", "deepseek", "qwen"],
        index=0,
        help="All are free + local. 'phi' is fastest. 'deepseek' is strongest for reasoning."
    )

    gen_python = st.checkbox(
        "Generate Python code",
        value=False,
        help="Optional. Converts pseudocode → runnable Python stubs."
    )

st.write("### Enter your instruction:")
user_input = st.text_area(
    "",
    height=150,
    placeholder="Example:\nIf the temperature is above 25, turn on the AC unless it is raining."
)

if st.button("Compile"):
    if not user_input.strip():
        st.error("Please enter an instruction.")
    else:
        with st.spinner("Compiling with " + model_choice + "..."):
            compiler = LanguageCompiler(model=model_choice)
            out = compiler.compile(user_input.strip(), to_code=gen_python)

        # --- Reasoning Output ---
        st.subheader("Reasoning (Logic Plan)")
        if not out.reasoning.steps:
            st.warning("Model returned no reasoning steps. Try rephrasing.")
        else:
            for step in out.reasoning.steps:
                deps = f" → depends on: {', '.join(step.depends_on)}" if step.depends_on else ""
                st.markdown(f"- **[{step.role}]** `{step.id}`: {step.text}{deps}")

        st.subheader("Pseudocode")
        st.code(out.pseudocode.code, language="text")

        if gen_python and out.code:
            st.subheader("Python Code")
            st.code(out.code.code, language="python")

st.markdown("---")
st.caption("Built with local open-source models (Phi-3 Micro, DeepSeek Coder, Qwen 2.5B). No APIs. No cloud. 100% free.")
