import sys
from pathlib import Path
from typing import Optional
from src.scrapper import ScrapInternshala, AttemptsHandler
from src.utils import Utils


class CliHandler:
    def _init_(self):
        self._attempt_handler = AttemptsHandler(5)

    def run(self):
        print("<<<<Welcome Message>>>>\n"
              "This program will help you to scrap data from www.internshala.com website and write it into CSV file in "
              "your local system.\n")
        print("Pick one job title from the available list using index number adjacent to it.\n")
        available_keywords = Utils.get_available_keywords()
        print("INDEX  JOB TITLE")
        for i, keyword in enumerate(available_keywords):
            print(i, "--->", keyword)

        user_input = input("\nEnter the index number:")
        user_input_int = self._get_idx_from_user_input(user_input)
        if user_input_int is None:
            print("Invalid input.")
            sys.exit()
        if not self._is_user_idx_in_range(user_input_int, len(available_keywords)):
            print("Invalid input")
            sys.exit()

        keyword_search = available_keywords[int(user_input)]
        scrapper = ScrapInternshala(keyword_search)
        scrapper.scrap_all_pages()
        print("Scrapping successfully completed.\n")
        print("Please provide a valid file path to save the data.\n"
              "If you have already saved data and trying to save new data it is highly recommended to provide different"
              " file name.\n")

        while self._attempt_handler.is_attempts_left():
            file_path = Path(input("Enter the path:  "))
            if not Utils.is_file_extension_supported(file_path):
                print("Invalid file suffix!!\n"
                      "File suffix should be '.csv'")
                self._attempt_handler.increment_cur_attempt()
                continue
            else:
                if Utils.is_file_path_exists(file_path):
                    is_override = self._prompt_user_for_overriding()
                    if not is_override:
                        print("Provide different file name with complete path again.")
                        self._attempt_handler.increment_cur_attempt()
                        continue
                    elif is_override is None:
                        print("Invalid input.")
                        continue
                if not Utils.is_parent_path_exists(file_path):
                    print("Invalid path!!")
                    self._attempt_handler.increment_cur_attempt()
                    continue
                scrapper.dump(str(file_path))
        print("Too many wrong attempts\n"
              "Program stopped.")
        sys.exit()

    @staticmethod
    def _prompt_user_for_overriding() -> Optional[bool]:
        user_input = input("(y/n):  ").lower()
        if user_input == "y":
            return True
        elif user_input == "n":
            return False
        return None

    @staticmethod
    def _get_idx_from_user_input(user_input: str) -> Optional[int]:
        try:
            return int(user_input)
        except ValueError:
            return None

    @staticmethod
    def _is_user_idx_in_range(user_input_int: int, max_len: int) -> bool:
        if user_input_int is None or user_input_int < 0 or user_input_int > max_len:
            return False
        return True
