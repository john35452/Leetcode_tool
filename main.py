from Crawler import LeetcodeCrawler

if __name__ == '__main__':
    crawler = LeetcodeCrawler()
    crawler.update_questions()
    questions = crawler.get_all_questions()
    print("Total question count:", len(questions))

    print("Output all question data")
    crawler.write_all_questions_to_csv()

    print("Output all contest data")
    crawler.write_all_contest_to_csv()
