<h1>Project Sisyphus</h1>

This repository includes the code for my Bachelors Project.
The goal of the project is to build a Robotics/Art installation, inspired from The Myth of Sisyphus.


The file arm_control.py is a wrapper for the uarm api.
The util function find_port(), scans for serial devices and determines the port for the particular device.


References/Mentions
The directory "uarm" is part of the official API and its the essential code to run the uArm Swift Pro robotic arm. 
Source: https://github.com/uArm-Developer/uArm-Python-SDK

The code in tutorial_program.py is originally from the tutorial I followed named "Tracking an object based on color in OpenCV" which helped me understand this particular approach to image recognition and deserves my gratitude.
Source: https://toptechboy.com/tracking-an-object-based-on-color-in-opencv/
