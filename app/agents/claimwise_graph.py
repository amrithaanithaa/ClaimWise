
import re
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from app.rag.rag_pipeline import answer_policy_question
from app.tools.claim_tools import (
    claim_status_tool,
    claim_details_tool,
    policy_details_tool,
    customer_details_tool,
    missing_documents_tool,
    hospital_network_tool,
)


# --------------------------------------------------
# 1. Shared state passed between LangGraph nodes
# --------------------------------------------------

class ClaimWiseState(TypedDict, total=False):
    question: str
    route: str
    claim_id: str
    policy_id: str
    customer_id: str
    hospital_id: str
    sql_result: Any
    rag_result: dict
    answer: str


# --------------------------------------------------
# 2. Extract IDs from the user's question
# --------------------------------------------------

def extract_ids(question: str) -> dict:
    patterns = {
        "claim_id": r"\bCLM\d+\b",
        "policy_id": r"\bPOL\d+\b",
        "customer_id": r"\bCUST\d+\b",
        "hospital_id": r"\bHOSP\d+\b",
    }

    extracted = {}

    for key, pattern in patterns.items():
        match = re.search(pattern, question, re.IGNORECASE)

        if match:
            extracted[key] = match.group(0).upper()

    return extracted


# --------------------------------------------------
# 3. Route the question to SQL, RAG, or hybrid
# --------------------------------------------------

def route_question(state: ClaimWiseState) -> dict:
    question = state["question"]
    text = question.casefold()
    ids = extract_ids(question)

    policy_terms = (
        "coverage",
        "covered",
        "exclusion",
        "excluded",
        "waiting period",
        "maternity",
        "hospitalization",
        "policy condition",
        "policy terms",
        "policy clause",
    )

    sql_terms = (
        "claim status",
        "claim details",
        "approved amount",
        "missing document",
        "documents missing",
        "customer details",
        "customer information",
        "policy details",
        "premium",
        "sum insured",
        "hospital network",
        "network hospital",
    )

    needs_policy_evidence = any(
        term in text for term in policy_terms
    )

    has_record_id = bool(ids)

    # Claim-specific questions needing both database
    # information and policy evidence.
    if ids.get("claim_id") and needs_policy_evidence:
        route = "hybrid"

    # Questions about known database records.
    elif has_record_id and (
        any(term in text for term in sql_terms)
        or not needs_policy_evidence
    ):
        route = "sql"

    # General policy questions.
    else:
        route = "rag"

    return {
        **ids,
        "route": route,
    }


# --------------------------------------------------
# 4. SQL node
# --------------------------------------------------

def sql_node(state: ClaimWiseState) -> dict:
    question = state["question"].casefold()

    claim_id = state.get("claim_id")
    policy_id = state.get("policy_id")
    customer_id = state.get("customer_id")
    hospital_id = state.get("hospital_id")

    if claim_id:
        if (
            "missing document" in question
            or "documents missing" in question
        ):
            result = missing_documents_tool(claim_id)

        elif "status" in question:
            result = claim_status_tool(claim_id)

        else:
            result = claim_details_tool(claim_id)

    elif policy_id:
        result = policy_details_tool(policy_id)

    elif customer_id:
        result = customer_details_tool(customer_id)

    elif hospital_id:
        result = hospital_network_tool(hospital_id)

    else:
        result = (
            "Please include a valid claim, policy, customer, "
            "or hospital ID for a record lookup."
        )

    return {
        "sql_result": result,
        "answer": f"Structured database result:\n{result}",
    }


# --------------------------------------------------
# 5. RAG node
# --------------------------------------------------

def rag_node(state: ClaimWiseState) -> dict:
    result = answer_policy_question(
        state["question"],
        top_k=5,
    )

    return {
        "rag_result": result,
        "answer": result["answer"],
    }


# --------------------------------------------------
# 6. Hybrid node
# Claim -> Policy ID -> Policy details -> Policy RAG
# --------------------------------------------------

