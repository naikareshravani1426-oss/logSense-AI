import re

def parse_log(raw: str) -> str:
    text = raw

    # Remove timestamps
    text = re.sub(r'\[?\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}\]?', '', text)

    # Remove IP addresses
    text = re.sub(r'\b\d{1,3}(\.\d{1,3}){3}\b', '', text)

    # Remove log levels (case-insensitive)
    text = re.sub(r'\b(INFO|DEBUG|WARN|ERROR|CRITICAL|FATAL)\b', '', text, flags=re.IGNORECASE)

    # Remove brackets
    text = re.sub(r'[\[\]]', '', text)

    # Normalize spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Lowercase (important for ML)
    text = text.lower()

    return text