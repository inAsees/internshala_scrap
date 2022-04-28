from test_scrapper import ScrapInternshala, get_available_keywords


class CliHandler:
    def __init__(self):
        pass

    @staticmethod
    def run():
        print("<<<<Welcome Message>>>>")  # To Do.
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
            print("Invalid input")
            quit()
        keyword_search = available_keywords[int(user_input)]
        scrapper = ScrapInternshala(keyword_search).scrap_all_pages()
