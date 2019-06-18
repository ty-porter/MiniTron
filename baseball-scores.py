#!/usr/bin/env python
import requests
import datetime

class Scoreboard():
	def __init__(self):
		self.getData()

	def getData(self):
		date = datetime.datetime.now()
		DATE = str(date.month) + "/" + str(date.day - 1) + "/" + str(date.year)
		URL = "https://mlb-api-server.herokuapp.com/api/games/" + DATE

		r = requests.get(URL)
		data = r.json()

		print(data)

# Main function
if __name__ == "__main__":
    scoreboard = Scoreboard()
	
