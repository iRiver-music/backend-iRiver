import json
import os
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from bs4.element import Tag
current_directory = os.getcwd()

"""chrome"""


def get_style(la=""):
    def web_driver():
        options = webdriver.ChromeOptions()
        options.add_argument("--verbose")
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument("--window-size=1920, 1200")
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=options)
        return driver

    def scroll(new_driver):
        scrolls = 0

        while True:
            new_driver.execute_script('window.scrollBy(0,1000);')
            scrolls += 1
            time.sleep(1)
            print(str(scrolls))
            if scrolls == 10:
                break

    # for i in range(1):

    def load_list(playlist, new_driver, list_name, title, i):
        # playlistid = playlists[i]['Link'][21:69]
        playlistid = playlist['Link'][21:69]
        link = 'https://www.youtube.com/playlist?' + playlistid
        new_driver.get(link)
        scroll(new_driver)

        html = new_driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # test = soup.find_all("img", {'class': 'yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded'})

        # 設置container
        container = soup.find_all("div", {'id': 'container'})
        # 下載
        album(container, list_name, title, i)
        # return test

    # lists = []

    def album(container, list_name, title, playlist):
        id = 0
        for tag in container:
            # if isinstance(n_tag, Tag):
            listt = {}
            temp = 0
            # listt['Title'] = title
            listt['albumSuperSetTitle'] = title
            listt['Album'] = list_name
            # 名稱
            name = tag.find("a", {
                            'class': 'yt-simple-endpoint style-scope ytd-playlist-video-renderer'}, {'id': 'video-title'})
            if name:
                listt['Name'] = name.text.strip()
                temp = temp+1

            # 人物
            desc = tag.find(
                "a", {'class': 'yt-simple-endpoint style-scope yt-formatted-string'})
            if desc:
                listt['Artist'] = desc.text.strip()
                temp = temp+1

            # 圖片
            count = tag.find("img", {
                'class': 'yt-core-image--fill-parent-height yt-core-image--fill-parent-width yt-core-image yt-core-image--content-mode-scale-aspect-fill yt-core-image--loaded'})
            if count:
                listt['pic'] = count['src']
                temp = temp+1

            # 鏈接
            link = tag.find("a", {'id': 'thumbnail'})
            if link:
                listt['Link'] = link['href']
                temp = temp+1

            if temp == 4:
                id = id + 1
                listt['ID'] = id
                listt['Description'] = playlist["Description"]
                lists.append(listt)

    def Scrap1():
        driver = web_driver()
        driver.get(
            'https://www.google.com/search?q=youtube+%E9%9F%B3%E6%A8%82%E9%A0%BB%E9%81%93')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        h = soup.find("div", {'class': 'yuRUbf'})
        h2 = h.find('a', {'data-jsarwt': '1'})['href']
        #
        driver = web_driver()
        driver.get(h2)
        scroll(driver)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        #
        t_tags = soup.find_all("ytd-item-section-renderer",
                               {'class': 'ytd-section-list-renderer'})
        #
        playlists = []
        for n_tag in t_tags:
            playlist = {}
            temp = 0

            title = n_tag.find(
                "span", {'class': 'style-scope ytd-shelf-renderer'})
            names = n_tag.findAll(
                "h3", {'class': 'style-scope ytd-compact-station-renderer'})
            descs = n_tag.findAll(
                "p", {'class': 'style-scope ytd-compact-station-renderer'})
            counts = n_tag.findAll(
                "p", {'class': 'style-scope ytd-compact-station-renderer', 'id': 'video-count-text'})
            links = n_tag.findAll("a", {'id': 'thumbnail'})

            for name, desc, count, link in zip(names, descs, counts, links):
                playlist = {}
                playlist['Title'] = title.text.strip()
                playlist['Name'] = name.text.strip() if name else None
                playlist['Description'] = desc.text.strip() if desc else None
                playlist['Track Count'] = count.text.strip() if count else None
                playlist['Link'] = link['href'] if link else None
                playlists.append(playlist)
        # lists = []
        index = 0
        for i in playlists:  # test
            # for i in playlists:
            print("list index = ", index)
            index = index + 1
            # 重新連線 driver = web_driver()
            driver = web_driver()

            list_name = i['Name']
            title = i['Title']
            # loading
            load_list(i, driver, list_name, title, i)

    """discover test"""

    lists = []
    Scrap1()

    file_path = os.path.join(current_directory, "script",
                             "lib", "style_{}.json".format(la))
    if os.path.exists(file_path):
        os.remove(file_path)
        print('Existing JSON file has been deleted.')

    if not os.path.exists(file_path):
        with open(file_path, 'w') as json_file:
            json.dump(lists, json_file)

    print('JSON data has been saved to', file_path)
