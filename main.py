import json
import os.path
from threading import Timer
from tkinter import filedialog, END

import customtkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mmpose.apis import MMPoseInferencer
from scipy.signal import medfilt
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

        # self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame,
        #                                                 text="Save",
        #                                                 height=50)
        # self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)

        # Create Tab View
        self.tabview = None
        self.videoplayer = None
        self.srt = None
        self.alt = None
        self.spt = None
        self.frame_count = []
        self.wrist_x = []
        self.ankle_x = []
        self.figure = Figure(figsize=(20, 6), dpi=100)
        self.plot = self.figure.add_subplot(111)
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
            ('JSON', '*.json'),
            ('Video Files', '*.mp4')
        )

        filename = filedialog.askopenfilename(
            title='Select File',
            initialdir='.',
            filetypes=filetypes
        )

        # Convert First If Video
        if filename.endswith(".mp4"):
            inferencer = MMPoseInferencer(
                pose2d='models/td-hm_hrnet-w32_8xb64-210e_coco-256x192.py',
                pose2d_weights='models/td-hm_hrnet-w32_8xb64-210e_coco-256x192-81c58e40_20220909.pth'
            )
            result_generator = inferencer(filename, pred_out_dir='results', vis_out_dir='results')
            frame_count = 0
            while True:
                try:
                    # noinspection PyTypeChecker
                    next(result_generator)
                    print("Frame: " + str(frame_count))
                    frame_count += 1
                except StopIteration:
                    break

        # Load JSON Data
        actual_filename = os.path.splitext(os.path.basename(filename))[0]
        with open("results/{}.json".format(actual_filename), "r") as f:
            data = json.load(f)
            for i, frame in enumerate(data):
                instance = frame['instances'][0]
                keypoints = instance['keypoints']
                scores = instance['keypoint_scores']

                right_wrist = keypoints[10]
                right_hip = keypoints[12]
                right_ankle = keypoints[16]

                # Frame Count
                self.frame_count.append(i)

                # Wrist
                wrist_relative_x = right_wrist[0] - right_hip[0]
                if wrist_relative_x < 0:
                    wrist_relative_x = 0
                self.wrist_x.append(wrist_relative_x)

                # Ankle
                ankle_relative_x = right_ankle[0] - right_hip[0]
                if ankle_relative_x > 0:
                    ankle_relative_x = 0
                self.ankle_x.append(ankle_relative_x)

        # Plotting the Graph
        wrist_x = medfilt(self.wrist_x, kernel_size=15)
        ankle_x = medfilt(self.ankle_x, kernel_size=15)
        self.plot.plot(self.frame_count, wrist_x)
        self.plot.plot(self.frame_count, ankle_x)

        self.videoplayer.load("results/" + actual_filename + ".mp4")
        Timer(2, self.videoplayer.play).start()

        self.entry.delete(0, END)
        self.entry.insert(0, filename)

    def configure_tab_view(self):
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=1, columnspan=2, padx=20, pady=20, sticky="nsew")
        self.tabview.add("Overview")
        self.tabview.add("Graphs")

        # Video Player
        self.videoplayer = TkinterVideo(self.tabview.tab("Overview"), scaled=True)
        self.videoplayer.grid(row=0, column=0, rowspan=3, padx=20, pady=20, sticky="nsew")
        # self.videoplayer.load("data/breast.mp4")
        # self.videoplayer.play()

        # Overview
        self.tabview.tab("Overview").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Overview").grid_rowconfigure(0, weight=1)  # configure grid of individual tabs
        # self.srt = customtkinter.CTkLabel(self.tabview.tab("Overview"),
        #                                   text="SRT\n\n? seconds",
        #                                   font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.srt.grid(row=0, column=1, padx=20, pady=20)
        #
        # self.alt = customtkinter.CTkLabel(self.tabview.tab("Overview"),
        #                                   text="ALT\n\n? seconds",
        #                                   font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.alt.grid(row=1, column=1, padx=20, pady=20)
        #
        # self.spt = customtkinter.CTkLabel(self.tabview.tab("Overview"),
        #                                   text="SPT\n\n? seconds",
        #                                   font=customtkinter.CTkFont(size=20, weight="bold"))
        # self.spt.grid(row=2, column=1, padx=20, pady=20)

        # Graph
        self.tabview.tab("Graphs").grid_columnconfigure(0, weight=1)
        motion = customtkinter.CTkLabel(self.tabview.tab("Graphs"),
                                        text="Kick vs Pull Motion",
                                        font=customtkinter.CTkFont(size=20, weight="bold"))
        motion.grid(row=0, column=0, padx=20, pady=20)
        canvas = FigureCanvasTkAgg(self.figure, self.tabview.tab("Graphs"))
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