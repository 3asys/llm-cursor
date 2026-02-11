"""Core application logic for the llm-cursor MVP.

Итерация 2: простой многошаговый диалог в одном процессе,
хранение истории в памяти и служебная команда `/history`.
"""

from __future__ import annotations

import logging
from typing import TypedDict, Literal


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


Role = Literal["system", "user", "assistant"]


class Message(TypedDict):
    role: Role
    content: str


History = list[Message]


def run_once(user_input: str) -> str:
    """Handle a single user input and return a fixed response.

    Оставлено для совместимости с тестами и простой проверки.
    Под капотом использует общую логику обработки одного шага.
    """
    logger.info("Handling single request: %s", user_input)
    history: History = []
    history, reply = handle_turn(history, user_input)
    return reply


def _format_history(history: History) -> str:
    """Return a simple text representation of the dialog history."""
    if not history:
        return "История пуста."

    lines: list[str] = []
    for msg in history:
        if msg["role"] == "user":
            prefix = "user"
        elif msg["role"] == "assistant":
            prefix = "assistant"
        else:
            prefix = msg["role"]

        lines.append(f"{prefix}: {msg['content']}")
    return "\n".join(lines)


def handle_turn(history: History, user_input: str) -> tuple[History, str]:
    """Обработать один шаг диалога.

    - При обычном тексте: добавить сообщения user/assistant и вернуть ответ.
    - При `/history`: вернуть текст истории без добавления новых сообщений.
    """
    logger.info("Handling dialog turn: %s", user_input)

    text = user_input.strip()

    if text == "/history":
        return history, _format_history(history)

    # Обычный шаг диалога: эхо-ответ с сохранением истории.
    new_history = list(history)
    new_history.append({"role": "user", "content": text})

    reply = f"Эхо: {text}" if text else "Пустой запрос."

    new_history.append({"role": "assistant", "content": reply})
    return new_history, reply

