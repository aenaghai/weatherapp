from cProfile import label
import os
import pytz
import pyowm
import seaborn as sns
from pyowm import OWM
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt


#API id from openweathermap
owm = pyowm.OWM('08820823151504804d9d6c720d917d80')     
mgr = owm.weather_manager()

degree = u'\N{DEGREE SIGN}'

st.title('Weather Forecast ' + "\U0001F600" )
st.write('Write the name of a City and select the Temperature Unit and Graph Type from the sidebar')

city = st.text_input("Name of the City: ", "")

if city == None:
    st.write("Please Enter a city name")

unit = st.selectbox("Select the Temperature Unit: ", ("Celsius", "Fahrenheit"))
graph = st.selectbox("Select the Graph Type: ", ("Line Graph", "Bar Graph"))


def temp():
    dates = []
    days = []
    mint = []
    maxt = []
    forecaster = mgr.forecast_at_place(city, '3h')
    forecast = forecaster.forecast
    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())  
        date = day.date()
        
        if date not in dates:
            dates.append(date)
        
        temperature = weather.temperature(units)['temp']
        
        if unit == 'Celsius':
            units = 'celsius'
        else:
            units = 'fahrenheit'
    
        
        if not mint[-1] or temperature < mint[-1]:
            mint[-1] = temperature
        if not maxt[-1] or temperature > maxt[-1]:
            maxt[-1] = temperature
            
    return(days, mint, maxt)   
    
def w_updates():
    forecaster = mgr.forecast_at_place(city, '3h') 
    st.title("Impending Temperature Changes: ")
    if forecaster.will_have_fog():
        st.write("FOG Alert!")
    if forecaster.will_have_rain():
        st.write("Rain Alert 🌧️")
    if forecaster.will_have_storm():
        st.write("Storm Alert! ⛈️")
    if forecaster.will_have_snow():
        st.write("Snow Alert! ❄️")
    if forecaster.will_have_tornado():
        st.write("Tornado Alert! 🌪️")
    if forecaster.will_have_hurricane():
        st.write("Hurricane Alert! ")
    if forecaster.will_have_clouds():
        st.write("Cloudy Skies ☁️")    
    if forecaster.will_have_clear():
        st.write("Clear Weather! 🪂")

def cloudandwind():
    obs=mgr.weather_at_place(city)
    w = obs.weather
    clouds = w.clouds
    winds = w.wind()['speed']
    st.title("Cloud coverage and wind speed")
    st.write('The current cloud coverage for',city,' is ',clouds,'%')
    st.write('The current wind speed for',city, ' is ',winds,'mph')

def riseandset():
    obs=mgr.weather_at_place(city)
    w = obs.weather
    st.title('Sunrise and Sunset Times')
    india = pytz.timezone("Asia/Kolkata")
    ss=w.sunset_time(timeformat='iso')
    sr=w.sunrise_time(timeformat='iso')  
    st.write("Sunrise time in ",city," is ",sr)
    st.write("Sunset time in ",city," is ",ss)
    
def updates():
    w_updates()
    cloudandwind()
    riseandset()

if __name__ == '__main__':
    
    if st.button("SUBMIT"):
        updates()
