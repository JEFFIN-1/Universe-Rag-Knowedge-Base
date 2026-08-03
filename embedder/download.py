from huggingface_hub import snapshot_download


def download_model():
    snapshot_download(
        repo_id="Xenova/all-MiniLM-L6-v2",
        local_dir="models/Xenova/all-MiniLM-L6-v2",
        local_dir_use_symlinks=False,
    )


if __name__ == "__main__":
    download_model()