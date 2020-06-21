import requests
from requests import get
import time
from requests.adapters import HTTPAdapter
from requests.exceptions import ProxyError
from Code_retrieval.GetTags import GetTags
from Code_retrieval.DigitalOceanAPI import DigitalOceanAPI
from bs4 import BeautifulSoup
from Code_retrieval.GetCode import GetCode
from Code_retrieval.GetRevisions import GetRevisions
from Code_retrieval.GetAuthor import GetAuthor
from Code_retrieval.GetAccepted import GetAccepted
from Code_retrieval.GetPost import GetPost
from UserSelection import UserSelection
from Code_retrieval.DatabaseConnection import DatabaseConnection
from Code_retrieval.RequestTimeout import RequestTimeout

base_url = 'https://ru.stackoverflow.com/questions/'


def create_droplet(name):
    droplet = DigitalOceanAPI.create_droplet(name)
    status = DigitalOceanAPI.check_status(droplet)

    while status == "in-progress":
        status = DigitalOceanAPI.check_status(droplet)
        time.sleep(5)
    load = droplet.load()
    ip_address = load.ip_address

    status = DigitalOceanAPI.check_status(droplet)
    print(status)
    return ip_address, droplet


def delete_droplet(droplet):
    droplet.destroy()


def get_post():
    post_prompt = "Select a an already filtered .csv file (e.g. android.csv, kotlin.csv, ...)"
    selected_file = UserSelection.user_input(post_prompt)
    post_id = GetPost.get_id(selected_file)
    post_url = GetPost.create_url(base_url, post_id)

    return post_url, post_id


def get_revisions(post, i, database):
    revision_url = post.replace("questions", "posts") + "/revisions"
    # revision = get(revision_url, proxies=proxies)
    revision = get(revision_url)
    revision_soup = BeautifulSoup(revision.content, 'lxml')
    GetRevisions.get_revisions(revision_soup)
    user_detail = GetRevisions.get_user_details(revision_soup)
    user_id = GetRevisions.get_user_id(user_detail)
    user_reputation = GetRevisions.get_user_reputation(user_detail)
    GetRevisions.save_database(database, revision_url, user_id, user_reputation, i)


def get_author(soup):
    question_container = GetCode.get_question(soup)
    author, reputation, creation_date = GetAuthor.get_author(question_container)
    return author, reputation, creation_date


def get_code(conn, soup, i, accepted, author, reputation, creation_date, tags, post_id):
    question_container = GetCode.get_question(soup)
    answer_container = GetCode.get_answers(soup)
    question_pre = GetCode.get_pre(question_container)
    answer_pre = GetCode.get_pre(answer_container)

    question_code = GetCode.get_code(question_pre)
    answer_code = GetCode.get_code(answer_pre)
    GetCode.save_database(i, conn, post_id, author, reputation, creation_date, accepted, question_code, answer_code,
                          tags)


def get_tags(soup):
    question = GetCode.get_question(soup)
    tags = GetTags.get_tags(question)
    separator = ', '
    tags = separator.join(tags)
    return tags


def get_accepted(soup):
    answer_container = GetCode.get_answers(soup)
    accepted_post = GetAccepted.accepted_id(answer_container)
    accepted_author = GetAuthor.get_author(accepted_post)
    return accepted_author


def proxy_function():
    user_input = input("Type True to enable proxies, False to disable proxies: ")
    if user_input == "True":
        enable_proxies = True
        return enable_proxies
    if user_input == "False":
        enable_proxies = False
        return enable_proxies
    else:
        proxy_function()


def select_parameter(post):
    print("Total length of posts:")
    print(len(post))
    start_parameter = input("Select a start parameter: ")
    start_parameter = int(start_parameter)
    end_parameter = input("Select a end parameter: ")
    end_parameter = int(end_parameter)

    return start_parameter, end_parameter


def request_loop(i, loop_length, post_url, proxies, db_connection, droplet, post_id, file_name, enable_proxies):
    while i < loop_length:
        time.sleep(1)
        if enable_proxies:
            try:
                get(post_url[i], proxies=proxies)
            except ProxyError:
                request_loop(i, loop_length, post_url, proxies, db_connection, droplet, post_id, file_name,
                             enable_proxies)
                print("Proxy Error")
            response = get(post_url[i], proxies=proxies)
        else:
            response = get(post_url[i])
        html_soup = BeautifulSoup(response.content, 'lxml')
        if RequestTimeout.check_availability(response):
            if enable_proxies:
                delete_droplet(droplet)
                ip_address, droplet = create_droplet("proxy-droplet")
                proxies = {
                    "http": "https://" + ip_address + ":3128",
                    "https": "https://" + ip_address + ":3128",
                }

                request_loop(i, loop_length, post_url, proxies, db_connection, droplet, post_id, file_name,
                             enable_proxies=True)
            else:
                time.sleep(300)
                request_loop(i, loop_length, post_url, proxies, db_connection, droplet, post_id, file_name,
                             enable_proxies=False)

        else:
            accepted_post = get_accepted(html_soup)
            author, reputation, creation_date = get_author(html_soup)
            tags = get_tags(html_soup)
            get_code(db_connection, html_soup, i, accepted_post, author, reputation, creation_date, tags, post_id[i])
            i += 1
            # get_revisions(post_url[i], i, db_connection)
            file = open(file_name + '.txt', 'w')
            str_i = str(i)
            file.write(str_i)
            file.close()
    return droplet


def main():
    db_connection = DatabaseConnection.create_connection(
        r"C:\Users\ba051652\OneDrive - Otto-Friedrich-Universität Bamberg\SS 20\Bachelorarbeit\Python\Data-retrieval\Code_retrieval\stackoverflow_ru.db")
    post_url, post_id = get_post()
    file_name = UserSelection.save_name()
    enable_proxies = proxy_function()

    if enable_proxies:
        ip_address, droplet = create_droplet("proxy-droplet")
        proxies = {
            "http": "https://" + ip_address + ":3128",
            "https": "https://" + ip_address + ":3128",
        }
    else:
        proxies = None
        droplet = None


    i, end = select_parameter(post_url)
    # 1014 post without an author/ deleted account
    #i = 0
    droplet = request_loop(i, end, post_url, proxies, db_connection, droplet, post_id, file_name,
                           enable_proxies)

    if droplet is not None:
        delete_droplet(droplet)


if __name__ == "__main__":
    main()
