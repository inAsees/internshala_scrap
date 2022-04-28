from tests.scrapper import ScrapInternshala, get_available_keywords, is_file_path_exists


class CliHandler:
    def __init__(self):
        pass

    @staticmethod
    def run():
        print("<<<<Welcome Message>>>>\n"
              "This program will help you to scrap data from www.internshala.com website and write it into CSV file in "
              "your local system.")
        print("Pick one job title from the available list using index number adjacent to it.")
        available_keywords = get_available_keywords()
        print("Index  Job title")
        for i in range(len(available_keywords)):
            print("{0}--->  {1}".format(i, available_keywords[i]))

        user_input = input("Enter the index number:")
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
        print("Scrapping successfully completed.")
        print("Please provide a valid file path to save the data.\n"
              "If you have already saved data and trying to save new data it is highly recommended to provide different"
              " file name.\n")
        file_path = input("Enter the path:  ")
        if is_file_path_exists(file_path):
            print("This file already exists,please provide different file name.")
            user_choice = input("Do you want to overwrite this file (Y/N): ").lower()
            if user_choice == "y":
                pass
            else:
                pass
        elif is_file_path_exists(file_path) is None:
            print("Invalid file suffix!!")
        else:
            print("Ready to write the file.")