def hybrid_node(state: ClaimWiseState) -> dict:
    claim_id = state.get("claim_id")

    if not claim_id:
        return {
            "answer": (
                "A hybrid claim lookup requires a valid claim ID."
            )
        }

    # Step 1: Fetch the claim record.
    claim = claim_details_tool(claim_id)

    if not isinstance(claim, dict):
        return {
            "sql_result": claim,
            "answer": (
                "The claim record could not be read as structured "
                "data. Policy-specific analysis could not continue."
            ),
        }

    # Step 2: Find the policy linked to this claim.
    policy_id = claim.get("policy_id")

    if not policy_id:
        return {
            "sql_result": claim,
            "answer": (
                f"Claim record:\n{claim}\n\n"
                "The associated policy ID is unavailable. "
                "Policy-specific evidence could not be retrieved."
            ),
        }

    # Step 3: Fetch the associated policy details.
    policy = policy_details_tool(policy_id)

    if not isinstance(policy, dict):
        return {
            "sql_result": {
                "claim": claim,
                "policy": policy,
            },
            "answer": (
                f"Claim record:\n{claim}\n\n"
                f"Policy lookup result:\n{policy}\n\n"
                "The policy details could not be interpreted as "
                "structured data, so policy-specific retrieval "
                "could not be reliably filtered."
            ),
        }

    # Step 4: Resolve the actual policy name.
    # These fields match the existing policy dataset.
    policy_name = (
        policy.get("product_name")
        or policy.get("policy_type")
    )

    if not policy_name:
        return {
            "sql_result": {
                "claim": claim,
                "policy": policy,
            },
            "answer": (
                f"Claim record:\n{claim}\n\n"
                f"Policy record:\n{policy}\n\n"
                "The policy name could not be identified. "
                "Policy-specific RAG retrieval was not performed "
                "because it could return unrelated evidence."
            ),
        }

    # Step 5: Include the exact policy name in the question.
    original_question = state["question"]

    rag_question = (
        f"Policy: {policy_name}\n"
        f"Question: {original_question}"
    )

    # The existing RAG pipeline detects the policy name
    # and filters ChromaDB to that policy.
    rag_result = answer_policy_question(
        rag_question,
        top_k=5,
    )

    # Step 6: Combine the structured and unstructured results.
    answer = (
        f"CLAIM RECORD:\n{claim}\n\n"
        f"ASSOCIATED POLICY RECORD:\n{policy}\n\n"
        f"POLICY EVIDENCE:\n{rag_result['answer']}\n\n"
        "Important: This information supports a policy review. "
        "It does not determine or guarantee claim approval."
    )

    return {
        "sql_result": {
            "claim": claim,
            "policy": policy,
        },
        "rag_result": rag_result,
        "answer": answer,
    }


# --------------------------------------------------
# 7. Construct the LangGraph workflow
# --------------------------------------------------

builder = StateGraph(ClaimWiseState)

builder.add_node("router", route_question)
builder.add_node("sql", sql_node)
builder.add_node("rag", rag_node)
builder.add_node("hybrid", hybrid_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    lambda state: state["route"],
    {
        "sql": "sql",
        "rag": "rag",
        "hybrid": "hybrid",
    },
)

builder.add_edge("sql", END)
builder.add_edge("rag", END)
builder.add_edge("hybrid", END)

claimwise_graph = builder.compile()


# --------------------------------------------------
# 8. Public function for the API and UI
# --------------------------------------------------

def ask_claimwise(question: str) -> dict:
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    result = claimwise_graph.invoke({
        "question": question.strip()
    })

    return {
        "question": result["question"],
        "route": result["route"],
        "answer": result["answer"],
        "sources": (
            result.get("rag_result", {}).get("sources", [])
        ),
        "sql_result": result.get("sql_result"),
    }


# --------------------------------------------------
# 9. Run the assistant from the terminal
# --------------------------------------------------

if __name__ == "__main__":
    print("ClaimWise LangGraph Assistant")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nAsk ClaimWise: ").strip()

        if question.casefold() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        try:
            result = ask_claimwise(question)

            print(f"\nSelected route: {result['route']}")
            print(f"\nClaimWise Answer:\n{result['answer']}")

            if result["sources"]:
                print("\nRetrieved Sources:")

                for source in result["sources"]:
                    print(
                        f"- {source['policy_name']} | "
                        f"Section {source['section_number']}: "
                        f"{source['section']} | "
                        f"{source['source']}"
                    )

        except Exception as error:
            print(f"\nAn error occurred: {error}")
