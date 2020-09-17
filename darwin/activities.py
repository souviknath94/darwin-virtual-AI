#!/usr/bin/env python
# -*- coding: utf-8 -*-

from darwin.imports import *

class Encryption:
    
    def __init__(self, key=None):
        if key is not None:
            self.key = key
        else:
            self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def encrypt(self, text):
        bytes_text = str.encode(text)
        encode_text = self.cipher_suite.encrypt(bytes_text)
        return encode_text
    
    def decrypt(self, encoded_text):
        decoded_text = self.cipher_suite.decrypt(encoded_text)
        final_text = decoded_text.decode()
        return final_text


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
        play_url = f'{self.BASE_URL}/watch?v={first_vid}'
        webbrowser.open(play_url)

class Weather:
    
    def __init__(self, text):
        self.text = text
        self.BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
        self.api_key = self.load_api_key()
        self.city = self.find_city()
        
    def load_api_key(self):
        
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'encryption.yaml'), 'r') as reader:
            api_inf = yaml.safe_load(reader)
        
        enc = Encryption(key=api_inf['fernet_key'])
        api_key = enc.decrypt(api_inf['api_key_encrypted'])

        return api_key
    
    def find_city(self):
        geoloc = geotext.GeoText(self.text)
        city = ''.join(geoloc.cities)
        return city

    def visibility_classification(self, visibility):
        if visibility>=40000:
            res = 'Excellent'
        elif visibility>=20000 and visibility<40000:
            res = 'Very Good'
        elif visibility>=10000 and visibility<20000:
            res = 'Good'
        elif visibility>2000 and visibility<10000:
            res = 'Moderate'
        elif visibility>=1000 and visibility<2000:
            res = 'Poor'
        elif visibility>=200 and visibility<1000:
            res = 'Fog'
        elif visibility>=40 and visibility<200:
            res = 'Thick Fog'
        elif visibility<40:
            res = 'Dense Fog'
        
        return res
    
    def get_weather_report(self):
        
        complete_url = self.BASE_URL+"appid="+self.api_key+"&q="+self.city
        response = requests.get(complete_url)
        data = response.json()
        
        temparature = int(round(data['main']['temp']-273.15, 0))
        humidity = data['main']['humidity']
        visibility = data['visibility']
        
        weather_info = f'The temparature of {self.city} today is {temparature} degree Centigrade with humidity being {humidity} and the visibility remains {self.visibility_classification(visibility)}'
        return weather_info


def save_darwin_pictures():

    home_dir = os.path.expanduser('~')
    desktop_exists = ''.join([i for i in os.listdir(home_dir) if 'Desktop' in i])
    
    try:
        save_dir_exists = ''.join([i for i in os.listdir(os.path.join(home_dir, desktop_exists)) if 'Darwin-captures' 
        in i])
    except:
        save_dir_exists = None

    if desktop_exists and not save_dir_exists:
        os.makedirs(os.path.join(home_dir, desktop_exists, 'Darwin-captures'), exist_ok=True)
        save_dir = os.path.join(home_dir, desktop_exists, 'Darwin-captures')
    elif desktop_exists and save_dir_exists:
        save_dir = os.path.join(home_dir, desktop_exists, 'Darwin-captures')

    return save_dir

def take_photo():
    
    camera = cv2.VideoCapture(0)
    i = 0
    while i<10:
        _, image = camera.read()
        i += 1
        if i==10:
            cv2.imwrite(os.path.join(save_darwin_pictures, 'darwin_capture.png'), image)
            
    del camera


def wolfram(command):
    
    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'wolfram_api.yaml'), 'r') as reader:
        api_inf = yaml.safe_load(reader)
        
    enc = Encryption(key=api_inf['fernet_key'])
    app_id = api_inf['wolfram_app_id']
    api_key = enc.decrypt(app_id)

    client = wolframalpha.Client(api_key)
    res = client.query(command)
    answer = next(res.results).text
    
    return answer