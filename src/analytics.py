import pandas as pd
from ast import literal_eval


class Analytics:
    def __init__(self, file_path=r"C:\Users\DELL\Desktop\scrap_for_computer_science.csv"):
        self._file_path = file_path
        self._max_counter = 10

    def get_top_skills(self):
        counter = 0
        dic = {}
        df = pd.read_csv(self._file_path)
        for i in df["skill_set"].values:
            for j in literal_eval(i):
                if j == "":
                    continue
                dic[j] = dic.get(j, 0) + 1
        sorted_dic = sorted(dic, key=dic.get, reverse=True)
        print("Top 10 skills are listed below\n")
        for key in sorted_dic:
            if counter == self._max_counter:
                break
            print(key, dic[key])
            counter += 1


if __name__ == "__main__":
    analytics = Analytics()
    analytics.get_top_skills()
