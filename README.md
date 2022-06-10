
![MIT License](https://img.shields.io/github/license/efetunca/finger-counter?style=flat-square)

# Virtual Painter

A simple program that allows you to draw with your finger on the webcam view.

The program allows switching between 3 different colors (Red, Green, Blue) and 1 eraser. Color and eraser selection boxes do not appear on the screen until a hand is detected on the webcam.
## How to Install and Run?

- Clone the project to your computer:

```bash
  git clone https://github.com/efetunca/Virtual-Painter.git
```

or simply download the project as ZIP file.

- Go to project directory:

```bash
  cd Virtual-Painter
```

- Install necessary modules:

```bash
  sudo pip3 install -r requirements.txt
```

- Run the program:

```bash
  python3 VirtualPainter.py
```

  
## Usage 

In order to use the program, a hand must first be detected on the webcam. The program works with only one hand; two-handed operation is not possible.

### To choose a color or eraser:
- Raise your index and middle fingers together and move them to the corresponding box. The text **"Select"** will appear in the lower-right side of the window.

- Each box allows its own color to be selected; select the black box for the eraser.

- By default, the program starts with the red color selected.

### To draw:
- Raise your index finger and start drawing. The text **"Draw"** will appear in the lower-right side of the window.
- As long as your index finger stay raised, you can draw. Lower your finger to stop drawing.
## Screenshots

![Usage Video](https://github.com/efetunca/Virtual-Painter/blob/main/.github/images/Virtual_Painter.gif)
## Troubleshooting

If you get the `Frames can not be received! Exiting...` error, simply run the program again.
  
## Future Updates

- The option to change the brush size will be added.

- Color and eraser selection mechanism will be improved.

- The option to save the drawing as an image will be added.

- Hand detection will be done with a self-written machine learning algorithm instead of the Mediapipe module.
## Related Project

To check out my other project that is similar to this one:

[Finger Counter](https://github.com/efetunca/Finger-Counter)

  