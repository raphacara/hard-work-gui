import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, messagebox, filedialog
import threading
import time
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


def random_data_window(size=50, low=0, high=100):
    return [random.randint(low, high) for _ in range(size)]

class FakeWorkApp:
    VERSION = "3.4.0"
    BUILD = "1830"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Data Processor v{self.VERSION} 🔄")
        self.root.geometry("1200x700")
        self.dark_mode = True
        self._set_theme()

        # Menus
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Export Logs...", command=self.export_logs)
        file_menu.add_command(label="Copy Logs", command=self.copy_logs)
        file_menu.add_command(label="Clear Logs", command=self.clear_logs)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        menubar.add_cascade(label="View", menu=view_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

        # Paned window: Tasks | Controls+Logs+Metrics
        paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True)
        left = ttk.Frame(paned, width=350)
        right = ttk.Frame(paned)
        paned.add(left)
        paned.add(right)

        # Left: Filter/Search + Job list
        search_frame = ttk.Frame(left)
        ttk.Label(search_frame, text="Filter tasks:").pack(side='left')
        self.search_var = tk.StringVar()
        entry = ttk.Entry(search_frame, textvariable=self.search_var)
        entry.pack(side='left', fill='x', expand=True, padx=(5,0))
        entry.bind('<KeyRelease>', self._filter_jobs)
        search_frame.pack(fill='x', padx=5, pady=(10,0))

        self.tree = ttk.Treeview(left, columns=("status",), show='headings', height=30)
        self.tree.heading('status', text='Status')
        self.tree.column('status', width=100, anchor='center')
        self.tree.pack(fill='both', expand=True, padx=5, pady=5)
        self.tree.bind('<Button-3>', self._show_job_details)

        # Populate jobs
        self.jobs = [f"job_{i:04d}" for i in range(1, 41)]
        for job in self.jobs:
            self.tree.insert('', 'end', iid=job, values=('Pending',))

        # Right top: controls
        ctrl = ttk.Frame(right)
        self.pause_btn = ttk.Button(ctrl, text="Pause ⏸", command=self.toggle_pause)
        self.pause_btn.pack(side='left', padx=5)
        ttk.Label(ctrl, text="Speed:").pack(side='left', padx=(10,0))
        self.speed_var = tk.DoubleVar(value=1.0)
        speed_scale = ttk.Scale(ctrl, from_=0.2, to=3.0, variable=self.speed_var, orient='horizontal')
        speed_scale.pack(side='left', padx=5)
        self.view_var = tk.StringVar(value='logs')
        for label, val in [('Logs','logs'), ('Metrics','metrics')]:
            ttk.Radiobutton(ctrl, text=label, variable=self.view_var, value=val, command=self.switch_view).pack(side='left', padx=5)
        ctrl.pack(fill='x', pady=5, padx=5)

        # Logs
        self.log_area = ScrolledText(right, state='disabled', wrap='word', height=14)
        self.log_area.pack(fill='both', expand=True, padx=5, pady=5)
        for lvl, color in [('INFO','#c5c8c6'),('WARNING','#e5c07b'),('ERROR','#e06c75')]:
            self.log_area.tag_config(lvl, foreground=color)

        # Metrics
        self.metrics_frame = ttk.Frame(right)
        self.fig, (self.ax_cpu, self.ax_mem, self.ax_io) = plt.subplots(3,1, figsize=(6,5), tight_layout=True)
        for ax, title in zip((self.ax_cpu,self.ax_mem,self.ax_io), ('CPU (%)','Memory (%)','Disk IO (%)')):
            ax.set_title(title)
            ax.set_ylim(0,100)
            ax.set_xlim(0,50)
            ax.set_facecolor('#1e1e1e' if self.dark_mode else '#ffffff')
            ax.tick_params(colors='#c5c8c6' if self.dark_mode else '#000000')
            ax._line, = ax.plot([], [])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.metrics_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.cpu_data = random_data_window()
        self.mem_data = random_data_window()
        self.io_data  = random_data_window()

        # Status bar
        self.statusbar = ttk.Label(self.root, text="Ready", relief='sunken', anchor='w')
        self.statusbar.pack(fill='x')

        # Simulation messages
        self.messages = [(lvl,msg) for lvl,msg in [
            ("INFO","Initializing subsystem..."),("INFO","Loading module X..."),
            ("WARNING","Disk IO high..."),("ERROR","Packet loss detected!"),
            ("INFO","Cache rebuild complete."),("INFO","Checkpoint saved."),
            ("WARNING","Low disk space."),("INFO","Deployment pipeline triggered."),
        ]]
        self.running = True

    def _set_theme(self):
        bg = '#2e2e2e' if self.dark_mode else '#f0f0f0'
        fg = '#c5c8c6' if self.dark_mode else '#000000'
        style = ttk.Style(self.root)
        style.theme_use('default')
        style.configure('.', background=bg, foreground=fg)
        self.root.configure(bg=bg)

    def _show_job_details(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            duration = random.uniform(0.5, 5.0)
            start = time.strftime("%H:%M:%S", time.localtime(time.time() - duration * 60))
            details = (
                f"Job: {item}\n"
                f"Status: {self.tree.set(item, 'status')}\n"
                f"Start: {start}\n"
                f"Duration: {duration:.2f} min"
            )
            messagebox.showinfo("Job Details", details)

    def _filter_jobs(self, event=None):
        term = self.search_var.get().lower()
        for job in self.jobs:
            if term in job.lower():
                self.tree.reattach(job, '', 'end')
            else:
                self.tree.detach(job)

    def show_about(self):
        messagebox.showinfo("About", f"Data Processor v{self.VERSION} build {self.BUILD}\nFakeCorp 2025")

    def toggle_pause(self):
        self.running = not self.running
        self.pause_btn.config(text="Resume ▶️" if not self.running else "Pause ⏸️")
        self.statusbar.config(text="Paused" if not self.running else "Running")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self._set_theme()
        for ax in (self.ax_cpu, self.ax_mem, self.ax_io):
            ax.set_facecolor('#1e1e1e' if self.dark_mode else '#ffffff')
        self.canvas.draw()

    def switch_view(self):
        if self.view_var.get() == 'logs':
            self.metrics_frame.pack_forget()
            self.log_area.pack(fill='both', expand=True, padx=5, pady=5)
        else:
            self.log_area.pack_forget()
            self.metrics_frame.pack(fill='both', expand=True, padx=5, pady=5)

    def start_simulation(self):
        def sim():
            while True:
                speed = self.speed_var.get()
                if self.running:
                    pending = [j for j in self.jobs if self.tree.set(j, 'status') == 'Pending']
                    if pending:
                        job = random.choice(pending)
                        self.tree.set(job, 'status', 'Processing')
                        ts = time.strftime("%Y-%m-%d %H:%M:%S")
                        self._log(f"[{ts}] Processing {job}\n", 'INFO')
                        for _ in range(3):
                            if not self.running:
                                break
                            time.sleep(random.uniform(0.05, 0.2) / speed)
                            self._update_metrics()
                        ok = random.random() < 0.8
                        lvl = 'INFO' if ok else 'ERROR'
                        self.tree.set(job, 'status', 'Completed' if ok else 'Failed')
                        self._log(f"[{ts}] {'Completed' if ok else 'Failed'} {job}\n", lvl)
                    else:
                        ts = time.strftime("%Y-%m-%d %H:%M:%S")
                        self._log(f"[{ts}] Queue empty, restarting...\n", 'INFO')
                        for j in self.jobs:
                            self.tree.set(j, 'status', 'Pending')
                time.sleep(1.0 / speed)
        threading.Thread(target=sim, daemon=True).start()

    def _update_metrics(self):
        self.cpu_data.append(random.randint(5, 95))
        self.cpu_data.pop(0)
        self.mem_data.append(random.randint(10, 90))
        self.mem_data.pop(0)
        self.io_data.append(random.randint(0, 100))
        self.io_data.pop(0)
        for data, ax in ((self.cpu_data, self.ax_cpu), (self.mem_data, self.ax_mem), (self.io_data, self.ax_io)):
            ax._line.set_data(range(len(data)), data)
            ax.set_xlim(0, len(data))
        self.canvas.draw()
        if random.random() < 0.025:
            messagebox.showwarning("Alert", "Unusual network activity detected.")

    def _log(self, text, lvl):
        self.log_area.configure(state='normal')
        self.log_area.insert('end', text, lvl)
        self.log_area.see('end')
        self.log_area.configure(state='disabled')

    def export_logs(self):
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text','*.txt')])
        if path:
            with open(path, 'w') as f:
                f.write(self.log_area.get('1.0', 'end'))
            messagebox.showinfo('Export', 'Logs saved successfully.')

    def copy_logs(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.log_area.get('1.0', 'end'))
        messagebox.showinfo('Copy', 'Logs copied to clipboard.')

    def clear_logs(self):
        self.log_area.configure(state='normal')
        self.log_area.delete('1.0', 'end')
        self.log_area.configure(state='disabled')

    def run(self):
        self.start_simulation()
        self.root.after(1000, self._clock)
        self.root.mainloop()

    def _clock(self):
        self.statusbar.config(text=f"v{self.VERSION} build {self.BUILD} | {time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.root.after(1000, self._clock)

if __name__ == '__main__':
    FakeWorkApp().run()
