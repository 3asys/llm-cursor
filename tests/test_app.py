from llm_cursor.app import History, handle_turn, run_once


def test_run_once_uses_handle_turn_and_returns_echo():
    reply = run_once("тестовый ввод")
    assert isinstance(reply, str)
    assert reply.startswith("Эхо:")


def test_handle_turn_adds_user_and_assistant_messages():
    history: History = []

    history, reply = handle_turn(history, "привет")

    assert reply.startswith("Эхо:")
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "привет"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == reply


def test_handle_turn_history_command_returns_formatted_history():
    history: History = []

    # сначала добавим один обычный шаг
    history, _ = handle_turn(history, "привет")

    # затем запросим историю
    history_after, reply = handle_turn(history, "/history")

    assert history_after is history  # история не должна меняться
    assert "user: привет" in reply
    assert "assistant: Эхо: привет" in reply

