import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from typing import List
# 自製

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# pytube
from pytube import Playlist
import re

from lib.options import get_available_port, get_firefox_options


def get_releases_urls(url: str) -> list:
    """
    get all video urls if available, return urls
    """
    if "/releases" not in url:
        # try:
        #     url = "/".join(url.split("/")[:4]) + "/releases"
        # except:
        url = '{}/releases'.format(url)

    options = get_firefox_options(port=get_available_port(), is_headless=False)
    driver = webdriver.Firefox(options=options)
    # 设置隐式等待时间
    driver.implicitly_wait(10)
    # 发送请求
    driver.get(url)
    # 滑动到页面底部，加载所有视频
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 等待视频加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'video-title')))
    # 获取所有视频链接
    videos = driver.find_elements(
        By.CSS_SELECTOR, 'a#video-title-link')

    video_urls = []
    for video in videos:
        href = video.get_attribute('href')
        title = video.get_attribute('title')
        video_urls.append((href, title))

    driver.quit()

    return video_urls


def get_playlist_urls(url: str) -> list:
    """
    get all playlists if available, return urls
    """
    if "/playlists" not in url:
        # try:
        #     url = url.split("/")[0] + "/playlists"
        # except:
        url = '{}/playlists'.format(url)

    options = get_firefox_options(port=get_available_port(), is_headless=True)
    driver = webdriver.Firefox(options=options)
    # 设置隐式等待时间
    driver.implicitly_wait(10)
    # 发送请求
    driver.get(url)
    # 滑动到页面底部，加载所有播放列表
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 等待播放列表加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'video-title')))
    # 获取所有video-title元素的href属性
    hrefs = []
    video_title_elements = driver.find_elements(By.ID, 'video-title')
    for element in video_title_elements:
        href = element.get_attribute('href')
        title = element.get_attribute('title')
        hrefs.append((href, title))
    driver.quit()

    return hrefs


def get_playlist_urls(url: str) -> list:
    """
    get all playlists if available, return urls
    """
    if "/playlists" not in url:
        # try:
        #     url = "/".join(url.split("/")[:4]) + "/playlists"
        # except:
        url = '{}/playlists'.format(url)

    options = get_firefox_options(port=get_available_port(), is_headless=True)
    driver = webdriver.Firefox(options=options)
    # 设置隐式等待时间
    driver.implicitly_wait(10)
    # 发送请求
    driver.get(url)
    # 滑动到页面底部，加载所有播放列表
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # 等待播放列表加载完成
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'video-title')))
    # 获取所有video-title元素的href属性
    hrefs = []
    video_title_elements = driver.find_elements(By.ID, 'video-title')
    for element in video_title_elements:
        href = element.get_attribute('href')
        title = element.get_attribute('title')
        hrefs.append((href, title))

    driver.quit()

    return hrefs


def get_all_video_urls(urls: list) -> list:
    video_urls = []
    for url in urls:
        playlist = Playlist(url)
        video_urls.extend(playlist.video_urls)

    # 移除重复的视频URL
    video_urls = list(set(video_urls))

    return video_urls


def get_all_playlists_music_ID(url: str) -> list:
    """
    获取该artist_url属性的所有music_ID
    """

    music_ID_list = []
    try:
        playlist_urls = get_releases_urls(url=url)
    except:
        playlist_urls = get_playlist_urls(url=url)

    if len(playlist_urls) == 0:
        playlist_urls = get_playlist_urls(url=url)

    for playlist_url in playlist_urls:
        if playlist_url[0] is not None:
            video_urls = get_all_video_urls(urls=[playlist_url[0]])
            for video_url in video_urls:
                match = re.search(r'(?<=v=)[^&]+', video_url)
                if match:
                    music_ID = match.group(0)[-11:]
                    music_ID_list.append((playlist_url[1], music_ID))

    return music_ID_list


def get_all_playlists_music_ID_with_retry(url: str, max_retries=3) -> list:
    """
    获取该artist_url属性的所有music_ID，最多尝试max_retries次
    """

    for retry in range(max_retries):
        try:
            music_ID_list = []
            playlist_urls = get_releases_urls(url=url)
            if len(playlist_urls) == 0:
                playlist_urls = get_playlist_urls(url=url)

            for playlist_url in playlist_urls:
                if playlist_url[0] is not None:
                    video_urls = get_all_video_urls(urls=[playlist_url[0]])
                    for video_url in video_urls:
                        match = re.search(r'(?<=v=)[^&]+', video_url)
                        if match:
                            music_ID = match.group(0)[-11:]
                            music_ID_list.append((playlist_url[1], music_ID))

            return music_ID_list  # 如果成功获取数据，返回数据

        except Exception as e:
            print(f"Attempt {retry+1}/{max_retries} failed. Error: {str(e)}")
            if retry < max_retries - 1:
                # 如果尚未达到最大重试次数，请等待一段时间后重试
                time.sleep(5)  # 等待5秒钟（可以根据需要调整等待时间）
            else:
                # 如果达到最大重试次数，抛出异常或返回空列表，根据需求自行处理
                raise Exception("Max retries reached. Unable to fetch data.")

    return []  # 如果所有尝试都失败，返回空列表
