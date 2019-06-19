#!/usr/bin/env python
from samplebase import SampleBase
import requests
import datetime
from rgbmatrix import graphics
import time

class Scoreboard(SampleBase):
        def __init__(self, *args, **kwargs):
                super(Scoreboard, self).__init__(*args, **kwargs)
                self.getData()

        # Get yesterday's date, and make a GET request to server, then parse results.
        def getData(self):
                date = datetime.datetime.now()
                DATE = str(date.month) + "/" + str(date.day - 1) + "/" + str(date.year)
                URL = "https://mlb-api-server.herokuapp.com/api/games/" + DATE

                r = requests.get(URL)
                self.data = r.json()
                

        def run(self):
                offscreen_canvas = self.matrix.CreateFrameCanvas()
                font = graphics.Font()
                font.LoadFont("../../../fonts/4x6.bdf")
                textColor = graphics.Color(255, 255, 255)
                pos = offscreen_canvas.width
                my_text = self.data['games'][0]['game']['winning_team']['name']              

                while True:
                        offscreen_canvas.Clear()
                        len = graphics.DrawText(offscreen_canvas, font, pos, 35, textColor, my_text)
                        pos -= 1
                        if (pos + len < 0):
                                        pos = offscreen_canvas.width

                        time.sleep(0.05)
                        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
    scoreboard = Scoreboard()
    if (not scoreboard.process()):
        scoreboard.print_help()
	
