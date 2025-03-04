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
import random 

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

def handle_followup_click(question):
    """Function to handle when a follow-up question is clicked."""
    st.session_state["trigger_query"] = True
    st.session_state["user_input"] = question
    # st.rerun() 

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def generate_sql_query(prompt, schema_description):
    full_prompt = f"""
        You are a helpful assistant that translates natural language questions into SQL queries. 
        If the prompt is casual conversation, return appriopriate response instead of trying to generate sql and also mention you're a data analyst agent.
        Backend is duckdb. For adding months use 'date_add(metric_month, INTERVAL 2 month)' .
        For past months use 'metric_month - interval 2 month'.
        use is_forecasted = 0 if not asked about future trends or forecasted values.
        Return only the SQL query. Dont have the 'sql' prefix. Always sort by metric_month before display as when applicable.
        Use the sum of all wells when asked about overall data or trend.
        When asked about wells data, dont group by month, unless asked about a well and its trend.
        Use is_forecasted = 1 when asked about future trends or forecasted values for coming months. 
        avoid is_forecasted column for expense_data table.
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
        temperature=0.2,
    )
    # print(chat_completion)
    return chat_completion.choices[0].message.content.strip().replace('`','')

def execute_query(query, database_path="mb_chatbot/ddb/oildata.db"):
    conn = duckdb.connect(database=database_path, read_only=True)
    try:
        df = conn.execute(query).fetchdf()
    except Exception as e:
        print(e)
        st.text(f"{query}")
        return "END"
    finally:
        conn.close()
    return df

def generate_descriptions(prompt, response_data):
    full_prompt = f"""
        You are an analytical assistant providing key insights. Generate a one-line summary and 3-4 observations based on the data.
        You will be provided with user query and the data(response) for the user query. 
        Also suggest follow up questions relevant to the user query based on the schema description.
        Avoid explicitly mentioning json.

        Format response as JSON:
        {{
            "summary": "Brief summary here",
            "observations": ["Observation 1", "Observation 2"],
            "follow_ups": ["Follow-up question 1", "Follow-up question 2"]
        }}

        User query: {prompt}

        Data(response): {response_data.values}

        Schema description: {schema_description}

        """
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": full_prompt}
        ],
        model="gpt-4o-mini",
        temperature=0.2,
    )
    response_data =  chat_completion.choices[0].message.content.strip().replace('`','')
    # print(response_data)
    # return chat_completion.choices[0].message.content.strip()
    return json.loads(response_data)

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
        temperature=0.2,
    )
    # print(chat_completion.choices[0].message.content.strip())
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

st.title("Ask me about Austin Salt flat")

# User input for prompt
# user_prompt = st.text_input("Enter your query", "whats the revenue trend look like?")

if "messages" not in st.session_state:
    st.session_state.messages = []

follow_upsv = ["What is the production trend?", "How does it compare with the forecast?", "What are the key drivers?"]

for msg in st.session_state.messages:
    with st.container():
        if msg["role"] == "assistant":
            st.pyplot(msg["image"])
            st.markdown(f"**💡 Summary:** {msg['summary']}")  # Display summary
            for obs in msg['observations']:
                st.markdown(f"- {obs}")
            # st.image(msg["image"], use_column_width=True)  # Display image
            st.markdown("### 🔍 Related:")
            for q in msg["follow_ups"]:
                st.button(q, key=q, on_click=handle_followup_click, args=(q,))
        else:
            st.markdown(msg["content"])  # Display user question

if "trigger_query" not in st.session_state:
    st.session_state["trigger_query"] = False
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""

user_prompt = st.chat_input("Ask me anything about Austin Salt Flat...")
user_query = ""
if user_prompt:
    user_query = user_prompt

if st.session_state.get("trigger_query", False):
    user_query = st.session_state["user_input"]

# print([s for s in st.session_state.keys()])
if "trigger_query" in st.session_state:
    print("this", st.session_state["user_input"])
    print(st.session_state["trigger_query"])

if user_prompt or ("trigger_query" in st.session_state and st.session_state["trigger_query"]):
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.container():
        st.markdown(f"**You asked:** {user_query}") 
    with st.container():
        with st.spinner("Thinking..."):
            sql_query = generate_sql_query(user_query, schema_description)
            result = execute_query(sql_query)
            # print("result", result)
            if isinstance(result, pd.DataFrame) and not result.empty:
                response_data = generate_descriptions(user_query, result)
                # print(response_data)
                summary = response_data["summary"]
                observations = response_data["observations"]
                follow_ups = response_data["follow_ups"]

                chart_code = generate_chart_code(user_query, result).replace('```python', '').replace('```', '').strip()
                fig = execute_chart_code(chart_code, result)
                if fig:
                    st.pyplot(fig)

                response_data = {
                    "role": "assistant",
                    "summary": summary,
                    "image": fig,
                    "follow_ups": follow_ups,
                    "observations": observations
                }
                st.session_state.messages.append(response_data)

                st.markdown(f"**💡 Summary:** {summary}")
                for obs in observations:
                    st.markdown(f"- {obs}")

                st.markdown("### 🔍 Related:")
                for question in follow_ups:
                    st.button(question, key=question, on_click=handle_followup_click, args=(question,))
            else:
                st.markdown("⚠️ No relevant data found. Try rephrasing your question.")


st.markdown("""
    <style>
        /* Make chat look like Perplexity */
        .stChatMessage { 
            padding: 12px; 
            border-radius: 10px; 
            margin-bottom: 10px; 
            max-width: 80%; 
        }
        .stChatMessage.assistant { 
            background-color: #e0e7ff; 
            font-weight: bold; 
        }
        .stChatInput input { 
            border-radius: 20px; 
            padding: 12px; 
        }
        .stSpinner {
            color: #2563eb;
        }
    </style>
""", unsafe_allow_html=True)

