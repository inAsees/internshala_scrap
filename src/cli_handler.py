from src.scrapper import ScrapInternshala, AttemptsHandling, get_available_keywords, is_file_path_exists, \
    is_file_parent_exists


class CliHandler:
    def __init__(self):
        self._attempt_handling = AttemptsHandling()

    def run(self):
        print("<<<<Welcome Message>>>>\n"
              "This program will help you to scrap data from www.internshala.com website and write it into CSV file in "
              "your local system.\n")
        print("Pick one job title from the available list using index number adjacent to it.\n")
        available_keywords = get_available_keywords()
        print("INDEX  JOB TITLE")
        for i in range(len(available_keywords)):
            print("{0}--->  {1}".format(i, available_keywords[i]))

        user_input = input("\nEnter the index number:")
        flag = False
        for idx in range(len(available_keywords)):
            if user_input == str(idx):
                flag = True
                break
        if not flag:
            print("Invalid input.\n"
                  "Run the program again.")
            quit()
        keyword_search = available_keywords[int(user_input)]
        scrapper = ScrapInternshala(keyword_search)
        scrapper.scrap_all_pages()
        print("Scrapping successfully completed.\n")
        print("Please provide a valid file path to save the data.\n"
              "If you have already saved data and trying to save new data it is highly recommended to provide different"
              " file name.\n")

        while self._attempt_handling.is_cur_attempt_less_than_max_attempt():
            if self._attempt_handling.is_cur_attempt_equals_last_attempt():
                print("Too many wrong attempts.\n"
                      "Program stopped.")
                quit()
            file_path = input("Enter the path:  ")
            if is_file_path_exists(file_path):
                print("This file already exists!!!.")
                user_choice = input("Do you want to overwrite this file (Y/N): ").lower()
                if user_choice == "y":
                    print("Ready to overwrite the file.")
                    scrapper.dump(file_path)
                    quit()
                elif user_choice == "n":
                    print("Provide different file name with complete path again.")
                    self._attempt_handling.increment_cur_attempt()
                    continue
                else:
                    print("Invalid input.")
                    self._attempt_handling.increment_cur_attempt()
                    continue
            elif is_file_path_exists(file_path) is None:
                print("Invalid file suffix!!\n"
                      "File suffix should be '.csv'")
                self._attempt_handling.increment_cur_attempt()
                continue
            if is_file_parent_exists(file_path):
                scrapper.dump(file_path)
                quit()
            elif is_file_parent_exists(file_path) is None:
                print("Invalid file suffix!!\n"
                      "File suffix should be '.csv'")
                self._attempt_handling.increment_cur_attempt()
                continue

            print("Invalid path!!")
            self._attempt_handling.increment_cur_attempt()
