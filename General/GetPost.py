import pandas as pd
from UserSelection import UserSelection


class GetPost:

    @staticmethod
    def select_csv():
        post_prompt = "Select a an already filtered .csv file (e.g. android.csv, kotlin.csv, ...)"
        selected_file = UserSelection.user_input(post_prompt)
        return selected_file

    @staticmethod
    def get_id(csv):
        csv_data = pd.read_csv(csv)
        post_id = csv_data["Id"].tolist()
        return post_id

    @staticmethod
    def create_url(url, id):
        post_url = []
        i = 0
        for i in range(len(id)):
            post = url + str(id[i])
            post_url.append(post)
            i += 1
        return post_url

    @staticmethod
    def create_revision_url(url):
        url = url + "/revisions"
        return url

    @staticmethod
    def select_parameter(post):
        print("Total length of posts:")
        print(len(post))
        start_parameter = input("Select a start parameter: ")
        start_parameter = int(start_parameter)
        end_parameter = input("Select a end parameter: ")
        end_parameter = int(end_parameter)

        return start_parameter, end_parameter
