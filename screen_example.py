#!/usr/bin/env python

from samplebase import SampleBase
from rgbmatrix import graphics
import time

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def run(self):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("/home/aryeh/rpi-rgb-led-matrix/fonts/10x20.bdf")
        textColor = graphics.Color(191,105,48)
        pos = offscreen_canvas.width
        text = "Train times:"

        offscreen_canvas.Clear()
        len = graphics.DrawText(offscreen_canvas, font, 0, 20, textColor, text)
        offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

        while True:
            # pos -= 1
            # if (pos + len < 0):
            #     pos = offscreen_canvas.width

            # time.sleep(0.05)
            # offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            pass

if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()