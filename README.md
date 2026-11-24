# Kids Drawing Buddy

A Flask-based kids drawing and coloring application for ages **4–8**.

## Features

- User registration and login
- Age selection: 4, 5, 6, 7, 8
- Age-appropriate drawing library
- Clean black-and-white illustrations with large coloring areas
- Fill tool
- Manual paint brush
- Three brush sizes
- Eraser
- Undo and reset
- Automatic drawing-progress saving
- Restores exact fill colors and brush strokes
- Gallery preview of saved progress
- Start / In Progress / Completed states
- SQLite database

## Technology

- Python / Flask
- SQLite
- HTML
- CSS
- JavaScript
- SVG coloring illustrations

## Windows

Extract the project and double-click:

`START_HERE.bat`

The app opens at:

`http://127.0.0.1:5000`

## VS Code

Open:

`Kids-Drawing-Buddy.code-workspace`

The project is configured to use:

`.venv\Scripts\python.exe`

## Drawing ages

- Age 4: Big Apple, Happy Flower
- Age 5: Friendly Fish, Ice Cream
- Age 6: Little Car, Cute Turtle
- Age 7: Space Rocket, Big Butterfly
- Age 8: Cozy House, Simple Castle

Older ages also see drawings from the younger age levels.

## Production note

This is a local starter/MVP. Before publishing an application for children,
add production security, CSRF protection, appropriate adult/guardian controls,
privacy safeguards, data minimization, and the protections required by the
laws applicable to your users.
