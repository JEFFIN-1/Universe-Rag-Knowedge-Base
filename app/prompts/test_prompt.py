from app.retrieval.hybrid import hybrid_search
from app.prompts.prompt_builder import build_prompt

query = "What is the Big Bang theory?"

docs = hybrid_search(query)

prompt = build_prompt(query, docs)

print(prompt)

from pprint import pprint

docs = hybrid_search(query)

pprint(docs[0])