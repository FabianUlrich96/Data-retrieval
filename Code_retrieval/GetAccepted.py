from bs4 import BeautifulSoup


class GetAccepted:
    @staticmethod
    def accepted_id(answer):
        post_accepted = answer.find_all('div', class_="answer accepted-answer")

        # todo get accepted post ID
        post_soup = BeautifulSoup(str(post_accepted), 'lxml')
        return post_soup


