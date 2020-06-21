import sqlite3

import pandas as pd
from bs4 import BeautifulSoup
from General.DatabaseConnection import DatabaseConnection


class GetCode:

    @staticmethod
    def get_question(html_soup):
        question = html_soup.find_all('div', class_='question')
        question_soup = BeautifulSoup(str(question), 'lxml')

        return question_soup

    @staticmethod
    def get_answers(html_soup):
        answer = html_soup.find_all('div', class_='answer')
        answer_soup = BeautifulSoup(str(answer), 'lxml')

        return answer_soup

    @staticmethod
    def get_pre(container):
        pre_tag = container.find_all('pre')
        pre_soup = BeautifulSoup(str(pre_tag), 'lxml')

        return pre_soup

    @staticmethod
    def get_code(pre):

        pre_code = []
        for code in pre:
            pre_code.extend(code.find_all('code'))
            pre_row = [code.text for code in pre_code]

            return pre_row

    @staticmethod
    def save_database(i, db_file, post_id, authors, reputation, creation_date, accepted, question_code, answer_code, tags):
        if accepted is not None:
            accepted = accepted[0]
        if question_code:
            question_code = list(question_code)[0]
        else:
            question_code = None

        if answer_code:
            answer_code = list(answer_code)[0]
        else:
            answer_code = None

        if accepted:
            accepted = accepted[0]
        else:
            accepted = None
        reputation = str(reputation)

        post_id = str(post_id)

        columns = ["Post", "Creation_Date", "Author", "Reputation", "Accepted", "Question_Code", "Answer_Code", "Tags"]
        data = pd.DataFrame(columns=columns)
        j = 0
        if authors is None:
            pass
        else:
            for author in authors:
                add_data = data.append(
                    {'Post': post_id, 'Creation_Date': creation_date, 'Author': author, 'Reputation': reputation, 'Accepted': accepted, 'Question_Code': question_code,
                     'Answer_Code': answer_code, 'Tags': tags},
                    ignore_index=True)
                j += 1

                conn = sqlite3.connect(db_file)
                if i == 0:
                    sql_create_posts_table = """ CREATE TABLE IF NOT EXISTS posts (
                                                              post text PRIMARY KEY,
                                                              creation_date DATE,                                                     
                                                              author text ,  
                                                              reputation text,                                                         
                                                              accepted text,
                                                              question_code text,
                                                              answer_code text,
                                                              tags text                                                  
                                                          ); """
                    DatabaseConnection.create_table(conn, sql_create_posts_table)

                    add_data.to_sql('posts', conn, if_exists='append', index=False)
                else:
                    add_data.to_sql('posts', conn, if_exists='append', index=False)
