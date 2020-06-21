from requests import get
import time
from requests.exceptions import ProxyError
from Code_retrieval.GetTags import GetTags
from General.DigitalOceanAPI import DigitalOceanAPI
from bs4 import BeautifulSoup
from Code_retrieval.GetCode import GetCode
from Code_retrieval.GetAuthor import GetAuthor
from Code_retrieval.GetAccepted import GetAccepted
from General.GetPost import GetPost
from UserSelection import UserSelection
from General.DatabaseConnection import DatabaseConnection
from General.RequestTimeout import RequestTimeout

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
                DigitalOceanAPI.delete_droplet(droplet)
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
            file = open(file_name + '.txt', 'w')
            str_i = str(i)
            file.write(str_i)
            file.close()
    return droplet


def main():
    db_connection = DatabaseConnection.create_connection(
        r"C:\Users\ba051652\OneDrive - Otto-Friedrich-Universität Bamberg\SS 20\Bachelorarbeit\Materialien\StackOverflow data dump\ru_database\stackoverflow_ru.db")
    selected_csv = GetPost.select_csv()
    post_id = GetPost.get_id(selected_csv)
    post_url = GetPost.create_url(base_url, post_id)
    file_name = UserSelection.save_name()
    enable_proxies = DigitalOceanAPI.proxy_function()

    if enable_proxies:
        ip_address, droplet = create_droplet("proxy-droplet")
        proxies = {
            "http": "https://" + ip_address + ":3128",
            "https": "https://" + ip_address + ":3128",
        }
    else:
        proxies = None
        droplet = None

    i, end = GetPost.select_parameter(post_url)
    # 1014 post without an author/ deleted account
    droplet = request_loop(i, end, post_url, proxies, db_connection, droplet, post_id, file_name,
                           enable_proxies)

    if droplet is not None:
        DigitalOceanAPI.delete_droplet(droplet)


if __name__ == "__main__":
    main()
