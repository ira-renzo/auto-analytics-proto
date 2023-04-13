<h1>
  Desktop Application for Automated Swimming Analytics
</h1>

<p align="justify">
  Sports analytics has become more popular in the world of sports. They play a huge role in enhancing the performance of athletes, assisting coaches in keeping track of their athletes, analyzing their performance, and determining strategies for improvement. In swimming, there have been limitations given the environment. In the Philippines, swimming analytics is limited to taking time using stopwatches, tempo trainers, and manually reviewing recorded footage by coaches for determining factors such as form and stroke count. This research aims to contribute to this issue by creating a swimming dataset focusing on the breaststroke swimming technique, which will then be used in training a pose estimation model and providing analytics, producing graphs containing phases of pull and kick motions of a swimmer performing the breaststroke.
</p>

<img src="https://github.com/ira-renzo/auto-analytics-proto/blob/main/tracker.png">
<img src="https://github.com/ira-renzo/auto-analytics-proto/blob/main/checker.png">

<h1>
  Notes
</h1>

- Just run main.py to start the application.
- If uploading an MP4 file, the application will run the pose estimation algorithm on the video. The program will stop and will take a few minutes to finish the process. Afterwards, this will generate the annotated MP4 and JSON file on the results folder.
- If uploading a JSON file, this will skip the pose estimation algorithm. Instead, the application will automatically look for the annotated MP4 with the same filename. The application will also generate the graphs based on the data in the JSON provided.
