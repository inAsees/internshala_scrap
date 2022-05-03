from src.cli_handler import CliHandler
import logging
from pathlib import Path

logging.basicConfig(filename=Path('scrap_logger.log'), encoding='utf-8', level=logging.INFO, filemode="w",
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    CliHandler().run()


if __name__ == "__main__":
    main()
