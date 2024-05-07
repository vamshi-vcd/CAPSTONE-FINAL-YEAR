import streamlit as st
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import PythonExporter
import io

# Function to execute IPython Notebook and capture output
def execute_notebook(notebook_file):
    try:
        # Read notebook content
        with open(notebook_file, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)

        # Create execute preprocessor
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        # Execute the notebook
        ep.preprocess(notebook, {'metadata': {'path': './'}})

        # Export executed notebook to Python script
        exporter = PythonExporter()
        exec_script, _ = exporter.from_notebook_node(notebook)

        # Capture output
        captured_output = io.StringIO()
        with io.capture_output() as captured:
            exec(exec_script)

        return captured_output.getvalue()
    except Exception as e:
        return f"Error occurred: {e}"

# Streamlit app
def main():
    st.title('MULTIMODAL FUSION TO ENHANCE HUMAN COMPUTER INTERACTION')

    # File paths of IPython Notebook files
    curlcounter_file = "curlcounter.ipynb"
    eyetracker_file = "eye tracker.ipynb"
    handtracker_file = "hand tracker.ipynb"

    # Align buttons at the center
    st.write("<div style='text-align: center;'>", unsafe_allow_html=True)

    # Button to execute curlcounter.ipynb
    st.markdown("<h3><b>Run Curl Counter</b></h3>", unsafe_allow_html=True)
    if st.button('Click here to open Virtual Gym Assistant', key="curlcounter" ):
        st.write("### Opening Curl Counter")
        output_curlcounter = execute_notebook(curlcounter_file)
        st.code(output_curlcounter, language='python')

    # Button to execute eye tracker.ipynb
    st.markdown("<h3><b>Run Eye Tracker</b></h3>", unsafe_allow_html=True)
    if st.button('Click here to open Eye Tracking Mouse', key="eyetracker"):
        st.write("### Opening Eye Tracker")
        output_eyetracker = execute_notebook(eyetracker_file)
        st.code(output_eyetracker, language='python')

    # Button to execute hand tracker.ipynb
    st.markdown("<h3><b>Run Hand Tracker</b></h3>", unsafe_allow_html=True)
    if st.button('Click here to open Hand Tracking Mouse', key="handtracker"):
        st.write("### Opening Hand Tracker")
        output_handtracker = execute_notebook(handtracker_file)
        st.code(output_handtracker, language='python')

    st.write("</div>", unsafe_allow_html=True)

# Run the Streamlit app
if __name__ == "__main__":
    main()
