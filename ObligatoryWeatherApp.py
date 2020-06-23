import PySimpleGUI as sg
import json, requests

gapi = "AIzaSyC8uR1p17ctHSa0V0_rCa6UALybGrB0I4Y"
apikey = "886705b4c1182eb1c69f28eb8c520e20"
# base_url variable to store url 
url = "https://maps.googleapis.com/maps/api/geocode/json?address="

city_name = "mansfield, TX"

myString = ""
for i in city_name:
    if i == " ":
        myString+="+"
    else:
        myString+=i

#print(myString)

complete_url = url + myString+ "&key=" + gapi

response = requests.get(complete_url)


json_object = response.json()

jsonFormatted = json.dumps(json_object["results"][0]["geometry"]["location"], indent=2)




a = json_object["results"][0]["geometry"]["location"]["lat"]
b = json_object["results"][0]["geometry"]["location"]["lng"]

url = "https://api.weather.gov/points/"+str(a)+","+str(b)

response  = requests.get(url)
json_object = response.json()
jsonFormatted = json.dumps(json_object, indent=2)


url = json_object["properties"]["forecast"]

response = requests.get(url)
json_object = response.json()

jsonFormatted = json.dumps(json_object, indent=2)


forecastList = []
num = 0
for i in json_object["properties"]["periods"]:
    forecastList.append( (i['name'],i["detailedForecast"],i["icon"]))





print(f"Length: {len(forecastList)}")
for i in range(0,14):
    print(f"{i}; {forecastList[i]}")

layout = []
column = []
layout+= [[sg.Text("Obligatory Weather API App",key="title", font = "cambria 30", text_color = "Blue")]]
layout+= [sg.Input("What's your city and state?", visible = True),sg.Button("OK"),sg.Combo(['Normal', 'Detailed','Tiny'])],
frame_layout =[]
frame_layout2 = []
frame_layout2+=[[sg.Text("textBox0",size = (25,12),font = "cambria 12",key="textBox0"),sg.Image(data = "", key="image0")]]

for i in range(1,14):
    print(f"textBox is {[i]}")
    frame_layout += [
        [
                  [sg.Text(f"textBox{i}",size = (25,12),font = "cambria 12",key=f"textBox{i}")],
                  [sg.Image(data = "", key=f"image{i}")]
           ]       
               ]

layout+= [  [sg.Frame(forecastList[0][0], frame_layout2, font = 'Any 12', title_color='green')for i in range(0,1)]]
layout+= [  [sg.Frame(forecastList[i][0], frame_layout[i-1], font='Any 12', title_color='blue')for i in range(1,14,2)]]
layout+= [  [sg.Frame(forecastList[i][0], frame_layout[i-1], font='Any 12', title_color='blue')for i in range(2,13,2)]]


window = sg.Window("a",layout,grab_anywhere=True)
window.finalize()

while True:
    window['textBox0'].update("hello")
    for i in range (0,14):
        window[f"textBox{i}"].Update(forecastList[i][1])
        #print(forecastList[i][0])
        url = forecastList[i][2]
        #print(forecastList[i][2])
        response = requests.get(url)
        img = (response.content)
        window[f"image{i}"].Update(data=img)
                               
    window.read()
