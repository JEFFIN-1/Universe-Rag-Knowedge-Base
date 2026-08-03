from pathlib import Path

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer


class Embedder:

    def __init__(self, model_path="models/Xenova/all-MiniLM-L6-v2"):

        model_path = Path(model_path)

        if not model_path.is_absolute():
            project_root = Path(__file__).resolve().parent.parent
            model_path = project_root / model_path

        model_path = model_path.resolve()

        print(f"Using model path: {model_path}")

        self.tokenizer = Tokenizer.from_file(
            str(model_path / "tokenizer.json")
        )

        self.session = ort.InferenceSession(
            str(model_path / "onnx" / "model_quantized.onnx"),
            providers=["CPUExecutionProvider"],
        )

        self.input_names = {
            inp.name
            for inp in self.session.get_inputs()
        }

    def encode(self, text, normalize=True):
        return self.encode_batch(
            [text],
            normalize=normalize,
        )[0]

    def encode_batch(self, texts, normalize=True):

        self.tokenizer.enable_padding()

        encoded = self.tokenizer.encode_batch(texts)

        feed = {}

        if "input_ids" in self.input_names:
            feed["input_ids"] = np.array(
                [e.ids for e in encoded],
                dtype=np.int64,
            )

        if "attention_mask" in self.input_names:
            feed["attention_mask"] = np.array(
                [e.attention_mask for e in encoded],
                dtype=np.int64,
            )

        if "token_type_ids" in self.input_names:
            feed["token_type_ids"] = np.array(
                [e.type_ids for e in encoded],
                dtype=np.int64,
            )

        hidden = self.session.run(None, feed)[0]

        mask = feed["attention_mask"][..., None]

        pooled = (hidden * mask).sum(axis=1) / mask.sum(axis=1)

        if normalize:
            pooled = pooled / np.linalg.norm(
                pooled,
                axis=1,
                keepdims=True,
            )

        return pooled