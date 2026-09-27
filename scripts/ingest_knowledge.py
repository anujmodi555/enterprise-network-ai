import logging

from enterprise_network_ai.rag import (
    ingest_all_documents,
)


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(name)s: %(message)s",
)


def main() -> None:

    total_chunks = (
        ingest_all_documents()
    )

    print(
        f"\nSuccessfully ingested "
        f"{total_chunks} knowledge chunks."
    )


if __name__ == "__main__":
    main()