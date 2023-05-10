import csv
import json
import time
import requests
from pathlib import Path


class LeetcodeCrawler:

    def __init__(self):
        self.problem_url = "https://leetcode.com/api/problems/all/"
        self.contest_url = "https://leetcode.com/contest/api/info/"
        self.level = {1: "Easy", 2: "Medium", 3: "Hard"}
        self.question_header = ["Id", "Title", "Difficulty", "Total_Accept", "Total_Submit", "Acceptance", "Preimum"]
        self.contest_header = ["Contest", "Id", "Title"]
        self.id_mapping = {}
        self.all_questions = []

    def get_all_questions(self):
        return self.all_questions
    def update_questions(self):
        res = requests.get(self.problem_url)
        data = json.loads(res.content)
        stat_status_pair = data["stat_status_pairs"]
        question = [{} for _ in range(len(stat_status_pair))]
        for q in stat_status_pair:
            self.id_mapping[q["stat"]["question_id"]] = q["stat"]["frontend_question_id"]
            question[q["stat"]["frontend_question_id"] - 1]["Id"] = q["stat"]["frontend_question_id"]
            question[q["stat"]["frontend_question_id"] - 1]["Title"] = q["stat"]["question__title"]
            question[q["stat"]["frontend_question_id"] - 1]["Difficulty"] = self.level[q["difficulty"]["level"]]
            question[q["stat"]["frontend_question_id"] - 1]["Total_Accept"] = q["stat"]["total_acs"]
            question[q["stat"]["frontend_question_id"] - 1]["Total_Submit"] = q["stat"]["total_submitted"]
            question[q["stat"]["frontend_question_id"] - 1]["Acceptance"] = q["stat"]["total_acs"] / q["stat"][
                "total_submitted"]
            question[q["stat"]["frontend_question_id"] - 1]["Preimum"] = q["paid_only"]
        self.all_questions = question

    def write_all_questions_to_csv(self, path="questions.csv"):
        data = self.get_all_questions()
        path = Path(path)
        print("Output path:", path.absolute())
        with open(path, "w", newline="") as output:
            writer = csv.writer(output)
            writer.writerow(self.question_header)
            for line in data:
                writer.writerow([line[val] for val in self.question_header])
        print("Write File Successfully")

    def get_contest_question(self, contest):
        res = requests.get(self.contest_url + contest + "/")
        data = json.loads(res.content)
        res = []
        if "error" in data:
            print("Cannot find contest:", contest)
        else:
            questions = data["questions"]
            for record in questions:
                id = record["question_id"]
                title = record["title"]
                if id not in self.id_mapping:
                    self.update_questions()
                res.append([contest, self.id_mapping[id], title])
        return res

    def write_all_contest_to_csv(self, path="contest.csv"):
        path = Path(path)
        res = []
        existing_contest = set()
        if path.exists():
            with open(path, "r") as fin:
                reader = csv.reader(fin)
                header = next(reader)
                print(header)
                for line in reader:
                    res.append(line)
                    existing_contest.add(line[0])
        print("The number of existing contest:", len(existing_contest))

        weekly = "weekly-contest-"
        biweekly = "biweekly-contest-"
        count = 0
        for i in range(55, 350):
            contest = weekly + str(i)
            if contest in existing_contest:
                continue
            count += 1
            res.extend(self.get_contest_question(weekly + str(i)))
            if count % 10 == 0:
                time.sleep(1)
        for i in range(1, 105):
            contest = biweekly + str(i)
            if contest in existing_contest:
                continue
            count += 1
            res.extend(self.get_contest_question(biweekly + str(i)))
            if count % 10 == 0:
                time.sleep(1)
        res.sort(key =lambda x:int(x[1]))

        with open(path, "w", newline="") as output:
            writer = csv.writer(output)
            writer.writerow(self.contest_header)
            for line in res:
                writer.writerow(line)
        print("Write File Successfully")

