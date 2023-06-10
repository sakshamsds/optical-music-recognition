This project reads muscial notes from a sheet and plays it.

[50475857_50479686_final_presentation.pdf](https://github.com/sakshamsds/optical-music-recognition/files/11641878/50475857_50479686_final_presentation.pdf)

To execute the project, please follow the following steps:
1. First install the requrired libraries using the './requirements.txt' file.
2. Run the python notebook './Code/train.ipynb' to train the 'YOLOv8x' model on the custom dataset. The custom dataset is pre-annotated and has already been divided into train, validation, and test splits. Results from training are saved under './Code/runs' directory.
3. Once the training is complete, run './Code/detect_rois.py'. This will take an input image and save the detected notes and ROIs as PNG images in the './Code/results' directory.
4. Next, load and run the './Code/detect_staff_line.py' file. This step uses the results from step 2 to predict the corresponding staff lines and save the notes in a text file as './Code/results/detected_notes.txt'. The musical notes are labeled based on their duration and position on the staff.
5. Finally, run the './Code/play.py' file to read the results from step 3 and play the music using the midiutil and pygame library.

<img width="1202" alt="image" src="https://github.com/sakshamsds/optical-music-recognition/assets/42541692/baad6d3d-2322-48bd-8524-98a818bfb737">
<img width="1199" alt="image" src="https://github.com/sakshamsds/optical-music-recognition/assets/42541692/8fc51882-b943-449c-8074-339809374553">
