import streamlit as st
import sys
import io
import contextlib

# Set page config
st.set_page_config(page_title="Python Console", layout="wide")

#  Initialize session state variables
if "code" not in st.session_state:
    st.session_state.code = ""
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {}
if "code_output" not in st.session_state:
    st.session_state.code_output = ""
if "waiting_for_input" not in st.session_state:
    st.session_state.waiting_for_input = False
if "run_code" not in st.session_state:
    st.session_state.run_code = False

#  Custom CSS for styling
st.markdown("""
    <style>
        body {
            color: white;
            background-color: #0e1117;
        }
        .stTextArea, .stButton, .stCode, .stTextInput {
            background-color: #161b22;
            color: white;
            border-radius: 5px;
        }
        .stButton>button {
            background-color: #c92a2a;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 10px 15px;
        }
        .stButton>button:hover {
            background-color: #9e1d1d;
        }
        .stTextInput>div>div>input {
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

#  UI Structure
st.title("🖥️ Python Console")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📥 Input")
    st.session_state.code = st.text_area("Write your Python code here:", st.session_state.code, height=250)

    #  Buttons under input section
    col_buttons = st.columns([1, 1])
    if col_buttons[0].button("Run Code"):
        st.session_state.run_code = True
        st.session_state.waiting_for_input = False
    if col_buttons[1].button("Clear Console"):
        st.session_state.code = ""  
        st.session_state.code_output = ""
        st.session_state.user_inputs = {}
        st.rerun()

with col2:
    st.markdown("### 📤 Output")
    if st.session_state.run_code:
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        missing_inputs = []

        #  Mock `input()` function
        def mock_input(prompt):
            if prompt not in st.session_state.user_inputs:
                st.session_state.user_inputs[prompt] = ""

            user_value = st.text_input(f"🔹 {prompt}", value=st.session_state.user_inputs[prompt], key=prompt)

            if user_value.strip() == "":
                missing_inputs.append(prompt)
                st.stop()

            st.session_state.user_inputs[prompt] = user_value
            return user_value

        if not missing_inputs:
            try:
                with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(error_buffer):
                    exec_globals = {"input": mock_input, "__name__": "__main__"}
                    exec(st.session_state.code, exec_globals)

                output = output_buffer.getvalue()
                error = error_buffer.getvalue()

                if error:
                    st.session_state.code_output = f"⚠️ Error: {error}"
                    st.error(error)
                else:
                    st.session_state.code_output = output
                    st.success("✅ Code executed successfully!")

            except Exception as e:
                st.session_state.code_output = f"⚠️ Error: {str(e)}"
                st.error(str(e))

            st.session_state.run_code = False

    st.code(st.session_state.code_output, language="python")


st.markdown("---")
st.markdown("###  Streamlit Test")
st.write("Use this to test Streamlit commands directly below:")

if st.button("Test Streamlit UI"):
    st.success(" Streamlit UI is working!")
    st.line_chart([1, 2, 3, 4, 5])
    st.bar_chart([5, 3, 7, 2])
    st.write(" Buttons, charts, and widgets work inside this app!")
