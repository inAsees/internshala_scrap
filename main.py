from src.cli_handler import CliHandler
import logging
from pathlib import Path

logging.basicConfig(filename=Path('scrap_logger.log'), encoding='utf-8',
                    level=logging.INFO)


def main():
    CliHandler().run()


if __name__ == "__main__":
    main()
