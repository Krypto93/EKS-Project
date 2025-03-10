import streamlit as st
import sys
import io
import contextlib
import subprocess
import os

# Set page config
st.set_page_config(page_title="Python Console & App Tester", layout="wide")

# ✅ Initialize session state variables
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

# ✅ Custom CSS for styling
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

# ✅ Function to Install Python Packages
def install_package(package):
    if not package.strip():
        return "⚠️ Please enter a valid package name."
    
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", package], capture_output=True, text=True)
        if result.returncode == 0:
            return f"✅ Successfully installed {package}"
        else:
            return f"❌ Error installing {package}: {result.stderr}"
    except Exception as e:
        return f"❌ Exception: {str(e)}"

# ✅ Function to Run Python Script
def run_python_script(script_path):
    try:
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return "", str(e)

# ✅ UI Structure
st.title("🚀 Python Console & Application Tester")

tab1, tab2 = st.tabs(["🔹 Python Console", "📂 Upload & Test Python Apps"])

# **🔹 Tab 1: Python Console**
with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📥 Python Code Input")
        st.session_state.code = st.text_area("Write your Python code here:", st.session_state.code, height=250)

        # ✅ Buttons under input section
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

            # ✅ Mock `input()` function
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

# **📂 Tab 2: Upload & Test Python Apps**
with tab2:
    st.markdown("### 📂 Upload Your Python Application")
    uploaded_file = st.file_uploader("Upload a `.py` file", type=["py"])

    if uploaded_file:
        # Save the uploaded file temporarily
        script_path = os.path.join("uploaded_script.py")
        with open(script_path, "wb") as f:
            f.write(uploaded_file.getvalue())

        st.success(f"✅ Uploaded `{uploaded_file.name}` successfully!")

        # ✅ Run Script Button
        if st.button("Run Uploaded Python Script"):
            st.info("⏳ Running script...")
            output, error = run_python_script(script_path)

            # ✅ Display Output
            st.markdown("### 📤 Output")
            if output:
                st.code(output, language="python")
            else:
                st.write("No output generated.")

            # ✅ Display Errors (if any)
            if error:
                st.markdown("### ❌ Errors")
                st.error(error)

# ✅ Package Installation Section
st.markdown("---")
st.markdown("### 📦 Install Python Packages")
package_name = st.text_input("Enter package name to install (e.g., `flask`, `numpy`):", "")

if st.button("Install Package"):
    if package_name.strip():  # Ensure non-empty input
        output = install_package(package_name)
        st.write(output)
    else:
        st.error("⚠️ Please enter a package name.")

# ✅ Streamlit Test UI
st.markdown("---")
st.markdown("### 🖥️ Streamlit Test")
st.write("Use this to test Streamlit commands directly below:")

if st.button("Test Streamlit UI"):
    st.success("✅ Streamlit UI is working!")
    st.line_chart([1, 2, 3, 4, 5])
    st.bar_chart([5, 3, 7, 2])
    
