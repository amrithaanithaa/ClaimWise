import pandas as pd
from app.database.database import get_connection
from app.config import DATA_PATH


datasets = {
    "customers": DATA_PATH / "customers.csv",
    "policies": DATA_PATH / "policies.csv",
    "claims": DATA_PATH / "claims.csv",
    "claim_documents": DATA_PATH / "claim_documents.csv",
    "hospitals": DATA_PATH / "hospitals.csv",
    "customer_interactions": DATA_PATH / "customer_interactions.csv",
}


def load_data():
    connection = get_connection()

    try:
        for table_name, file_path in datasets.items():
            print(f"Loading {table_name}...")

            df = pd.read_csv(file_path)

            df.to_sql(
                table_name,
                connection,
                if_exists="replace",
                index=False
            )

            print(f"{table_name}: {len(df)} rows loaded")

    finally:
        connection.close()


if __name__ == "__main__":
    load_data()