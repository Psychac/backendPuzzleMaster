import requests
import os


def calibrate():
    url = 'http://127.0.0.1:8000/calibrate'
    #print(os.getcwd())
    #Green
    payload = {'color': "Green",'side':"F"}
    my_img = {'image': open('./Test/rubiks-side-F.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    #Yellow
    payload = {'color': "Yellow",'side':"R"}
    my_img = {'image': open('./Test/rubiks-side-R.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    #Blue
    payload = {'color': "Blue",'side':"B"}
    my_img = {'image': open('./Test/rubiks-side-B.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    #Orange
    payload = {'color': "Orange",'side':"L"}
    my_img = {'image': open('./Test/rubiks-side-L.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    #White
    payload = {'color': "White",'side':"U"}
    my_img = {'image': open('./Test/rubiks-side-U.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    #Red
    payload = {'color': "Red",'side':"D"}
    my_img = {'image': open('./Test/rubiks-side-D.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)

    # convert server response into JSON format.
    print(r.json())
    #return r

def cubenotation():
    url = 'http://127.0.0.1:8000/colors'
    #Green
    payload = {'side':"Front"}
    my_img = {'image': open('./Test/rubiks-side-F.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    print(r.json())
    #Yellow
    payload = {'side':"Right"}
    my_img = {'image': open('./Test/rubiks-side-R.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    print(r.json())
    #Blue
    payload = {'side':"Back"}
    my_img = {'image': open('./Test/rubiks-side-B.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    print(r.json())
    #Orange
    payload = {'side':"Left"}
    my_img = {'image': open('./Test/rubiks-side-L.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    print(r.json())
    #White
    payload = {'side':"Up"}
    my_img = {'image': open('./Test/rubiks-side-U.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    print(r.json())
    #Red
    payload = {'side': "Down"}
    my_img = {'image': open('./Test/rubiks-side-D.jpg', 'rb')}
    r = requests.post(url, files=my_img,data=payload)
    print(r.json())

def result():
    url = 'http://127.0.0.1:8000/result'
    #payload = {'status': True}
    result = requests.post(url)
    print(result.json())

def reset():
    url = 'http://127.0.0.1:8000/resetapp'
    payload = {'status': True}
    result = requests.post(url,data=payload)
    print(result.json())


def cal():
    url = 'http://127.0.0.1:8000/calibratePallete'
    payload = {'red': (0, 0, 255),
    'orange': (0, 165, 255),
    'blue'  : (255, 0, 0),
    'green' : (0, 255, 0),
    'white' : (255, 255, 255),
    'yellow': (0, 255, 255)}
    r = requests.post(url,data=payload)
    print(r.json())

# cal()
calibrate()
cubenotation()
result()
reset()

#FDBLUDBULFBRLRURDBLFDDFFUBBFRURDLFBLUUDULFDFLDRRRBBULR