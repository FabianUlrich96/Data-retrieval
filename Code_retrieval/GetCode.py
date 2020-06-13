from requests import get
from bs4 import BeautifulSoup
url = 'https://ru.stackoverflow.com/questions/1138934/%d0%92%d1%8b%d0%bb%d0%b5%d1%82%d0%b0%d0%b5%d1%82-%d0%bf%d1%80%d0%be%d0%b3%d1%80%d0%b0%d0%bc%d0%bc%d0%b0-%d0%bf%d1%80%d0%b8-%d0%bf%d0%be%d0%bf%d1%8b%d1%82%d0%ba%d0%b5-%d0%b2%d1%8b%d0%b2%d0%b5%d1%81%d1%82%d0%b8-%d0%bd%d0%b5%d0%ba%d1%82%d0%be%d1%80%d1%8b%d0%b5-%d0%b0%d1%80%d0%b3%d1%83%d0%bc%d0%b5%d0%bd%d1%82%d1%8b-%d0%b2-log-kotlin'
#url = 'https://ru.stackoverflow.com/questions/1140031/%d0%9f%d1%80%d0%be%d0%b1%d0%bb%d0%b5%d0%bc%d0%b0-%d1%81-arrayadapter-spiner'
response = get(url)

html_soup = BeautifulSoup(response.content, 'lxml')


def get_question():
    question = html_soup.find_all('div', class_='question')
    question_soup = BeautifulSoup(str(question), 'lxml')

    print(question_soup)
    return question_soup


def get_answers():
    answer = html_soup.find_all('div', class_='answer')
    answer_soup = BeautifulSoup(str(answer), 'lxml')

    return answer_soup


def get_pre(container):
    pre_tag = container.find_all('pre')
    pre_soup = BeautifulSoup(str(pre_tag), 'lxml')

    return pre_soup


def get_code(pre):

    pre_code = []
    for code in pre:
        pre_code.extend(code.find_all('code'))
        pre_row = [code.text for code in pre_code]

        return pre_row


def main():
    question_container = get_question()
    answer_container = get_answers()
    question_pre = get_pre(question_container)
    answer_pre = get_pre(answer_container)


    question_code = get_code(question_pre)
    answer_code = get_code(answer_pre)

    print(question_code)
    print(answer_code)


if __name__ == "__main__":
    main()
