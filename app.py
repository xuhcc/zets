import tkinter as tk
import tkinter.ttk as ttk
import threading
import queue
import time

import gradient
import generator

class Worker(threading.Thread):

    def __init__(self, queue, mode, gen_params):
        """
        Accepts:
            queue: Queue object
            mode: set type
            gen_params: parameters for generator function
        """
        threading.Thread.__init__(self, daemon=True)
        self.queue = queue
        if mode == "julia":
            self.gen = generator.julia2(**gen_params)
        elif mode == "mandelbrot":
            self.gen = generator.mandelbrot(**gen_params)
        else:
            self.gen = []

    def run(self):
        for item in self.gen:
            self.queue.put(item)

class Application(object):

    def __init__(self, width=800, height=600, mode="julia", **kwargs):
        # Prepare window and elements
        self.root = tk.Tk()
        self.root.title(mode)
        self.root.geometry("{w}x{h}+{ox}+{oy}".format(
            w=width + 2,
            h=height + 2 + 20,
            ox=100,
            oy=50))
        self.canvas = tk.Canvas(
            self.root,
            width=width,
            height=height,
            bd=0,
            bg="#eee")
        self.canvas.bind("<Button-1>", lambda e: self.quit())
        self.canvas.pack()
        self.image = tk.PhotoImage(width=width, height=height)
        self.pgbar = tk.ttk.Progressbar(
            self.root,
            orient="horizontal",
            mode="determinate",
            length=width,
            maximum=height)
        self.pgbar.pack()
        # Collect parameters for generator
        self.gen_params = kwargs
        self.gen_params['size_x'] = width
        self.gen_params['size_y'] = height
        # Set up worker
        self.queue = queue.Queue()
        self.worker = Worker(self.queue, mode, self.gen_params)

    def periodic_call(self):
        while self.queue.qsize():
            # Retrieve item from queue and put on the image
            try:
                y, line = self.queue.get()
                self.image.put(line, to=(0, y))
                self.pgbar.step(1)
            except queue.Empty:
                pass
        if self.worker.is_alive():
            # Repeat
            self.root.after(100, self.periodic_call)
        else:
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)
            print("Image created in {0} sec".format(time.time() - self.start_time))

    def start(self):
        self.start_time = time.time()
        self.worker.start()
        self.root.after(100, self.periodic_call)
        self.root.mainloop()

    def quit(self):
        self.root.destroy()


def main():
    app = Application(
        mode="julia", width=900, height=900, maxiter=250)
    app.start()

if __name__ == "__main__":
    main()
