# from app.database.queries import get_claim_details

# claim_id="CLM300001"
# result=get_claim_details(claim_id)
# print(result)


#-----------------------------------------------
# from app.database.queries import get_policy_details


# policy_id = "POL239115"

# result = get_policy_details(policy_id)

# print(result)

#-----------------------------------------------

# from app.database.queries import get_customer_details


# customer_id = "CUST135804"

# result = get_customer_details(customer_id)

# print(result)

#---------------------------------------------------

# from app.database.queries import get_missing_documents


# claim_id = "CLM300001"

# result = get_missing_documents(claim_id)

# print(result)
#--------------------------------------------------

# from app.database.queries import check_hospital_network


# hospital_id = "HOSP1347"

# result = check_hospital_network(hospital_id)

# print(result)

#------------------------------------------------

from app.database.queries import get_claim_status


claim_id = "CLM300001"

result = get_claim_status(claim_id)

print(result)