from enterprise_network_ai.rag import (
    retrieve_knowledge,
)


QUESTIONS = [
    "How should I troubleshoot BGP flapping?",
    "What should I check for high CPU?",
    "What can cause interface errors?",
]


def main() -> None:

    for question in QUESTIONS:

        print("\n" + "=" * 70)

        print("QUESTION:")
        print(question)

        results = retrieve_knowledge(
            question=question,
            top_k=3,
        )

        print("\nRESULTS:")

        for result in results:

            print(
                f"\nDocument: "
                f"{result['document_name']}"
            )

            print(
                f"Similarity: "
                f"{result['similarity']:.4f}"
            )

            print(
                f"Content:\n"
                f"{result['content'][:500]}"
            )


if __name__ == "__main__":
    main()