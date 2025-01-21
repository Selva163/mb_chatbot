import json
from openai import OpenAI
import streamlit as st
import duckdb
from autoviz.AutoViz_Class import AutoViz_Class
import sweetviz as sv
# from pandas_profiling import ProfileReport
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load OpenAI API Key
import os

# Step 1: Load Metadata
def load_metadata(file_path):
    with open(file_path, "r") as f:
        metadata = json.load(f)
    return metadata

metadata_path = "mb_chatbot/data/metadata.json"  # Update this path with your JSON metadata file
metadata = load_metadata(metadata_path)

# Step 2: Generate Schema Description from Metadata
def generate_schema_description(metadata):
    schema_description = []
    for table_name, table_info in metadata["tables"].items():
        schema_description.append(f"Table: {table_name}")
        schema_description.append(f"Description: {table_info['description']}")
        schema_description.append("Columns:")
        for column_name, column_description in table_info["columns"].items():
            schema_description.append(f"  - {column_name}: {column_description}")
        schema_description.append("\n")
    return "\n".join(schema_description)

schema_description = generate_schema_description(metadata)

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def generate_sql_query(prompt, schema_description):
    full_prompt = f"""
        You are a helpful assistant that translates natural language questions into SQL queries. 
        Backend is duckdb.
        Return only the SQL query. Dont have the 'sql' prefix. Always sort by metric_month before display as when applicable.
        Use the sum of all wells when asked about overall data or trend.
        When asked about wells data, dont group by month, unless asked about a well and its trend.
        Use the schema below to understand the database structure:

        {schema_description}

        Generate only the SQL query, no explanation or extra text. Avoid sql prefix

        Question: {prompt}
        """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        model="gpt-4o-mini",
    )
    # print(chat_completion)
    return chat_completion.choices[0].message.content.strip().replace('`','')

def generate_descriptions(prompt, response_data):
    full_prompt = f"""
        You are an analytical assistant providing key insights. Generate a one-line summary and 3-4 observations based on the data.
        You will be provided with user query and the data(response) for the user query.

        User query: {prompt}

        Data(response): {response_data.values}
        """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        model="gpt-4o-mini",
    )
    # print(chat_completion)
    return chat_completion.choices[0].message.content.strip()

def execute_query(query, database_path="mb_chatbot/ddb/oildata.db"):
    conn = duckdb.connect(database=database_path, read_only=True)
    try:
        df = conn.execute(query).fetchdf()
    except Exception as e:
        return str(e)
    finally:
        conn.close()
    return df


def generate_chart_code(prompt, response_data):
    full_prompt = f"""
        You are a data visualization expert for the oil and gas sector.
        You will be provided with user query and the corresponding data(response).
        Create a compelling visual based on the data.
        Send only the python code without the extra text.
        Dont generate instructions to run python code.
        Make sure the x-axis and y-axis has the proper text like whether the value is in thousands or millions.
        User query: {prompt}

        Data(response): {response_data.values}        
    """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        model="gpt-4o-mini",
    )
    print(chat_completion.choices[0].message.content.strip())
    return chat_completion.choices[0].message.content.strip()

# Function to execute the generated Python code
def execute_chart_code(chart_code, df):
    try:
        exec_globals = {"df": df, "plt": plt}
        exec(chart_code, exec_globals)
        fig = exec_globals["plt"].gcf()  # Get the current figure
        return fig
    except Exception as e:
        st.error(f"Error in generated code execution: {e}")
        return None

user_prompt = "whats the revenue trend look like?"
sql_query = generate_sql_query(user_prompt, schema_description)
result = execute_query(sql_query)

st.title("Ask me about Austin Salt flat")

# User input for prompt
user_prompt = st.text_input("Enter your query", "whats the revenue trend look like?")

# Button to trigger query execution
if st.button("Run Query"):
    try:
        # Generate SQL Query
        sql_query = generate_sql_query(user_prompt, schema_description)
        # st.write(f"Generated SQL Query:")
        # st.text(f"{sql_query}")

        # Execute SQL Query
        result = execute_query(sql_query)
        if isinstance(result, str):  # Error message
            st.error(result)
        else:  # Display result dataframe
            with st.spinner("Generating response..."):
                # st.dataframe(result)
                desccc = generate_descriptions(user_prompt, result)
                st.text(f"{desccc}")
                chart_code = generate_chart_code(user_prompt, result)
                chart_code = chart_code.replace('```python', '').replace('```', '').strip()
            with st.spinner("Rendering the chart..."):
                fig = execute_chart_code(chart_code, result)
                if fig:
                    # Display the chart
                    st.pyplot(fig)
    except Exception as e:
        st.error(f"Error: {str(e)}")