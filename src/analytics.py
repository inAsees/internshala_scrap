from typing import Dict, List
import pandas as pd
from ast import literal_eval


class Analytics:
    def __init__(self, file_path=r"C:\Users\DELL\Desktop\scrap_for_python\only_python_scrap.csv"):
        self._file_path = file_path
        self._max_counter = 10
        self._df = pd.read_csv(self._file_path)
        self._dic = {}

    def search_top_skills(self) -> None:
        for i in self._df["skill_set"].values:
            for j in literal_eval(i):
                if j == "":
                    continue
                self._dic[j] = self._dic.get(j, 0) + 1
        sorted_dic = sorted(self._dic, key=self._dic.get, reverse=True)
        print("* Top 10 skills are listed below\n")
        self._print_top_results(self._dic, sorted_dic)

    def search_top_locations(self) -> None:
        for i in self._df["location"].values:
            self._dic[i] = self._dic.get(i, 0) + 1
        sorted_dic = sorted(self._dic, key=self._dic.get, reverse=True)
        print("\n* Top 10 locations are listed below\n")
        self._print_top_results(self._dic, sorted_dic)

    def search_top_skills_acc_to_highest_stipend(self) -> None:
        sorted_df = self._df.sort_values("monthly_lump_sum", ascending=False)
        for i in sorted_df["skill_set"].values:
            for j in literal_eval(i):
                if j == "":
                    continue
                self._dic[j] = self._dic.get(j, 0) + 1
        sorted_dic = sorted(self._dic, key=self._dic.get, reverse=True)
        print("\n* Top 10 skills according to highest stipend are listed below\n")
        self._print_top_results(self._dic, sorted_dic)

    def _print_top_results(self, dic: Dict, sorted_dic: List) -> None:
        counter = 0
        for i, key in enumerate(sorted_dic):
            if counter == self._max_counter:
                break
            print(i + 1, key, "-->", dic[key])
            counter += 1
        self._dic = {}


if __name__ == "__main__":
    analytics = Analytics()
    analytics.search_top_skills()
    analytics.search_top_locations()
    analytics.search_top_skills_acc_to_highest_stipend()
