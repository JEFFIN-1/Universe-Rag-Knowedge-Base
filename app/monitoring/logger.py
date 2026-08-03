from app.monitoring.database import get_connection


def log_conversation(
    question: str,
    answer: str,
    response_time: float,
    retrieved_chunks: int,
    model: str = "llama",
):
    print("📊 Logging conversation...")

    conn = get_connection()

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO conversations (
                question,
                answer,
                model,
                response_time,
                retrieved_chunks
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                question,
                answer,
                model,
                response_time,
                retrieved_chunks,
            ),
        )

    conn.commit()
    conn.close()

    print("✅ Conversation logged.")