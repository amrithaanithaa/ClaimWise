from app.tools.claim_tools import (
    claim_status_tool,
    claim_details_tool,
    policy_details_tool,
    customer_details_tool,
    missing_documents_tool,
    hospital_network_tool,
)


print("CLAIM STATUS")
print(claim_status_tool("CLM300001"))

print("\nCLAIM DETAILS")
print(claim_details_tool("CLM300001"))

print("\nPOLICY DETAILS")
print(policy_details_tool("POL239115"))

print("\nCUSTOMER DETAILS")
print(customer_details_tool("CUST135804"))

print("\nMISSING DOCUMENTS")
print(missing_documents_tool("CLM300001"))

print("\nHOSPITAL NETWORK")
print(hospital_network_tool("HOSP1347"))