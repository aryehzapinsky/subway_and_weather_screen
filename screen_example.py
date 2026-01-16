#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import time
from subway_example import filter_trains_next_two, get_upcoming_trains
from weather_example import get_weather
from datetime import datetime

PATH_NAME = "tmp_weather.json"

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    """
    10x20.bdf  5x8.bdf   6x13.bdf   6x9.bdf    7x13O.bdf  8x13.bdf   9x15.bdf   9x18B.bdf  README.md    texgyre-27.bdf
    4x6.bdf    6x10.bdf  6x13B.bdf  7x13.bdf   7x14.bdf   8x13B.bdf  9x15B.bdf  AUTHORS    clR6x12.bdf  tom-thumb.bdf
    5x7.bdf    6x12.bdf  6x13O.bdf  7x13B.bdf  7x14B.bdf  8x13O.bdf  9x18.bdf   README     helvR12.bdf
    """
    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font_large = graphics.Font()
        font_large.LoadFont("/home/aryeh/rpi-rgb-led-matrix/fonts/6x10.bdf")
        font_small = graphics.Font()
        font_small.LoadFont("/home/aryeh/rpi-rgb-led-matrix/fonts/5x8.bdf")
        textColor = graphics.Color(207,207,207)
        

        while True:
            train_times = filter_trains_next_two(get_upcoming_trains())
            
            offscreen_canvas.Clear()
            if (train_times[0] is not None):
                graphics.DrawText(offscreen_canvas, font_large, 1, 10, textColor, "{} MIN".format(train_times[0]))
            if (train_times[1] is not None):
                graphics.DrawText(offscreen_canvas, font_large, 1, 20, textColor, "{} MIN".format(train_times[1]))

            # weather - now
            weather = get_weather(PATH_NAME)
            current_temperature = weather.get('current_temperature')
            if current_temperature:
                graphics.DrawText(offscreen_canvas, font_large, 1, 40, textColor, "{} F".format(current_temperature))
            
            high = weather.get('high')
            low = weather.get('low')
            if (high and low):
                graphics.DrawText(offscreen_canvas, font_large, 1, 50, textColor, "L:{} H:{}".format(low, high))

            percipitation_time = weather.get('percipitation_time')
            if percipitation_time:
                rain_or_snow = "rain" if weather.get('rain') else "snow"
                # Show rain in 12 hour format with AM or PM
                graphics.DrawText(offscreen_canvas, font_large, 1, 60, textColor, "{}:{}".format(
                    rain_or_snow,
                    percipitation_time.strftime("%-I %p")))

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

            # Update more frequently when commuting or awake. 
            current_hour = datetime.now().hour
            if (current_hour >= 6 and current_hour < 10):
                time.sleep(30)
            elif (current_hour >= 10 and current_hour < 20):
                time.sleep(90)
            else:
                time.sleep(120)

# image = Image.open(image_file)

# # Configuration for the matrix
# options = RGBMatrixOptions()
# options.rows = 32
# options.chain_length = 1
# options.parallel = 1
# options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

# matrix = RGBMatrix(options = options)

# # Make image fit our screen.
# image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)

# matrix.SetImage(image.convert('RGB'))

def main():
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()

if __name__ == "__main__":
    while True:
        try:
            main()
        except:
            continue