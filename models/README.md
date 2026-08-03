# Local models

This directory contains model artifacts used at runtime rather than application source code. The current embedder expects the ONNX model and tokenizer for `Xenova/all-MiniLM-L6-v2` under `Xenova/all-MiniLM-L6-v2/`.

Use `python -m embedder.download` to download that model when it is absent. Do not add README files inside model cache directories; their structure is controlled by the model downloader.
