from app.database.database import get_connection


def get_claim_details(claim_id: str):

    connection = get_connection()

    try:
        query = """
            SELECT
                claim_id,
                customer_id,
                policy_id,
                claim_status,
                claim_amount,
                approved_amount,
                diagnosis_or_loss_type,
                claim_date,
                rejection_or_adjustment_reason
            FROM claims
            WHERE claim_id = ?
        """

        cursor = connection.execute(query, (claim_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))

    finally:
        connection.close()

#================== get policy details=============
def get_policy_details(policy_id: str):
    connection = get_connection()

    try:
        query = """
            SELECT
                policy_id,
                customer_id,
                policy_type,
                product_name,
                policy_start_date,
                policy_end_date,
                sum_insured,
                annual_premium,
                policy_status,
                co_pay_pct,
                deductible,
                waiting_period_days
            FROM policies
            WHERE policy_id = ?
        """

        cursor = connection.execute(query, (policy_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))

    finally:
        connection.close()

#========================= get_customer_details()==============================

def get_customer_details(customer_id: str):
    connection = get_connection()

    try:
        query = """
            SELECT
                customer_id,
                customer_name,
                age,
                gender,
                city,
                state,
                customer_since,
                kyc_status,
                risk_segment
            FROM customers
            WHERE customer_id = ?
        """

        cursor = connection.execute(query, (customer_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))

    finally:
        connection.close()

#=============================  get_missing_documents()==============================
def get_missing_documents(claim_id: str):
    connection = get_connection()

    try:
        query = """
            SELECT
                claim_id,
                document_type,
                upload_status,
                verification_status,
                file_type
            FROM claim_documents
            WHERE claim_id = ?
              AND (
                  upload_status != 'Uploaded'
                  OR verification_status != 'Verified'
              )
        """

        cursor = connection.execute(query, (claim_id,))
        rows = cursor.fetchall()

        columns = [column[0] for column in cursor.description]

        return [dict(zip(columns, row)) for row in rows]

    finally:
        connection.close()

#====================== check_hospital_network()===========================

def check_hospital_network(hospital_id: str):
    connection = get_connection()

    try:
        query = """
            SELECT
                hospital_id,
                hospital_name,
                city,
                network_status,
                specialty
            FROM hospitals
            WHERE hospital_id = ?
        """

        cursor = connection.execute(query, (hospital_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))

    finally:
        connection.close()

#===========================  get_claim_status()==========================

def get_claim_status(claim_id: str):
    connection = get_connection()

    try:
        query = """
            SELECT
                claim_id,
                claim_status
            FROM claims
            WHERE claim_id = ?
        """

        cursor = connection.execute(query, (claim_id,))
        row = cursor.fetchone()

        if row is None:
            return None

        columns = [column[0] for column in cursor.description]

        return dict(zip(columns, row))

    finally:
        connection.close()
