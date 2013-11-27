import tkinter as tk
import gradient
import julia
import threading
import queue

class Worker(threading.Thread):

    def __init__(self, queue, *gargs):
        """
        Accepts:
            queue: Queue object
            gargs: arguments for map generating function
        """
        threading.Thread.__init__(self)
        self.queue = queue
        self.gargs = gargs

    def run(self):
        for item in julia.generate_map(*self.gargs):
            self.queue.put(item)

class Window(object):

    def __init__(self, size_x, size_y, func, maxiter, scale):
        self.size_x = size_x
        self.size_y = size_y
        self.func = func
        self.maxiter = maxiter
        self.scale = scale
        self.colors = gradient.generate_gradient(
            "#E1FFA2",
            "#470063",
            self.maxiter)
        self.root = tk.Tk()
        self.root.title("Julia")
        self.root.geometry("{0}x{1}+200+150".format(size_x + 2, size_y + 2))
        self.root.overrideredirect(True)
        self.canvas = tk.Canvas(
            self.root,
            width=self.size_x,
            height=self.size_y,
            bd=2,
            bg=self.colors[0])
        self.canvas.bind("<Button-1>", lambda e: self.quit())
        self.canvas.pack()

    def draw_set_p(self):
        """
        Draw set using PhotoImage
        """
        ju = julia.generate_set(
            self.func, self.size_x, self.size_y, self.scale, self.maxiter)
        self.image = tk.PhotoImage(width=self.size_x, height=self.size_y)
        for x, y, i in ju:
            if i > 0:
                self.image.put(self.colors[i], (x, y))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def draw_set_pp(self):
        """
        Draw set using PhotoImage, alternative method
        """
        ju = julia.generate_map(
            self.func,
            self.size_x, self.size_y, self.scale,
            self.maxiter, self.colors)
        self.image = tk.PhotoImage(width=self.size_x, height=self.size_y)
        for y, line in ju:
            self.image.put(line, to=(0, y))
        self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def draw_set_l(self):
        """
        Draw set using lines
        """
        ju = julia.generate_set(
            self.func, self.size_x, self.size_y, self.scale, self.maxiter)
        for x, y, i in ju:
            if i > 0:
                self.canvas.create_line(
                    x, y, x + 1, y + 1, fill=self.colors[i], width=1)
        
    def start(self):
        self.root.after(100, self.draw_set_pp)
        self.root.mainloop()

    def periodic_call(self):
        while self.queue.qsize():
            # Retrieve item from queue and put on the image
            try:
                y, line = self.queue.get()
                self.image.put(line, to=(0, y))
            except queue.Empty:
                pass
        if self.worker.is_alive():
            # Repeat
            self.root.after(100, self.periodic_call)
        else:
            self.canvas.create_image(0, 0, image=self.image, anchor=tk.NW)

    def start_threaded(self):
        self.queue = queue.Queue()
        self.worker = Worker(self.queue,
            self.func, self.size_x, self.size_y, self.scale, self.maxiter, self.colors)
        self.image = tk.PhotoImage(width=self.size_x, height=self.size_y)
        self.worker.start()
        self.root.after(100, self.periodic_call)
        self.root.mainloop()

    def quit(self):
        self.root.destroy()


def main():
    func = lambda z: z ** 2 - 0.4 + 0.6j
    app = Window(1000, 800, func, 100, 250)
    app.start_threaded()

if __name__ == "__main__":
    main()
