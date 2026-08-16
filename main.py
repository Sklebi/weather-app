import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter Da City", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.initUI()
    def initUI(self):
        self.setWindowTitle("The Sklebi Weather App!!")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)
        self.setWindowIcon(QIcon("icon.png"))

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            WeatherApp{

                background-color: #5f8ed9;
                min-height: 500px;
                
            }
            QLabel {
                font-family: "Cascadia Code";
                color: white;
            }


            QLabel#city_label {
                font-size: 40px;
                font-family: "Cascadia Code";
                color: white;
            }
            QLineEdit#city_input{
                font-size: 40px;
                font-family: "Cascadia Code";
                background-color: #4e7cc7;
                color: white; 
                border: 3px solid #4f74b0;
                
            }
            QPushButton#get_weather_button{
                font-size: 30px; 
                font-family: "Cascadia Code";
                background-color: #7faffa;
                color: white;
                border: 3px solid #4f74b0;
                min-height: 25px;
                padding:10px 20px;  
            } 

            QPushButton#get_weather_button:hover {
                background-color: #9ec4ff;
                border: 3px solid #7faffa;
                
            }
            QPushButton#get_weather_button:pressed {
                background-color: #4e7cc7;
                padding-top: 4px;
                padding-left: 4px;
            
            }
            QLabel#temperature_label{
                color: white;
                font-size: 75px;
                font-family: UMTypeWriter;
            }
            QLabel#emoji_label{
            font-size: 100px; 
            font-family: "Segoe UI emoji";
            
            
            }
            QLabel#description_label{
            font-size: 50px;
            color: white;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "f982ed8c20a7fae189a0c7aa4a7e50a7"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data["cod"] == 200:
                self.display_weather(data)

        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request:\nPlease check your input")
                case 401: 
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403: 
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not Found:\nCity not found")
                case 500: 
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503: 
                    self.display_error("Service Unavaliable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _: 
                    self.display_error(f"HTTP error occured:\n{http_error}")


        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

        except requests.exceptions.RequestException:
            pass


    def display_error(self,message):
        self.temperature_label.setStyleSheet("font-size:30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def display_weather(self,data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temperature_k = data["main"]["temp"]
        temperature_f = (temperature_k - 273.15) * (9/5) + 32
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_f:.0f}°F")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description) 

    @staticmethod
    def get_weather_emoji(weather_id):
        if weather_id >= 200 and weather_id <=232: 
            return "⛈️"
        elif 300 <= weather_id <= 321: 
            return "⛅"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <=622:
            return "❄️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771: 
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 801 <= weather_id <= 804:
            return "⛅"
        else:
            return ""




if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())