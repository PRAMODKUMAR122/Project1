import tkinter as tk
import math
import random
from threading import Thread
import time

class UAV:
    def __init__(self, canvas, x, y, title):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.title = title
        self.obj = self.canvas.create_oval(x, y, x + 40, y + 40, fill="blue")
        self.label = self.canvas.create_text(x + 20, y - 10, fill="darkblue", font="Times 7 italic bold", text=title)

    def move(self):
        while True:
            if not self.canvas.simulation_running:
                break
            if 450 <= self.y <= 600:
                self.y += 10
            else:
                self.y = 450
            self.canvas.move(self.obj, 0, 10)
            self.canvas.move(self.label, 0, 10)
            time.sleep(1)

class IoTDevice:
    def __init__(self, canvas, x, y, id):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.id = id
        self.obj = self.canvas.create_oval(x, y, x + 40, y + 40, fill="red")
        self.label = self.canvas.create_text(x + 20, y - 10, fill="darkblue", font="Times 8 italic bold", text="IoT" + str(id))

class SimulationCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.simulation_running = False

    def start_simulation(self):
        self.simulation_running = True

    def stop_simulation(self):
        self.simulation_running = False

class Simulation:
    def __init__(self, canvas):
        self.canvas = canvas
        self.uavs = []
        self.iot_devices = []

    def generate_iot_devices(self, num_devices):
        for i in range(3, num_devices):
            x = random.randint(100, 450)
            y = random.randint(50, 600)
            if not self.is_too_close(x, y):
                self.iot_devices.append(IoTDevice(self.canvas, x, y, i))

    def is_too_close(self, x, y):
        for iot in self.iot_devices:
            dist = math.sqrt((iot.x - x) ** 2 + (iot.y - y) ** 2)
            if dist < 60:
                return True
        return False

    def start_simulation(self):
        self.canvas.start_simulation()
        for i in range(3):
            self.uavs.append(UAV(self.canvas, 5, 650 - i * 200, f"UAV{i + 1}"))
            Thread(target=self.uavs[i].move, daemon=True).start()

    def task_offloading(self, src):
        if not self.canvas.simulation_running:
            return
        temp = self.iot_devices[src]
        src_x, src_y = temp.x, temp.y
        distances = [(uav, math.sqrt((uav.x - src_x) ** 2 + (uav.y - src_y) ** 2)) for uav in self.uavs]
        distances.sort(key=lambda x: x[1])
        selected_uavs = [dist[0] for dist in distances[:2]]
        for uav in selected_uavs:
            self.canvas.create_line(src_x + 20, src_y + 20, 25, uav.y + 20, fill='black', width=3)

def main():
    root = tk.Tk()
    root.geometry("1300x1200")
    root.title("UAV-IoT Simulation")
    root.resizable(True, True)

    canvas = SimulationCanvas(root, width=800, height=700)
    canvas.pack()

    simulation = Simulation(canvas)

    l2 = tk.Label(root, text='Num IoT:')
    l2.config(font=('times', 12, 'bold'))
    l2.place(x=820, y=10)
    tf1 = tk.Entry(root, width=10)
    tf1.config(font=('times', 12, 'bold'))
    tf1.place(x=970, y=10)
    l1 = tk.Label(root, text='IoT ID:')
    l1.config(font=('times', 12, 'bold'))
    l1.place(x=820, y=60)
    mobile_list = tk.Listbox(root)
    mobile_list.place(x=970, y=60)
    mobile_list.config(font=('times', 12, 'bold'))
    for i in range(3, 100):
        mobile_list.insert(tk.END, str(i))
    mobile_list.select_set(0)
    createButton = tk.Button(root, text="Generate IoT Network", command=lambda: simulation.generate_iot_devices(int(tf1.get().strip())))
    createButton.place(x=820, y=110)
    createButton.config(font=('times', 12, 'bold'))
    offloadButton = tk.Button(root, text="IoT Task Offloading", command=lambda: simulation.task_offloading(int(mobile_list.curselection()[0]) + 3))
    offloadButton.place(x=820, y=160)
    offloadButton.config(font=('times', 12, 'bold'))
    startButton = tk.Button(root, text="Start Simulation", command=simulation.start_simulation)
    startButton.place(x=820, y=210)
    startButton.config(font=('times', 12, 'bold'))
    stopButton = tk.Button(root, text="Stop Simulation", command=canvas.stop_simulation)
    stopButton.place(x=820, y=260)
    stopButton.config(font=('times', 12, 'bold'))
    exitButton = tk.Button(root, text="Exit", command=root.destroy)
    exitButton.place(x=820, y=310)
    exitButton.config(font=('times', 12, 'bold'))

    root.mainloop()
if __name__ == "__main__":
    main()
