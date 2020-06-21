from bs4 import BeautifulSoup


class GetAuthor:

    @staticmethod
    def get_author(question):
        author = question.find_all('div', itemprop='author')
        author_soup = BeautifulSoup(str(author), 'lxml')

        date_span = question.find('span', class_='relativetime')

        if date_span is None:
            author_date = None
        else:
            author_date = date_span['title']
        author_reputation = author_soup.select_one("span[class=reputation-score]")
        if author_reputation is None:
            pass
        else:
            author_reputation = author_reputation.text

        user_id = []
        for a in author_soup.find_all('a', href=True):
            link = a['href']
            link_split = link.split("/")[2]

            id_int = int(link_split)
            user_id.append(id_int)
        return user_id, author_reputation, author_date
