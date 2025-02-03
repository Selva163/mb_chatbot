import duckdb as ddb
# %load_ext magic_duckdb
con = ddb.connect("mb_chatbot/ddb/oildata.db")

def load_table(table_name):
    with open(f"mb_chatbot/sql/create_{table_name}_table.sql", "r") as sql_query_file:
        sql_query = sql_query_file.read()
    con.sql(sql_query)
    print(f"{table_name} loaded")

load_table("overall")
load_table("expenses")
load_table("wells_dca_future_predictions")
load_table("wells_dca")
 
con.close()



