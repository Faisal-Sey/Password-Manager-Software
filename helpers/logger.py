import os
from datetime import datetime
from typing import Dict


def logger(category: str, status: str, message: str) -> None:
    message_symbols: Dict[str, str] = {
        "error": "\U0001F534",  # for errors
        "success": "\U0001F7E2",  # for success
    }

    file_path: str = os.path.join("logs", f"{category}.txt")

    message_symbol: str = message_symbols[status]

    message: str = f"{message_symbol} {str(datetime.now())}: {message}"

    with open(file_path, "a", encoding="utf-8") as file:
        file.write(f"{message}\n")
