#!/usr/bin/env python
from appbase import AppBase
import requests
import datetime
from rgbmatrix import graphics
import time
from teams import teams

class Scoreboard(AppBase):
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
    font.LoadFont("./fonts/4x6.bdf")
    textColor = graphics.Color(255, 255, 255)
    x_pos = 1
    y_pos = 5


    games = self.data['games']

    for game in games:
    
      # Teams & Scores
      winning_team = game['game']['winning_team']['name']
      winning_team_runs = game['game']['winning_team']['runs']
      losing_team = game['game']['losing_team']['name']
      losing_team_runs = game['game']['losing_team']['runs']

      # Pitchers
      winning_pitcher = game['game']['winning_team']['winning_pitcher']['name']
      winning_pitcher_record_object = game['game']['winning_team']['winning_pitcher']['record']
      # winning_pitcher_record = "(" + str(winning_pitcher_record_object['wins']) + '-' + str(winning_pitcher_record_object['losses']) + ")"

      losing_pitcher = game['game']['losing_team']['losing_pitcher']['name']
      losing_pitcher_record_object = game['game']['losing_team']['losing_pitcher']['record']
      # losing_pitcher_record = "(" + str(losing_pitcher_record_object['wins']) + '-' + str(losing_pitcher_record_object['losses']) + ")"

      save_pitcher = game['game']['winning_team']['save_pitcher']['name']
      
      if save_pitcher != '':
        save_pitcher_saves = str(game['game']['winning_team']['save_pitcher']['saves'])

      if winning_team == game['game']['played_at']['home_team']:
        home_team = winning_team
        away_team = losing_team
        home_team_runs = winning_team_runs
        away_team_runs = losing_team_runs
      else:
        home_team = losing_team
        away_team = winning_team
        home_team_runs = losing_team_runs
        away_team_runs = winning_team_runs

      # Team colors
      home_red_val = teams[home_team]['color']['red']
      home_green_val = teams[home_team]['color']['green']
      home_blue_val = teams[home_team]['color']['blue']

      away_red_val = teams[away_team]['color']['red']
      away_green_val = teams[away_team]['color']['green']
      away_blue_val = teams[away_team]['color']['blue']        

      # Formatting strings for display
      away_team_formatted = teams[away_team]['short_name'] + " " + teams[away_team]['name']
      home_team_formatted = teams[home_team]['short_name'] + " " + teams[home_team]['name']

      win_length = len(winning_pitcher)
      lose_length = len(losing_pitcher)
      save_length = len(save_pitcher)

      winning_pitcher_formatted = "W " + winning_pitcher[slice(0,1)] + ". " + winning_pitcher[slice(winning_pitcher.index(' ') + 1, win_length)]
      losing_pitcher_formatted = "L " + losing_pitcher[slice(0,1)] + ". " + losing_pitcher[slice(losing_pitcher.index(' ') + 1, lose_length)]
      
      if save_pitcher != "":
        save_pitcher_formatted = "S " + save_pitcher[slice(0,1)] + ". " + save_pitcher[slice(save_pitcher.index(' ') + 1, save_length)] 

      timeout = 0
      
      while timeout < (15 / 0.05): 
        offscreen_canvas.Clear()

        # Print color for away team
        for pixel_y in range(9):
          for pixel_x in range(self.matrix.width):
            offscreen_canvas.SetPixel(pixel_x, pixel_y, away_red_val, away_green_val, away_blue_val)

        # Print color for home team
        for pixel_y in range(9,18):
          for pixel_x in range(self.matrix.width):
            offscreen_canvas.SetPixel(pixel_x, pixel_y, home_red_val, home_green_val, home_blue_val)
          
        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 2, textColor, away_team_formatted)                                              
        graphics.DrawText(offscreen_canvas, font, ( offscreen_canvas.width - ( len(str(away_team_runs)) * 4 + 1 ) ), y_pos + 2, textColor, str(away_team_runs))
        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 11, textColor, home_team_formatted)                                              
        graphics.DrawText(offscreen_canvas, font, ( offscreen_canvas.width - ( len(str(home_team_runs)) * 4 + 1 ) ), y_pos + 11, textColor, str(home_team_runs))

        # graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 21, textColor, "Pitching:")
        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 28, textColor, winning_pitcher_formatted)
        graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 35, textColor, losing_pitcher_formatted)

        if save_pitcher != '':
                graphics.DrawText(offscreen_canvas, font, x_pos, y_pos + 42, textColor, save_pitcher_formatted)
        
        time.sleep(0.05)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
        timeout += 0.5

    self.run()

# Main function
if __name__ == "__main__":
  scoreboard = Scoreboard()
  if (not scoreboard.process()):
      scoreboard.print_help()

