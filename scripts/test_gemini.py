from enterprise_network_ai.llm import ask_llm


question = "What does high CPU utilization on a network router generally indicate?"

context = """
Device: R1
CPU utilization: 91%
Memory utilization: 62%
Alert: CPU utilization is above 85%.
"""

answer = ask_llm(
    question=question,
    network_context=context,
)

print("\nLLM RESPONSE:\n")
print(answer)