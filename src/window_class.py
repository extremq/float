import tkinter as tk
import math
import random
import webbrowser

from tkinter.constants import ACTIVE, DISABLED

class gui():
    mw = None # main window
    mf = None # main frame
    lf = None # label frame
    cf = None # credit frame
    tf = None # tool frame
    vf = None # value frame
    
    btn_error, btn_coef = None, None
    
    cnt_input = None
    
    # The states of the tools
    state = {
        'coef': {
            'count': 0,
            'values': [["", ""] for x in range(200)],
            'entries': [[0, 0] for x in range(200)],
            'frame': None
        },
        'error': {
            'count': 0,
            'values': ["" for x in range(200)],
            'entries': [0 for x in range(200)],
            'frame': None
        }
    }
    
    tips = [
        "Poți trece de la o căsuță la alta apăsând Tab sau Shift + Tab.",
        "Programul suportă calcule cu numere arbitrar de mari.",
        "Când schimbi numărul de determinări nu pierzi datele introduse.",
        "Programul va lua în calcul doar determinările valide.",
        "Când schimbi tipul de calcul nu pierzi progresul.",
        "Ferestrele cu rezultate persistă și poți afișa mai multe calcule simultan."
    ]
    
    def __init__(self):
        self.setup()
    
    # Generating the 3 main frames and window
    def setup(self):
        self.mw = tk.Tk()
        
        self.mw.title('float')
        self.mw.geometry('400x600')
        self.mw.resizable(0, 0)
        
        self.mf = tk.Frame(master=self.mw, bg='#fff')
        self.mf.pack_propagate(0)
        self.mf.pack(fill=tk.BOTH, expand=1)
        
        self.lf, self.btn_error, self.btn_coef = self.init_labels(self.mf)
        
        self.tf = self.init_tool(self.mf)
        tk.Label(master=self.tf, text="Alege modul de lucru apăsând pe unul dintre butoanele de mai sus.", 
                 font="Arial 20", wraplength=300, bg="#fff").pack(pady=180)
        
        self.cf = self.init_credits(self.mf)
        
        self.mw.mainloop()
        
    # Top side of gui which contains the tool selector
    def init_labels(self, main_frame):
        # Frame for the buttons
        lf = tk.Frame(master=main_frame, height=30, bg='#fff')
        lf.pack_propagate(0)
        lf.pack(side=tk.TOP, fill=tk.X, padx=25, pady=15)
        
        # Error button
        btn_error = tk.Button(master=lf, text="Calcul erori", bg='#fff', fg="#000",
                              height=5, width=20, command=self.error_mode, cursor="hand2")
        btn_error.pack(side=tk.LEFT, padx=10)
        
        # Coefficient button
        btn_coef = tk.Button(master=lf, text="Calcul coeficienți", bg='#fff',
                             fg="#000", height=5, width=20, command=self.coef_mode, cursor="hand2")
        btn_coef.pack(side=tk.RIGHT, padx=10)
        
        return lf, btn_error, btn_coef
    
    # Bottom side of gui which contains credits
    def init_credits(self, main_frame):
        # Frame for the credits
        cf = tk.Frame(master=main_frame, height=30, bg='#fff')
        cf.pack_propagate(0)
        cf.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        credits = tk.Label(master=cf, text=f"{self.tips[random.randint(0, len(self.tips) - 1)]}\nRealizat de Extremq",
                           bg="#fff", fg='#1e2375', cursor="hand2")
        credits.pack(side=tk.BOTTOM)

        credits.bind("<Button-1>", lambda e: webbrowser.open_new_tab('https://extremq.github.io'))
        credits.bind("<Enter>", lambda e: self.change_color(credits, 'red'))
        credits.bind("<Leave>", lambda e: self.change_color(credits, '#1e2375'))

        return cf
    
    def change_color(self, credits, color, event=None):
        credits['fg'] = color

    # The middle, dynamic part which contains entries and such
    def init_tool(self, main_frame):
        tf = tk.Frame(master=main_frame, bg='#fff')
        tf.pack_propagate(0)
        tf.pack(fill=tk.BOTH, expand=1, padx=25)
        
        return tf
    
    # This will initialize the basic things needed to ask the user for the number of entries
    # as well as extra buttons for clearing and computing
    def init_count_entry(self, tool_frame, tool):
        cnt_label = tk.Label(master=tool_frame, text="Număr determinări (2 - 100):", bg="#fff")
        cnt_label.pack()
        
        self.cnt_input = tk.Entry(master=tool_frame)
        self.cnt_input.pack()
        
        # Error has different kinds of entries
        cnt_valid = tk.Button(master=tool_frame, text="Începe", cursor="hand2")
        cnt_valid.pack()
    
        # I really can't stress with the errors given by grids.
        # You will see that I am placing the entries by x and y coordinates
        # but I don't find it wrong per se, as this is a fixed size app (x-platform too).
        cnt_clear = tk.Button(master=tool_frame, text="Șterge valorile", cursor="hand2")
        cnt_clear.place(x=200, y=40)
        
        cnt_compute = tk.Button(master=tool_frame, text="Calculează", cursor="hand2")
        cnt_compute.place(x=83, y=40)

        if tool == 'error':
            cnt_valid['command'] = lambda: self.generate_error_entries(self.vf, self.cnt_input.get())
            cnt_clear['command'] = self.clear_error_values
            cnt_compute['command'] = self.compute_error
        else:
            cnt_label['text']  = "Număr determinări (2 - 25):"
            cnt_valid['command'] = lambda: self.generate_coef_entries(self.vf, self.cnt_input.get())
            cnt_clear['command'] = self.clear_coef_values
            cnt_compute['command'] = self.compute_coef
   

    def generate_coef_entries(self, value_frame, n):
        # Validation of size
        if not n.isnumeric() or (int(n) > 25 or int(n) < 2):
            self.cnt_input['bg'] = '#fa857d'
            return
        
        n = int(n)
        self.cnt_input['bg'] = '#a2fa7d'
            
        count = self.state['coef']['count']
        
        if n > count:
            start = count
            
            # Generate all the entries (or only the needed ones)
            for k in range(start, n):
                row = k
                
                self.state['coef']['entries'][k] = [
                    tk.Entry(master=value_frame, width=10),
                    tk.Entry(master=value_frame, width=10),
                ]

                if self.state['coef']['values'][k][0]:
                    self.state['coef']['entries'][k][0].insert(0, self.state['coef']['values'][k][0])

                if self.state['coef']['values'][k][1]:
                    self.state['coef']['entries'][k][1].insert(0, self.state['coef']['values'][k][1])

                self.state['coef']['entries'][k][0].place(y=15+row*15, x=80)
                self.state['coef']['entries'][k][1].place(y=15+row*15, x=180)
        elif n < count:
            start = n
            
            # Delete the extra entries only    
            for k in range(start, count):
                self.state['coef']['values'][k][0] = self.state['coef']['entries'][k][0].get()
                self.state['coef']['values'][k][1] = self.state['coef']['entries'][k][1].get()
                self.state['coef']['entries'][k][0].destroy()
                self.state['coef']['entries'][k][1].destroy()
        
        self.state['coef']['count'] = n

    def generate_error_entries(self, value_frame, n):
        # Validation of size
        if not n.isnumeric() or (int(n) > 100 or int(n) < 2):
            self.cnt_input['bg'] = '#fa857d'
            return
        
        n = int(n)
        self.cnt_input['bg'] = '#a2fa7d'
            
        count = self.state['error']['count']
        
        if n > count:
            start = count
            
            # Generate all the entries (or only the needed ones)
            for k in range(start, n):
                row = k // 4
                column = k % 4
                
                self.state['error']['entries'][k] = tk.Entry(master=value_frame,
                                                            width=10)
                if self.state['error']['values'][k]:
                    self.state['error']['entries'][k].insert(0, self.state['error']['values'][k])
                self.state['error']['entries'][k].place(y=15+row*15, x=13+column*80)
        elif n < count:
            start = n
            
            # Delete the extra entries only    
            for k in range(start, count):
                self.state['error']['values'][k] = self.state['error']['entries'][k].get()
                self.state['error']['entries'][k].destroy()
        
        self.state['error']['count'] = n
    
    def compute_error(self):
        sum_of_elements = 0
        sum_of_deltas = 0

        valid_elements = 0
        
        # Force an update
        self.store_errors()
        
        for k in range(self.state['error']['count']):
            value = self.state['error']['values'][k]
            if value is not None and self.isnumber(value):
                value = float(value)
                sum_of_elements += value
                valid_elements += 1
        
        if valid_elements < 2:
            return
        
        average_element = sum_of_elements / valid_elements
        
        for k in range(self.state['error']['count']):
            value = self.state['error']['values'][k]
            if value is not None and self.isnumber(value):
                value = float(value)
                sum_of_deltas += (average_element - value) ** 2
        
        average_delta = math.sqrt(sum_of_deltas / (valid_elements * (valid_elements - 1)))
        percent_delta = average_delta / average_element * 100
        
        popup = tk.Toplevel(master=self.mw)
        popup.title(f"Rezultat - {valid_elements} elemente.")
        popup.geometry("400x260")
        popup.resizable(0, 0)
        
        tk.Label(master=popup, text=f"Eroare absolută:\n {average_delta}\n\nValoare medie:\n {average_element}\n\nEroare relativă:\n {percent_delta}%",
                 font="Arial 20").pack()
            
    def compute_coef(self):
        sum_x = 0
        sum_y = 0
        sum_product = 0
        sum_x_square = 0

        valid_elements = 0

        # Force an update
        self.store_coef()

        for k in range(self.state['coef']['count']):
            x = self.state['coef']['values'][k][0]
            y = self.state['coef']['values'][k][1]
            if (x is not None and y is not None) and self.isnumber(x) and self.isnumber(y):
                x = float(x)
                y = float(y)
                sum_x += x
                sum_y += y
                sum_product += x * y
                sum_x_square += x ** 2
                valid_elements += 1
        
        if valid_elements < 2:
            return

        b = (valid_elements * sum_product - sum_x * sum_y) / (valid_elements * sum_x_square - sum_x ** 2)
        a = (sum_x_square * sum_y - sum_x * sum_product) / (valid_elements * sum_x_square - sum_x ** 2)

        
        popup = tk.Toplevel(master=self.mw)
        popup.title(f"Rezultat - {valid_elements} elemente.")
        popup.geometry("400x160")
        popup.resizable(0, 0)
        
        tk.Label(master=popup, text=f"b:\n {b}\n\na:\n {a}",
                 font="Arial 20").pack()

    # Since entries are different based on tool, I will split their functions
    def clear_error_values(self):
        for k in range(0, self.state['error']['count']):
                self.state['error']['values'][k] = None

                self.state['error']['entries'][k].destroy()
        self.state['error']['count'] = 0
    
    def clear_coef_values(self):
        for k in range(0, self.state['coef']['count']):
                self.state['coef']['values'][k][0] = None
                self.state['coef']['values'][k][1] = None

                self.state['coef']['entries'][k][0].destroy()
                self.state['coef']['entries'][k][1].destroy()
        self.state['coef']['count'] = 0

    # Same as recovering
    def recover_error_entries(self, value_frame):    
        for k in range(0, self.state['error']['count']):
                row = k // 4
                column = k % 4
                
                self.state['error']['entries'][k] = tk.Entry(master=value_frame,
                                                            width=10)
                self.state['error']['entries'][k].insert(0, self.state['error']['values'][k])
                self.state['error']['entries'][k].place(y=15+row*15, x=13+column*80)
        self.cnt_input.insert(0, self.state['error']['count'])

    def recover_coef_entries(self, value_frame):    
        for k in range(0, self.state['coef']['count']):
                row = k
                
                self.state['coef']['entries'][k] = [
                    tk.Entry(master=value_frame, width=10),
                    tk.Entry(master=value_frame, width=10),
                ]

                if self.state['coef']['values'][k][0]:
                    self.state['coef']['entries'][k][0].insert(0, self.state['coef']['values'][k][0])

                if self.state['coef']['values'][k][1]:
                    self.state['coef']['entries'][k][1].insert(0, self.state['coef']['values'][k][1])

                self.state['coef']['entries'][k][0].place(y=15+row*15, x=80)
                self.state['coef']['entries'][k][1].place(y=15+row*15, x=180)
        self.cnt_input.insert(0, self.state['coef']['count'])
    
    # When I switch between tools, I want to keep my data intact.
    def store_errors(self):
        for i in range(self.state['error']['count']):
            self.state['error']['values'][i] = self.state['error']['entries'][i].get()

    def store_coef(self):
        for i in range(self.state['coef']['count']):
            self.state['coef']['values'][i][0] = self.state['coef']['entries'][i][0].get()
            self.state['coef']['values'][i][1] = self.state['coef']['entries'][i][1].get()
    
    # Simple function to easily modify color and state of button
    def config_button(self, btn, state, bg, fg):
        btn['state'] = state
        btn['bg'] = bg
        btn['fg'] = fg
    
    def coef_mode(self):
        self.store_errors()
        
        self.config_button(self.btn_coef, DISABLED, "#1e2375", "#fff")
        self.config_button(self.btn_error, ACTIVE, "#fff", "#000")
        
        self.tf.destroy()
        self.tf = self.init_tool(self.mf)
        
        self.init_count_entry(self.tf, 'coef')
        
        value_frame = tk.Frame(master=self.tf, bg='#eee')
        value_frame.pack_propagate(0)
        value_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        
        self.vf = value_frame

        self.recover_coef_entries(self.vf)
        
    def error_mode(self):
        self.store_coef()

        self.config_button(self.btn_error, DISABLED, "#1e2375", "#fff")
        self.config_button(self.btn_coef, ACTIVE, "#fff", "#000")
        
        self.tf.destroy()
        self.tf = self.init_tool(self.mf)
        
        self.init_count_entry(self.tf, 'error')
        
        value_frame = tk.Frame(master=self.tf, bg='#eee')
        value_frame.pack_propagate(0)
        value_frame.pack(fill=tk.BOTH, expand=1, padx=10, pady=10)
        
        self.vf = value_frame
        
        self.recover_error_entries(self.vf)

    def isnumber(self, s):
        try:
            float(s)
            bool_a = True
        except:
            bool_a = False

        return bool_a