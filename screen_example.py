#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import time
from subway_example import filter_trains_next_two, get_upcoming_trains
from datetime import datetime

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font_large = graphics.Font()
        font_large.LoadFont("/home/aryeh/rpi-rgb-led-matrix/fonts/7x13.bdf")
        font_small = graphics.Font()
        font_small.LoadFont("/home/aryeh/rpi-rgb-led-matrix/fonts/5x8.bdf")
        textColor = graphics.Color(52,85,235)

        while True:
            train_times = filter_trains_next_two(get_upcoming_trains())
            
            offscreen_canvas.Clear()
            graphics.DrawText(offscreen_canvas, font_large, 0, 10, textColor, "Train times:")
            graphics.DrawText(offscreen_canvas, font_small, 0, 25, textColor, "1. {} minutes".format(train_times[0]))
            graphics.DrawText(offscreen_canvas, font_small, 0, 40, textColor, "2. {} minutes".format(train_times[1]))
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

            current_hour = datetime.now().hour
            if (current_hour > 6 and current_hour < 21):
                time.sleep(90)
            else:
                time.sleep(60*30)

if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()