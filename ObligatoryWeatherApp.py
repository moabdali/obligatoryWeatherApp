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


#print(jsonFormatted)

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
#print(jsonFormatted)

forecastList = []
num = 0
for i in json_object["properties"]["periods"]:
    #print(i['name']+": \n"+i["detailedForecast"]+"\n\n")
    forecastList.append( (i['name'],i["detailedForecast"],i["icon"]))
    #print(f"forcastList is: {forecastList}")







print(forecastList[0][2])

layout = []
column = []
layout.append( [sg.Text("Obligatory Weather API App",key="title", font = "cambria 30", text_color = "Blue")])
frame_layout =[]
for i in range(0,14):
    frame_layout += [
        [
                  [sg.Text("a",size = (12,25),font = "cambria 12",key=f"textBox{i}")],
                  [sg.Image(data = "", key=f"image{i}")]
           ]       
               ]


layout+= [  [sg.Frame(forecastList[i][0], frame_layout[i], font='Any 12', title_color='blue')for i in range(0,14)]]  

##column2=[    ]


#layout+=column1
#layout+=column2

window = sg.Window("a",layout,finalize = True,grab_anywhere=True)

for i in range (0,14):
    window[f"textBox{i}"].Update(forecastList[i][1])
    print(forecastList[i][0])
    url = forecastList[i][2]
    #print(forecastList[i][2])
    response = requests.get(url)
    img = (response.content)
    window[f"image{i}"].Update(data=img)
                               


window.read()
