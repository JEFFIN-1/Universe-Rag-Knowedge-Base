from app.chat.service import ask

question = "What is Retrieval-Augmented Generation?"

response = ask(question)

print("\n===== ANSWER =====\n")
print(response["answer"])

print("\n===== SOURCES =====\n")

for doc in response["documents"]:
    source = doc["_source"]

    print(source["source"])
    print("-" * 50)