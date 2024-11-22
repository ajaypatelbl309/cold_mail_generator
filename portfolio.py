import pandas as pd
import uuid
import streamlit as st
from streamlit_chromadb_connection.chromadb_connection import ChromadbConnection


class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.collection_name = "portfolio"

        # Initialize the Streamlit ChromaDB connection
        self.conn = st.connection(
            "chromadb",
            type=ChromadbConnection,
            client="PersistentClient",
            path="/tmp/.chroma"  # Adjust the path if needed
        )

    def load_portfolio(self):
        # Fetch collection data to check if it's empty
        try:
            collection_data = self.conn.get_collection_data(self.collection_name)
        except Exception:
            collection_data = None

        if not collection_data or collection_data.empty:
            for _, row in self.data.iterrows():
                self.conn.add_to_collection(
                    collection_name=self.collection_name,
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        try:
            results = self.conn.query_collection(
                collection_name=self.collection_name,
                query_texts=skills,
                n_results=2
            )
            return results.get('metadatas', [])
        except Exception as e:
            st.error(f"Error querying collection: {e}")
            return []
