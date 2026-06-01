from unittest.mock import patch, MagicMock
from src.input_delivery import InputDelivery

def test_clipboard_mode_copies_text():
    delivery = InputDelivery(mode="clipboard")
    with patch("src.input_delivery.pyperclip") as mock_clip:
        delivery.deliver("hello world")
        mock_clip.copy.assert_called_once_with("hello world")

def test_terminal_mode_types_text():
    delivery = InputDelivery(mode="terminal")
    with patch("src.input_delivery.Controller") as MockController:
        mock_kb = MagicMock()
        MockController.return_value = mock_kb
        delivery = InputDelivery(mode="terminal")
        delivery.deliver("hello")
        mock_kb.type.assert_called_once_with("hello")

def test_mode_can_be_changed():
    delivery = InputDelivery(mode="terminal")
    delivery.set_mode("clipboard")
    assert delivery.mode == "clipboard"

def test_invalid_mode_raises():
    delivery = InputDelivery(mode="terminal")
    try:
        delivery.set_mode("invalid")
        assert False, "should have raised"
    except ValueError:
        pass
