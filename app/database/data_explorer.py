import pandas as pd

# Load datasets
customers_df = pd.read_csv("data/customers.csv")
policies_df = pd.read_csv("data/policies.csv")
claims_df = pd.read_csv("data/claims.csv")
claim_documents_df = pd.read_csv("data/claim_documents.csv")
hospitals_df = pd.read_csv("data/hospitals.csv")
interactions_df = pd.read_csv("data/customer_interactions.csv")


def display_dataset_info(name, df):
    print(f"\n{'=' * 50}")
    print(f"{name}")
    print(f"{'=' * 50}")

    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Columns:", df.columns.tolist())


display_dataset_info("CUSTOMERS", customers_df)
display_dataset_info("POLICIES", policies_df)
display_dataset_info("CLAIMS", claims_df)
display_dataset_info("CLAIM DOCUMENTS", claim_documents_df)
display_dataset_info("HOSPITALS", hospitals_df)
display_dataset_info("CUSTOMER INTERACTIONS", interactions_df)