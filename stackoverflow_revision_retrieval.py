import time
from requests import get
from requests.exceptions import ProxyError
from bs4 import BeautifulSoup
from General.GetPost import GetPost
from General.RequestTimeout import RequestTimeout
from General.DatabaseConnection import DatabaseConnection
from Revision_retrieval.GetRevisions import GetRevisions
from General.DigitalOceanAPI import DigitalOceanAPI
from UserSelection import UserSelection

base_url = 'https://ru.stackoverflow.com/posts/'


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


def get_revisions(post, i, database, revision_soup):
    GetRevisions.get_revisions(revision_soup)
    user_detail = GetRevisions.get_user_details(revision_soup)
    user_id = GetRevisions.get_user_id(user_detail)
    user_reputation = GetRevisions.get_user_reputation(user_detail)
    post = str(post[i])
    GetRevisions.save_database(database, post, user_id, user_reputation, i)


def request_loop(i, loop_length, post_url, proxies, db_connection, droplet, post_id, file_name, enable_proxies):
    while i < loop_length:
        revision_url = GetPost.create_revision_url(post_url[i])
        time.sleep(1)
        if enable_proxies:
            try:
                get(revision_url, proxies=proxies)
            except ProxyError:
                request_loop(i, loop_length, post_url, proxies, db_connection, droplet, post_id, file_name,
                             enable_proxies)
                print("Proxy Error")
            response = get(revision_url, proxies=proxies)
        else:
            response = get(revision_url)
        html_soup = BeautifulSoup(response.content, 'lxml')
        if RequestTimeout.check_availability(response):
            if enable_proxies:
                DigitalOceanAPI.delete_droplet(droplet)
                ip_address, droplet = DigitalOceanAPI.create_droplet("proxy-droplet")
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
            get_revisions(post_id, i, db_connection, html_soup)
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

    droplet = request_loop(i, end, post_url, proxies, db_connection, droplet, post_id, file_name, enable_proxies)
    if droplet is not None:
        DigitalOceanAPI.delete_droplet(droplet)


if __name__ == "__main__":
    main()
