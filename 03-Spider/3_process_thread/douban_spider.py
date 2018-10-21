

from urllib import parse
import requests
import threading


def get_json_info(url):
    response = requests.get(url)
    return response.json()


class spiderDB(threading.Thread):

    def __init__(self):
        super(spiderDB, self).__init__()
        self.lock = threading.Lock()

    def update_movie_list(self):
        if self.lock.acquire():
            link = movies_list.pop() if movies_list else ''
            self.lock.release()
            return link

    def run(self):
        task_link = self.update_movie_list()
        if task_link:
            movies_res = get_json_info(task_link)
            result = movies_res['subjects']
            for res in result:
                print(res['title'], res['rate'])


def main():

    tag_url = 'https://movie.douban.com/j/search_tags?type=movie&source='
    movie_url = 'https://movie.douban.com/j/search_subjects?type=movie&%s&sort=recommend&page_limit=20&page_start=0'
    tage_list = get_json_info(tag_url)
    global movies_list
    movies_list = []
    for tag in tage_list['tags']:
        data = {'tag': tag}
        m_url = movie_url % parse.urlencode(data)
        movies_list.append(m_url)

    # print(movies_list)
    while movies_list:
        s1 = spiderDB()
        s2 = spiderDB()
        s3 = spiderDB()
        s4 = spiderDB()
        s5 = spiderDB()
        s1.start()
        s2.start()
        s3.start()
        s4.start()
        s5.start()


if __name__ == '__main__':
    main()
