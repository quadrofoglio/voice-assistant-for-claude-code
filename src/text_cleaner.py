import re

def clean_for_tts(text: str) -> str:
    if not text:
        return ""
    # Remove fenced code blocks
    text = re.sub(r'```[\s\S]*?```', '', text)
    # Remove inline code
    text = re.sub(r'`[^`\n]+`', '', text)
    # Remove markdown headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Remove bold/italic markers, keep text
    text = re.sub(r'\*{1,3}([^*\n]+)\*{1,3}', r'\1', text)
    # Collapse excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Collapse excessive spaces
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()
