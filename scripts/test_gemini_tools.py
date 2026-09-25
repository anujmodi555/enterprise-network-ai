import logging

from enterprise_network_ai.llm import ask_network_assistant


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)


questions = ["restart_device",
]


for question in questions:

    print("\n" + "=" * 70)
    print("QUESTION:")
    print(question)

    answer = ask_network_assistant(
        question=question
    )

    print("\nANSWER:")
    print(answer)