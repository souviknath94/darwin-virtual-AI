#!/usr/bin/env python
# -*- coding: utf-8 -*-

from darwin.imports import *
from darwin.paths import __audio_files__

class Youtube:

    def __init__(self):
        self.BASE_URL = "https://yuotube.com"

    def __create_search_term(self, search_term):
        encoded_search = urllib.parse.quote(search_term)
        return encoded_search

    def youtube_search(self, search_term):
        encoded_search = self.__create_search_term(search_term)
        webbrowser.open(f'{self.BASE_URL}/results?search_query={encoded_search}')

    def youtube_play(self, search_term):
        encoded_search = self.__create_search_term(search_term)
        url = f"{self.BASE_URL}/results?search_query={encoded_search}"
        response = requests.get(url).text

        if 'window["ytInitialData"]' not in response:
            response = requests.get(url).text

        start = response.index('window["ytInitialData"]') + len('window["ytInitialData"]') + 3
        end = response.index("};", start) + 1

        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
                "sectionListRenderer"
            ]["contents"][0]["itemSectionRenderer"]["contents"]

        res_list = []
        for video in videos:
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                vid_id = video_data.get('videoId')
                res_list.append(vid_id)
        
        first_vid = res_list[0]
        play_url = f'{BASE_URL}/watch?v={first_vid}'
        webbrowser.open(play_url)


