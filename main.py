from Crawler import LeetcodeCrawler

if __name__ == '__main__':
    crawler = LeetcodeCrawler()
    questions = crawler.get_questions()
    print("Question count:", len(questions))
    print(questions[:5])
    print("Writing Csv File")
    crawler.write_csv("questions.csv")
