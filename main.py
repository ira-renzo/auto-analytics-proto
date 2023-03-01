from threading import Timer
from tkinter import filedialog, END

import customtkinter
import numpy
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkVideoPlayer import TkinterVideo


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure Window
        self.title("Swimming Analytics")
        self.geometry("{}x{}".format(self.winfo_screenwidth(), self.winfo_screenheight()))

        # Configure Grid Layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Sidebar Frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=1, sticky="nsew")

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame,
                                                 text="Swimming\nAnalytics",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="Play/Pause",
                                                        command=self.play_pause,
                                                        height=50)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)

        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,
                                                        text="Save",
                                                        height=50)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Create Video Player
        self.videoplayer = TkinterVideo(master=self, scaled=True)
        self.videoplayer.load("swim.mp4")
        self.videoplayer.grid(row=0, column=1, padx=20, pady=80, sticky="nsew")
        self.videoplayer.play()

        # Create Tab View
        self.tabview = None
        self.srt = None
        self.alt = None
        self.spt = None
        self.configure_tab_view()

        # File Picker
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Video File Path")
        self.entry.grid(row=1, column=0, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self,
                                                     fg_color="transparent",
                                                     border_width=2,
                                                     text_color=("gray10", "#DCE4EE"),
                                                     text="Select File",
                                                     command=self.select_file)
        self.main_button_1.grid(row=1, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def select_file(self):
        filetypes = (
            ('Video Files', '*.mp4'),
        )

        filename = filedialog.askopenfilename(
            title='Select File',
            initialdir='.',
            filetypes=filetypes)

        self.videoplayer.load(filename)
        Timer(2, self.videoplayer.play).start()

        self.entry.delete(0, END)
        self.entry.insert(0, filename)

    def configure_tab_view(self):
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Metrics")
        self.tabview.add("Graphs")
        self.tabview.tab("Metrics").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Graphs").grid_columnconfigure(0, weight=1)

        self.srt = customtkinter.CTkLabel(self.tabview.tab("Metrics"),
                                          text="SRT\n\n? seconds",
                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.srt.grid(row=0, column=0, padx=20, pady=20)

        self.alt = customtkinter.CTkLabel(self.tabview.tab("Metrics"),
                                          text="ALT\n\n? seconds",
                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.alt.grid(row=1, column=0, padx=20, pady=20)

        self.spt = customtkinter.CTkLabel(self.tabview.tab("Metrics"),
                                          text="SPT\n\n? seconds",
                                          font=customtkinter.CTkFont(size=20, weight="bold"))
        self.spt.grid(row=2, column=0, padx=20, pady=20)

        motion = customtkinter.CTkLabel(self.tabview.tab("Graphs"),
                                        text="Kick vs Pull Motion",
                                        font=customtkinter.CTkFont(size=20, weight="bold"))
        motion.grid(row=0, column=0, padx=20, pady=20)

        figure = Figure(figsize=(2.5, 2.5), dpi=100)

        # Adding the Subplot
        plot = figure.add_subplot(111)

        # Plotting the Graph
        t = numpy.arange(0.0, 2.0, 0.01)
        s1 = numpy.sin(2 * numpy.pi * t)
        plot.plot(t, s1)

        canvas = FigureCanvasTkAgg(figure, self.tabview.tab("Graphs"))
        canvas.draw()
        canvas.get_tk_widget().grid(row=1, column=0, padx=20, pady=20)

    def play_pause(self):
        if self.videoplayer.is_paused():
            self.videoplayer.play()
        else:
            self.videoplayer.pause()


if __name__ == "__main__":
    customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
    customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

    app = App()
    app.mainloop()