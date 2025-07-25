import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLabel,QLineEdit,QPushButton,QVBoxLayout)
from PyQt5.QtCore import Qt

class Weather_app(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label=QLabel("Enter city name :",self)
        self.city_input=QLineEdit(self)
        self.get_weather_button=QPushButton("Get Weather",self)
        self.temperature_label=QLabel(self)
        self.emoji_label=QLabel(self)
        self.description_label=QLabel(self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("Weather App")
        xbox=QVBoxLayout()
        xbox.addWidget(self.city_label)
        xbox.addWidget(self.city_input)
        xbox.addWidget(self.get_weather_button)
        xbox.addWidget(self.temperature_label)
        xbox.addWidget(self.emoji_label)
        xbox.addWidget(self.description_label)

        self.setLayout(xbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;       
                           }
            QLabel#city_label{
                           font-size: 40px;
                           font-style: italic;
                           }
            QLineEdit#city_input{
                           font-size: 40px;
                           }
            QPushButton#get_weather_button{
                           font-size: 30px;
                           font-weight: bold;
                           }
            QLabel#temperature_label {
                           font-size: 70px;
                           }
            QLabel#emoji_label {
                           font-size: 100px;
                           font-family: Segoe UI emoji;
                           }
            QLabel#description_label {
                           font-size: 50px;
                           }
        """)
        self.get_weather_button.clicked.connect(self.get_weather)
    
    def get_weather(self):
        
        api_key="ea7147dd59c46c81014025274e37fcf6"
        city=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        try:
            res=requests.get(url)
            res.raise_for_status()
            data=res.json()
            if data["cod"]==200:
                self.display_weather(data)
        except requests.exceptions.HTTPError as http_error:
            match res.status_code:
                case 400:
                    self.display_error("Bad Request: Invalid or missing parameters.")
                case 401:
                    self.display_error("Unauthorized: Invalid or missing API key.")
                case 403:
                    self.display_error("Forbidden: Insufficient permissions for the API key.")
                case 404:
                    self.display_error("Not Found: Resource not found.")
                case 405:
                    self.display_error("Method Not Allowed: Wrong HTTP method used.")
                case 408:
                    self.display_error("Request Timeout: The request timed out.")
                case 409:
                    self.display_error("Conflict: Duplicate or conflicting request.")
                case 500:
                    self.display_error("Internal Server Error: Something went wrong on the server.")
                case 502:
                    self.display_error("Bad Gateway: Invalid response from upstream server.")
                case 503:
                    self.display_error("Service Unavailable: Server is temporarily down.")
                case 504:
                    self.display_error("Gateway Timeout: Server took too long to respond.")
                case _:
                    self.display_error(f"Unexpected Error: {http_error}")

                
        except requests.ConnectionError:
            self.display_error("Inernet error. \n Check your connection")

        except requests.Timeout:
            self.display_error("The request has timed out")

        except requests.TooManyRedirects:
            self.display_error("Too many redirects")

        except requests.exceptions.RequestException as re_error:
            self.display_error(f"Request error :{re_error}")

       
    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        temperature_k=data["main"]["temp"]
        temperature_c=temperature_k-273.15
        self.description_label.setStyleSheet("font-size: 35px;")
        self.temperature_label.setStyleSheet("font-size: 70;")
        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        weather_state=data["weather"][0]["description"]
        self.description_label.setText(f"{weather_state}")
        weather_id=data["weather"][0]["id"]
        self.emoji_label.setText(self.get_emoji(weather_id))

    @staticmethod
    def get_emoji(weather_id):
        if 200<=weather_id<=232:
            return "⛈️"
        elif 300<=weather_id<=321:
            return "🌥️"
        elif 500<=weather_id<=531:
            return "🌧️"
        elif 600<=weather_id<=622:
            return "☃️"
        elif 701<=weather_id<=741:
            return "🌫️"
        elif weather_id==762:
            return "🌋"
        elif weather_id==771:
            return "💨"
        elif weather_id==781:
            return "🌪️"
        elif weather_id==800:
            return "☀️"
        elif 801<=weather_id<=804:
            return "☁️"
        else:
            return ""

if __name__=="__main__":
    app=QApplication(sys.argv)
    weather_app=Weather_app()
    weather_app.show()
    sys.exit(app.exec_())
