"""CLI entry point for the llm-cursor MVP."""

from __future__ import annotations

import logging
import sys

from .app import History, handle_turn, run_once


logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    # На Iteration 2 аргументы CLI по-прежнему игнорируются.
    print("LLM Cursor CLI. Введите текст, /history для истории или /exit для выхода.")

    history: History = []

    while True:
        try:
            user_input = input("> ")
        except EOFError:
            # Ввод закончился — выходим.
            print("\nВыход.")
            break

        text = user_input.strip()
        if text in {"/exit", "/quit"}:
            print("Завершение диалога.")
            break

        try:
            history, reply = handle_turn(history, user_input)
        except Exception:  # noqa: BLE001 - достаточно общей обработки на MVP
            logger.exception("Unexpected error in CLI loop")
            print("Произошла ошибка, попробуйте ещё раз или завершите диалог командой /exit.")
            continue

        print(reply)

    return 0


if __name__ == "__main__":  # pragma: no cover - direct CLI execution
    raise SystemExit(main())

