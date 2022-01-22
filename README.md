# Face-Recognition
  This project is still under development and won't work if deployed.
## Requirements
  - numpy
  - tensorflow>=1.12.1
  - opencv-python
  - opencv-contrib-python
  - keras
  - matplotlib
  - pillow
  - face-recognition
  - dlib
  - Django
  - django-bootstrap4
  - django-widget-tweaks
## Pre-requisites

If you use Linux then you can download the weights by executing the script provided in model-weights.

Else you can download the weights by this link

https://docs.google.com/uc?export=download&id=13gFDLFhhBqwMw6gf8jVUvNDH2UrgCCrX

and place the extracted weights file in "model-weights" folder.

## Execution

To execute the project change directory to "faceweb" and execute this command
`python manage.py runserver`


## Running as docker container
1. Build the image 
```
docker build -f DockerFile -t faceapp
```

2. Create container
```
docker create -p 3000:3000 faceapp
```

3. Start container
```
docker start <container_id>
```