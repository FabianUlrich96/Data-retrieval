from requests import get
from bs4 import BeautifulSoup
from Code_retrieval.GetCode import GetCode
from Code_retrieval.GetRevisions import GetRevisions
from Code_retrieval.GetAuthor import GetAuthor
from Code_retrieval.GetAccepted import GetAccepted
url = 'https://ru.stackoverflow.com/questions/1138934/'
#url = 'https://ru.stackoverflow.com/questions/1140031/'
response = get(url)
html_soup = BeautifulSoup(response.content, 'lxml')

def get_id():
    



def get_revisions():
    revision_url = url.replace("questions", "posts") + "revisions"
    print(revision_url)
    revision = get(revision_url)
    revision_soup = BeautifulSoup(revision.content, 'lxml')
    GetRevisions.get_revisions(revision_soup)
    user_detail = GetRevisions.get_user_details(revision_soup)
    user_link = GetRevisions.get_user_link(user_detail)
    user_reputation = GetRevisions.get_user_reputation(user_detail)

    print(user_link)
    print(user_reputation)


def get_author():
    question_container = GetCode.get_question(html_soup)
    author = GetAuthor.get_author(question_container)
    print(author)


def get_code():

    question_container = GetCode.get_question(html_soup)
    answer_container = GetCode.get_answers(html_soup)
    question_pre = GetCode.get_pre(question_container)
    answer_pre = GetCode.get_pre(answer_container)

    question_code = GetCode.get_code(question_pre)
    answer_code = GetCode.get_code(answer_pre)

    print(question_code)
    print(answer_code)


def get_accepted():
    answer_container = GetCode.get_answers(html_soup)
    accepted_post = GetAccepted.accepted_id(answer_container)
    accepted_author = GetAuthor.get_author(accepted_post)


def main():
    get_code()
    get_revisions()
    get_author()
    get_accepted()


if __name__ == "__main__":
    main()
