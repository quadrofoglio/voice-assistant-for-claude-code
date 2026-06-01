import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hook.stop_hook import extract_last_assistant_text

def test_extracts_string_content():
    transcript = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "world"},
    ]
    assert extract_last_assistant_text(transcript) == "world"

def test_extracts_text_from_content_list():
    transcript = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": [
            {"type": "text", "text": "part one"},
            {"type": "tool_use", "name": "Read"},
            {"type": "text", "text": "part two"},
        ]},
    ]
    result = extract_last_assistant_text(transcript)
    assert "part one" in result
    assert "part two" in result

def test_skips_tool_use_blocks():
    transcript = [
        {"role": "assistant", "content": [
            {"type": "tool_use", "name": "Bash", "input": {}},
            {"type": "text", "text": "done"},
        ]},
    ]
    assert extract_last_assistant_text(transcript) == "done"

def test_returns_empty_for_no_assistant_message():
    assert extract_last_assistant_text([{"role": "user", "content": "hi"}]) == ""

def test_returns_empty_for_empty_transcript():
    assert extract_last_assistant_text([]) == ""
