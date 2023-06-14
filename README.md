## Mini Lounge Minigames Helper
### New Method (Color Detection)
![image](https://github.com/InfernoDragon0/miniLoungeMS/assets/1367130/574441d3-b052-4adf-80ce-fc2f6cd56170)

### Old Method (Image Detection)
![image](https://i.imgur.com/ZRkwCj8.jpg)

### Notes
- To run the New Method for Colorful invitation, run ```maininvitation.py```. New method may fail the combo from time to time due to incorrect delays (still fixing)
- An OpenCV python script to help with the mini lounge mini games in MS. This uses a non-invasive method. It uses OpenCV to capture the screen and act upon the current status of the game.

### Prerequisites
- OpenCV2
- numpy
- Python 3+ 64 Bits
- imutils
- pywin32
- win32api

``` 
pip install opencv-python
pip install imutils
pip install numpy
pip install pywin32
pip install keyboard
```

### Instructions
- Set your maplestory to windowed mode
- 1366 x 768 Resolution
- External Chat window does not matter
- Run ```python main.py```, make sure it is run in ADMIN MODE! For See Saw, run ```python mainseesaw.py```
- To exit, press Q when focused on any of the opencv windows
- For See Saw, you must set your npc key to S, or go to the ```mainseesaw.py``` and change ```kValue``` to your key

### Features
- Fully automated "Colorful Ignition" Mini Game
- Fully Automated "See Saw" Mini Game
