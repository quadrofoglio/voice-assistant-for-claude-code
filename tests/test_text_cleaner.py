from src.text_cleaner import clean_for_tts

def test_strips_fenced_code_block():
    text = "Here is the code:\n```python\ndef foo():\n    pass\n```\nThat's it."
    result = clean_for_tts(text)
    assert "def foo" not in result
    assert "Here is the code" in result
    assert "That's it" in result

def test_strips_inline_code():
    text = "Call the `foo()` function to start."
    result = clean_for_tts(text)
    assert "`" not in result
    assert "foo" not in result
    assert "Call the" in result

def test_strips_markdown_headers():
    text = "## Summary\nThis is a summary."
    result = clean_for_tts(text)
    assert "##" not in result
    assert "Summary" in result

def test_strips_urls():
    text = "See https://example.com for details."
    result = clean_for_tts(text)
    assert "https://" not in result

def test_collapses_excess_newlines():
    text = "Hello\n\n\n\nWorld"
    result = clean_for_tts(text)
    assert "\n\n\n" not in result

def test_empty_string():
    assert clean_for_tts("") == ""

def test_plain_prose_unchanged():
    text = "The function handles user authentication by validating tokens."
    assert "handles user authentication" in clean_for_tts(text)
