import sqlite3

from bs4 import BeautifulSoup
import pandas as pd
from General.DatabaseConnection import DatabaseConnection


class GetRevisions:
    @staticmethod
    def get_revisions(html_soup):
        revisions = html_soup.find_all('div', class_='revisions')
        revisions_soup = BeautifulSoup(str(revisions), 'lxml')

        return revisions_soup

    @staticmethod
    def get_user_details(html_soup):
        details = html_soup.find_all('div', class_='user-details')
        details_soup = BeautifulSoup(str(details), 'lxml')

        return details_soup

    @staticmethod
    def get_user_id(detail):
        user_id = []
        for a in detail.find_all('a', href=True):
            link = a['href']
            link_split = link.split("/")[2]

            id_int = int(link_split)
            user_id.append(id_int)
            return user_id

    @staticmethod
    def get_user_reputation(detail):
        user_detail = []
        for reputation in detail:
            user_detail.extend(reputation.find_all('span', class_='reputation-score'))
            reputation_row = [reputation.text for reputation in user_detail]

            return reputation_row

    @staticmethod
    def save_database(db_file, revision_url, ids, reputations, i):
        columns = ["Post", "Reputation", "User_Id"]
        data = pd.DataFrame(columns=columns)
        j = 0
        for user_id in ids:
            if user_id:
                pass
            else:
                user_id = None
            add_data = data.append({'Post': revision_url, 'Reputation': reputations[j], 'User_Id': user_id},
                                   ignore_index=True)
            j += 1
            conn = sqlite3.connect(db_file)
            if i == 0:
                sql_create_revisions_table = """ CREATE TABLE IF NOT EXISTS revisions (
                                                       post text PRIMARY KEY,
                                                       reputation text ,
                                                       user_id text                                                  
                                                   ); """
                DatabaseConnection.create_table(conn, sql_create_revisions_table)
                add_data.to_sql('revisions', conn, if_exists='replace', index=False)

            else:
                add_data.to_sql('revisions', conn, if_exists='append', index=False)




