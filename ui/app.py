
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="ClaimWise | Insurance Intelligence",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ ClaimWise")
st.subheader("Insurance Claims & Policy Intelligence Assistant")
st.caption(
    "Ask questions about insurance policies, claim records, "
    "waiting periods, exclusions, and required documents."
)

st.divider()

with st.sidebar:
    st.header("About ClaimWise")
    st.write(
        "ClaimWise combines structured claim data with "
        "retrieval-augmented generation (RAG) to provide "
        "evidence-based insurance information."
    )

    st.info(
        "Answers are informational. They do not guarantee "
        "claim approval or settlement."
    )

    st.markdown("**Available workflows**")
    st.write("🗃️ SQL — Claim and customer records")
    st.write("📚 RAG — Policy information")
    st.write("🔀 Hybrid — Claim records plus policy evidence")

st.markdown("### Ask a question")

examples = [
    "What is the maternity waiting period under Health Secure Plus?",
    "What is the status of claim CLM300001?",
    "For claim CLM300001, what policy coverage and exclusions should be checked?",
]

selected_example = st.selectbox(
    "Choose an example or write your own question below",
    ["Choose an example..."] + examples,
)

default_question = (
    selected_example if selected_example in examples else ""
)

with st.form("claimwise_question_form"):
    question = st.text_area(
        "Your question",
        value=default_question,
        placeholder="Example: What is the status of claim CLM300001?",
        height=110,
    )

    submitted = st.form_submit_button(
        "Ask ClaimWise",
        type="primary",
        use_container_width=True,
    )

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")

    else:
        try:
            with st.spinner("Analyzing your question..."):
                response = requests.post(
                    API_URL,
                    json={"question": question.strip()},
                    timeout=120,
                )

            if response.ok:
                result = response.json()

                st.divider()
                st.markdown("### ClaimWise Answer")

                route = result.get("route", "unknown").upper()
                st.markdown(f"**Workflow:** `{route}`")
                st.markdown(result.get("answer", "No answer returned."))

                sources = result.get("sources", [])

                if sources:
                    with st.expander(
                        f"View retrieved policy sources ({len(sources)})"
                    ):
                        for source in sources:
                            st.markdown(
                                f"- **{source.get('policy_name', 'Unknown')}** "
                                f"— Section {source.get('section_number', '?')}: "
                                f"{source.get('section', 'Unknown')} "
                                f"(`{source.get('source', 'Unknown')}`)"
                            )

                elif route in {"RAG", "HYBRID"}:
                    st.info(
                        "No policy source metadata was returned "
                        "for this response."
                    )

            else:
                st.error(
                    f"API error ({response.status_code}): "
                    f"{response.text}"
                )

        except requests.RequestException as error:
            st.error(
                "Could not connect to the ClaimWise API. "
                "Make sure FastAPI is running at "
                "http://127.0.0.1:8000."
            )
            st.caption(str(error))

st.divider()
st.caption("ClaimWise · GenAI-Powered Insurance Policy Intelligence")
