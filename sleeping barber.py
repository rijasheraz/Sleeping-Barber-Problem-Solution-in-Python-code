# Sleeping-Barber-Problem-Solution-in-Python
from tkinter import *
from tkinter.ttk import Progressbar, Style
import tkinter as tk
from tkinter import messagebox
from threading import Semaphore, Condition
from tkinter import scrolledtext
from tkinter import Tk, Label, Canvas, Button, PhotoImage
import threading
import time
import queue
import random

NUM_CHAIRS = 4


class Sleeping_Barber:
    def __init__(self):
        self.window = Tk()
        self.window.title("Sleeping Barber Shop")
        self.window.geometry("950x600")
        self.center_window()
        self.image_filename = '/home/operating/Downloads/project.png'
        self.create_widgets()

    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def create_widgets(self):
        c = Canvas(self.window, bg="white", height=440, width=1000)
        c.pack()

        filename = PhotoImage(file=self.image_filename)
        filename = filename.zoom(1)
        background_label = Label(self.window, bg="white", image=filename)
        background_label.image = filename  # Store a reference to the image
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        filename = filename.zoom(1)
        #filename = filename.subsample(1)

        background_label = Label(self.window, bg="white", image=filename)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        frame = Frame(self.window)
        frame.pack(side='bottom', pady=20)
        frame.configure(bg="white")  # Set the background color of the Frame to white

        style = Style()
        style.configure("TProgressbar", bg="white")

        load = Progressbar(frame, orient=HORIZONTAL, length=500, mode='determinate', style="TProgressbar")
        load.pack(pady=10)

        load_label = Label(frame, text="", bg="white")
        load_label.pack(pady=5)

        start_button = Button(frame, text="Start", command=lambda: self.start_loading(load, load_label, frame), bg="black", fg="white")
        start_button.pack(pady=10)
        start_button.configure(bg="white", fg="black")

        self.window.mainloop()

    def start_loading(self, load, load_label, frame):
        def update():
            nonlocal i
            if i <= 10:  
                txt = "Please wait..." + str(10 * i) + "%"
                load.config(value=10 * i)  
                load_label.config(text=txt)  
                self.window.after(800, update)
                i += 1    
            else:
                self.window.withdraw()  # Hide the main window
                self.start_barber_simulation()

        i = 0    
        update()

    def start_barber_simulation(self):
        barber_window = Toplevel(self.window)
        app = BarberShopSimulator(barber_window, self)  # Pass a reference to Sleeping_Barber

class EndPage:
    def __init__(self):
        self.window = None    

    def show_page(self):
        self.window = Tk()    
        self.window.title("Sleeping Barber Shop ")
        self.window.geometry("900x670")
        self.window.configure(bg="cadetblue")  # Set the background color of the window 
        self.center_window()
        
    def center_window(self):
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        
        # Use a custom font for the heading
        heading_font = ("Times New Roman", 24, "bold")
        label = Label(self.window, text="No customer remain \n Barber is going to sleep ...zzzzz \n \n\n\n\n\nShop is Closed!!!", bg='cadetblue', font=heading_font)
        label.place(x=240,y=90)
        
        frame = Frame(self.window)
        frame.pack(side='bottom', pady=20)
        frame.configure(bg="cadetblue")  # Set the background color of the Frame to white

        exit_button = Button(self.window, text="Exit", command=self.window.destroy,height=2, width=9)
        exit_button.place(x=400, y=430)

        self.window.mainloop()




        
class BarberShopSimulator:
    def __init__(self, master, sleeping_barber):
        self.master = master
        self.sleeping_barber = sleeping_barber  # Store the reference
        self.master.title("Sleeping Barber shop")
        self.master.geometry("920x680")
        self.master.configure(bg="white")  # Set the background color of the window to white
        
        # Add a heading label
        heading_label = tk.Label(self.master, text="Welcome In Barber Shop", font=("Georgia", 25,"bold"), pady=10, bg="white")
        heading_label.place(x=260, y=25)
         
        self.sem_waiting_room = threading.Semaphore(value=NUM_CHAIRS)
        self.mutex_barber_chair = threading.Lock()
        self.cond_customer_arrived = threading.Condition(self.mutex_barber_chair)
        self.barber_sleeping = Semaphore(1)  # Set initial state to awake
        self.customer_queue = queue.Queue()
        self.barber_thread = threading.Thread(target=self.barber_procedure)
        self.barber_thread.start()
         

        self.start_simulation_button = tk.Button(self.master, text="Start", command=self.start_simulation, bg="white", fg="black")
        self.start_simulation_button.place(x=450 , y=130)

        self.text_widget = scrolledtext.ScrolledText(self.master, width=65, height=25, bg="lightgrey")
        self.text_widget.place(x=210,y= 190)
        
        self.center_window()

    def center_window(self):
        self.master.update_idletasks()
        width = self.master.winfo_width()
        height = self.master.winfo_height()
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.master.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def start_simulation(self):
        for i in range(10):
            customer_thread = threading.Thread(target=self.customer_arrival, args=(i,))
            customer_thread.start()
            time.sleep(random.uniform(0.5, 0.2))

    def customer_arrival(self, customer_id):
        with self.mutex_barber_chair:
            if NUM_CHAIRS >= customer_id:  # Compare with the number of chairs
                if self.sem_waiting_room.acquire(blocking=False):
                    self.customer_queue.put(customer_id)
                    self.cond_customer_arrived.notify()
                    self.sem_waiting_room.release()

    def barber_procedure(self):
        while True:
            with self.mutex_barber_chair:
                while self.customer_queue.empty():
                    if not self.barber_sleeping:  
                        self.text_widget.insert(tk.END, "Barber is going to sleep\n")
                        self.barber_sleeping = True      
                        self.text_widget.yview(tk.END)
                        time.sleep(random.uniform(1, 3))  # Simulate barber going to sleep
                        self.check_simulation_complete()

                    self.cond_customer_arrived.wait()

                self.barber_sleeping = False      
                customer_id = self.customer_queue.get()  
                output = f"Barber is cutting hair for Customer {customer_id}\n"
                self.text_widget.insert(tk.END, output)
                self.text_widget.yview(tk.END)    
                time.sleep(random.uniform(1, 4))  

                if self.customer_queue.empty():
                    self.check_simulation_complete()
  
    def check_simulation_complete(self):
        self.text_widget.insert(tk.END, "Barber is going to sleep\n")  
        self.text_widget.yview(tk.END)  
        time.sleep(random.uniform(1, 3))  # Simulate barber going to sleep
        answer = messagebox.askquestion("Cutting is  Finished",
                                         "All customers served. Do you want to again cutting ?")
        if answer == 'yes':
            self.start_simulation()
        else:
            self.show_next_page_func_no()

    def show_next_page_func_no(self):
	    self.master.destroy()  # Destroy the current window
	    # Create an instance of the NextPage class and show the page
	    next_page = EndPage()
	    next_page.show_page()

if __name__ == "__main__":                
    app = Sleeping_Barber()          
    app.window.mainloop()
    app.EndPage()

 
     
 
