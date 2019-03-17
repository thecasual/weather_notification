import configparser
import os.path
import requests
import smtplib
import json

config = configparser.ConfigParser()
if os.path.isfile('weathermailer_custom.conf'):
    config.read('weathermailer_custom.conf')
else:
    config.read('weathermailer.conf')

phonenumber = list(config.items('phonenumbers'))
smtpserver = config['SETTINGS']['smtpserver']
coords = config['SETTINGS']['coords']

class weather():
    def __init__(self, phonenumber, smtpserver, coords):
        self.phonenumber = phonenumber
        self.smtpserver = smtpserver
        self.coords= coords
        self.url = 'https://api.weather.gov/points/{0}/forecast'.format(self.coords)
        self.message = ""
        self.subject = ""

    def getweather(self):
        r = requests.get(self.url)
        self.response = r.json()
        self.tonightweather = self.response['properties']['periods'][1]['detailedForecast']
        self.allweatherstatuses = self.response['properties']['periods']
        self.afternoonweather = self.response['properties']['periods'][0]['detailedForecast']

    def sendmessage(self):
        
        self.smtpobject = smtplib.SMTP(self.smtpserver, 25)
        
        self.messagelenth = len(self.message)
        self.messages2send = int(self.messagelenth / 100) + (self.messagelenth % 100 > 0)
        for order, number in self.phonenumber:
            if self.messages2send == 1:
                self.smtpobject.sendmail(self.subject, str(number), self.message)
            else:
                for chunk in range(self.messages2send):
                    if int(chunk) == 0:
                        self.smtpobject.sendmail(self.subject, str(number), self.message[0:100])
                    else:
                        self.smtpobject.sendmail(self.subject, str(number), self.message[(100 * chunk):(100 * chunk + 100)])
                
            print("Sent the following text '{0}' to {1} in {2} messages".format(self.message, str(number), self.messages2send))

if __name__ == "__main__":
    weather = weather(phonenumber, smtpserver, coords)
    weather.getweather()
    weather.message = weather.afternoonweather
    weather.subject = "WeatherBot"
    weather.sendmessage()