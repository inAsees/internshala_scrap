from typing import Dict, List
import pandas as pd
from ast import literal_eval


class Analytics:
    def __init__(self, file_path=r"C:\Users\DELL\Desktop\scrap_for_python\only_python_scrap.csv"):
        self._file_path = file_path
        self._max_counter = 10

    def get_top_skills(self):
        dic = {}
        df = pd.read_csv(self._file_path)
        for i in df["skill_set"].values:
            for j in literal_eval(i):
                if j == "":
                    continue
                dic[j] = dic.get(j, 0) + 1
        sorted_dic = sorted(dic, key=dic.get, reverse=True)
        print("* Top 10 skills are listed below\n")
        self._print(dic, sorted_dic)

    def get_top_locations(self):
        df = pd.read_csv(self._file_path)
        dic = {}
        for i in df["location"].values:
            dic[i] = dic.get(i, 0) + 1
        sorted_dic = sorted(dic, key=dic.get, reverse=True)
        print("\n* Top 10 locations are listed below\n")
        self._print(dic, sorted_dic)

    def _print(self, dic: Dict, sorted_dic: List):
        counter = 0
        for i, key in enumerate(sorted_dic):
            if counter == self._max_counter:
                break
            print(i + 1, key, "-->", dic[key])
            counter += 1


if __name__ == "__main__":
    analytics = Analytics()
    analytics.get_top_skills()
    analytics.get_top_locations()
