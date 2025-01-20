import json

if __name__ == "__main__":
    # Database Schema Description
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
                # schema_description.append(f"  - {column_name}")
                schema_description.append(f"  - {column_name}: {column_description}")
            schema_description.append("\n")
        return "\n".join(schema_description)

    schema_description = generate_schema_description(metadata)
    # print("Query Result:", result)
    print(schema_description)
