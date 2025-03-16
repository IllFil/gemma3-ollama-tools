from llm_set_up.llm_core import run_chat
from utils.set_logging import setup_logging


def main():
    setup_logging()
    run_chat()


if __name__ == "__main__":
    main()