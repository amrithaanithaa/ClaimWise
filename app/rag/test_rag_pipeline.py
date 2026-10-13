
from app.rag.rag_pipeline import answer_policy_question


while True:
    question = input("\nAsk ClaimWise (or type 'exit'): ").strip()

    if question.lower() == "exit":
        break

    try:
        result = answer_policy_question(question)

        print("\nClaimWise Answer:")
        print(result["answer"])

        print("\nRetrieved Sources:")
        for source in result["sources"]:
            print(
                f"- {source['policy_name']} | "
                f"Section {source['section_number']}: "
                f"{source['section']} | "
                f"{source['source']}"
            )

    except Exception as error:
        print(f"Error: {error}")
