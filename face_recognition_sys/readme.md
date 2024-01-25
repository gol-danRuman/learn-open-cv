
# Face Recognition System

> basics.py
  - Basic logic for using face recognition system

> credentials.json
  - Credential for google workspace
  - https://console.cloud.google.com/apis/dashboard?project=symmetric-span-411911

> encode_generator.py
  - logic for encoding the images
  - read the [spreadsheet](https://docs.google.com/spreadsheets/d/14SobbZCDKX9IKOJjY56G-WIOfVc7BctskqEKRG2ImAo/edit?resourcekey#gid=1132047224) which is filled with [form](https://forms.gle/15pNdt9f3BgL4nTh7) 
  - the image url in the form is located at [drive](https://drive.google.com/drive/u/0/folders/1Yo50e_-Wg0VuEiYU06mg6kRp0NCa8nrgzglOQfLiB3MizkpP5Ye7rp3KQuknwPseRhejC9sI)
  - saved the model as EncodeFile.p using pickle

> get_drive_image_from_sheet.py
  - testing code to get image from the sheet above

> google_space_msg.py
  - send message to google space script

> compare_face_recognition.py
  - get info from sheet and images from drive, which is stored the model as pickle file
  - import that pickle file and get images from the camera to compare the face matching to the already created model

## Frontend

React applicaton to connect face recognition system build from [ref](https://www.smashingmagazine.com/2020/06/facial-recognition-web-application-react/)



## Devops

- Use Docker for building app and pushing image to dockerhub
- Commands used for docker images and deployment
> docker push rumancha12/face_recognition_backend_image:latest
> docker tag face_recognition_backend_image rumancha12/face_recognition_backend_image:latest
> docker login
> docker ps -a
> docker image ls
> docker run -it --name backend -p 8000:8000 --network bridge face_recognition_backend_image
> docker build -t face_recognition_backend_image .
> docker rm backend
> sudo systemctl status docker
> sudo systemctl restart docker
>  docker pull m03geek/ffmpeg-opencv-dlib
> 
> 



### Hosting: 
I have used [render](https://dashboard.render.com/web/srv-cmp42kfqd2ns738o8jr0/deploys/dep-cmp42kvqd2ns738o8jtg) for backend deployment using my 
dockerhub and images 
Image URL: docker.io/rumancha12/face_recognition_backend_image:latest
BackEnd API: https://face-recognition-sys-backend-api.onrender.com/
FrontEnd URL: 












- References:
  - https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78
  - https://www.youtube.com/watch?v=sz25xxF_AVE&list=PLMoSUbG1Q_r8jFS04rot-3NzidnV54Z2q&index=4&ab_channel=Murtaza%27sWorkshop-RoboticsandAI
  - https://kumarvinay.com/installing-dlib-library-in-ubuntu/ [dlib install]