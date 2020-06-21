import pandas as pd


class GetPost:
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
