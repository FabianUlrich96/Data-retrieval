class GetTags:
    @staticmethod
    def get_tags(soup):
        tags = soup.find_all('div', class_='post-taglist grid gs4 gsy fd-column')
        tags_detail = []
        for link in tags:
            tags.extend(link.find_all('a'))
            tags_detail.append(link.text)

        return tags_detail
