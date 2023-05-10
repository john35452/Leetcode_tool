import csv
import json
import requests
from pathlib import Path


class LeetcodeCrawler:

    def __init__(self):
        self.url = "https://leetcode.com/api/problems/all/"
        self.level = {1: "Easy", 2: "Medium", 3: "Hard"}
        self.header = ["Id", "Title", "Difficulty", "Total_Accept", "Total_Submit", "Acceptance", "Preimum"]

    def get_questions(self):
        res = requests.get(self.url)
        data = json.loads(res.content)
        stat_status_pair = data["stat_status_pairs"]
        question = [{} for _ in range(len(stat_status_pair))]
        for q in stat_status_pair:
            question[q["stat"]["frontend_question_id"] - 1]["Id"] = q["stat"]["frontend_question_id"]
            question[q["stat"]["frontend_question_id"] - 1]["Title"] = q["stat"]["question__title"]
            question[q["stat"]["frontend_question_id"] - 1]["Difficulty"] = self.level[q["difficulty"]["level"]]
            question[q["stat"]["frontend_question_id"] - 1]["Total_Accept"] = q["stat"]["total_acs"]
            question[q["stat"]["frontend_question_id"] - 1]["Total_Submit"] = q["stat"]["total_submitted"]
            question[q["stat"]["frontend_question_id"] - 1]["Acceptance"] = q["stat"]["total_acs"] / q["stat"]["total_submitted"]
            question[q["stat"]["frontend_question_id"] - 1]["Preimum"] = q["paid_only"]
        return question

    def write_csv(self, path="."):
        data = self.get_questions()
        path = Path(path)
        print("Output path:", path.absolute())
        with open(path, "w", newline="") as output:
            writer = csv.writer(output)
            writer.writerow(self.header)
            for line in data:
                writer.writerow([line[val] for val in self.header])
        print("Write File Successfully")