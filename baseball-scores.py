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
                x_pos = 0
                y_pos = 5

                # Teams & Scores
                winning_team = self.data['games'][0]['game']['winning_team']['name']
                winning_team_runs = self.data['games'][0]['game']['winning_team']['runs']
                losing_team = self.data['games'][0]['game']['losing_team']['name']
                losing_team_runs = self.data['games'][0]['game']['losing_team']['runs']

                # Pitchers
                winning_pitcher = self.data['games'][0]['game']['winning_team']['winning_pitcher']['name']
                winning_pitcher_record_object = self.data['games'][0]['game']['winning_team']['winning_pitcher']['record']
                winning_pitcher_record = str(winning_pitcher_record_object['wins']) + ' - ' + str(winning_pitcher_record_object['losses'])

                losing_pitcher = self.data['games'][0]['game']['losing_team']['losing_pitcher']['name']
                losing_pitcher_record_object = self.data['games'][0]['game']['losing_team']['losing_pitcher']['record']
                losing_pitcher_record = str(losing_pitcher_record_object['wins']) + ' - ' + str(losing_pitcher_record_object['losses'])

                while True:
                        offscreen_canvas.Clear()
                        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos, textColor, winning_team)                                              
                        graphics.DrawText(offscreen_canvas, font, ( offscreen_canvas.width - ( len(str(winning_team_runs)) * 4 ) ), y_pos, textColor, str(winning_team_runs))
                        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 7, textColor, losing_team)                                              
                        graphics.DrawText(offscreen_canvas, font, ( offscreen_canvas.width - ( len(str(winning_team_runs)) * 4 ) ), y_pos + 7, textColor, str(losing_team_runs))

                        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 21, textColor, "Pitching:")
                        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 28, textColor, "W " + winning_pitcher + winning_pitcher_record)
                        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 35, textColor, "L " + losing_pitcher + losing_pitcher_record)
                        
                        time.sleep(0.05)
                        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

# Main function
if __name__ == "__main__":
    scoreboard = Scoreboard()
    if (not scoreboard.process()):
        scoreboard.print_help()
	
