#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import time
from subway_example import filter_trains_next_two, get_upcoming_trains
from datetime import datetime

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
            graphics.DrawText(offscreen_canvas, font_small, 0, 10, textColor, "TRAINS:")
            graphics.DrawText(offscreen_canvas, font_large, 0, 20, textColor, "{} MIN".format(train_times[0]))
            graphics.DrawText(offscreen_canvas, font_large, 0, 30, textColor, "{} MIN".format(train_times[1]))
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

            current_hour = datetime.now().hour
            if (current_hour >= 6 and current_hour < 10):
                time.sleep(30)
            elif (current_hour >= 10 and current_hour < 20):
                time.sleep(90)
            else:
                time.sleep(120)

if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()