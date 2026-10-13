from app.database.queries import (
    get_claim_status,
    get_claim_details,
    get_policy_details,
    get_customer_details,
    get_missing_documents,
    check_hospital_network,
)


def claim_status_tool(claim_id: str):
    return get_claim_status(claim_id)


def claim_details_tool(claim_id: str):
    return get_claim_details(claim_id)


def policy_details_tool(policy_id: str):
    return get_policy_details(policy_id)


def customer_details_tool(customer_id: str):
    return get_customer_details(customer_id)


def missing_documents_tool(claim_id: str):
    return get_missing_documents(claim_id)


def hospital_network_tool(hospital_id: str):
    return check_hospital_network(hospital_id)