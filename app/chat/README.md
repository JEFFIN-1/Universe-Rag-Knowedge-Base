# Chat orchestration

`service.py` coordinates one chat request: it retrieves relevant chunks with hybrid search, builds a context-only prompt, generates an answer, measures elapsed time, and sends the result to the monitoring logger.
