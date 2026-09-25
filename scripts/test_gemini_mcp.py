import asyncio
import logging

from enterprise_network_ai.gemini_mcp import (
    ask_network_assistant,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)

QUESTIONS = ["What is the BGP status of R1?"]
# QUESTIONS = [
#     "What is the current status of R1?",
#     "Are there any active alerts on R1?",
#     "What is the BGP status of R1?",
#     (
#         "Check GigabitEthernet0/0 on R1 "
#         "and tell me whether it shows any issues."
#     ),
#     (
#         "Investigate R1 and give me a network health "
#         "summary using the available diagnostic tools."
#     ),
# ]


async def main() -> None:

    for question in QUESTIONS:

        print("\n" + "=" * 70)

        print("QUESTION:")
        print(question)

        answer = await ask_network_assistant(
            question=question,
        )

        print("\nANSWER:")
        print(answer)


if __name__ == "__main__":
    asyncio.run(main())