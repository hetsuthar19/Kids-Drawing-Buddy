**Kids Drawing Buddy** is a fun, interactive, and child-friendly drawing and coloring web application designed for children aged **4–8 years**.

The application allows kids to choose simple black-and-white drawings, add colors using fill and brush tools, erase mistakes, undo changes, and automatically save their drawing progress so they can continue later.

---

## 🌟 Project Overview

Kids Drawing Buddy is designed to make digital coloring simple and enjoyable for young children.

The application provides age-appropriate drawings with large and easy-to-color areas. Children can manually paint using different colors and brush sizes or quickly color closed areas using the fill tool.

The application also automatically saves the child's drawing progress.

If the child leaves the drawing screen and opens the same drawing again later, the previously selected colors and brush strokes are restored.

---

## ✨ Main Features

### 👤 User Account

- User Registration
- User Login
- Secure password hashing
- User-specific drawing progress
- Logout functionality

---

### 🎂 Age Selection

The application supports children aged:

- 4 Years
- 5 Years
- 6 Years
- 7 Years
- 8 Years

Drawings are displayed according to the selected age.

Older children can also access drawings available for younger age groups.

---

## 🖼️ Drawing Gallery

Kids can select different drawings from the drawing gallery.

Example drawing categories include:

- 🍎 Big Apple
- 🌼 Happy Flower
- 🐟 Friendly Fish
- 🍦 Ice Cream
- 🚗 Little Car
- 🐢 Cute Turtle
- 🚀 Space Rocket
- 🦋 Big Butterfly
- 🏠 Cozy House
- 🏰 Simple Castle

The illustrations are designed with:

- Clean black outlines
- Large coloring areas
- Simple shapes
- Closed paths
- Minimal unnecessary details
- Kid-friendly designs

---

## 🖌️ Drawing Tools

The drawing screen includes an easy-to-use toolbar.

### 🪣 Fill Tool

Kids can:

1. Select a color.
2. Select the Fill Tool.
3. Tap a closed area of the drawing.
4. The selected area is filled automatically.

---

### 🖌️ Paint Brush

Children can manually draw and paint directly on the drawing.

Available brush sizes:

- Small
- Medium
- Large

---

### 🧽 Eraser

The eraser allows children to remove:

- Brush strokes
- Filled colors

---

### ↶ Undo

The Undo button restores the previous drawing action.

---

### 🗑️ Reset

The Reset button clears the current drawing and returns it to its original black-and-white state.

---

## 🎨 Color Palette

The application provides multiple child-friendly colors such as:

- Red
- Pink
- Orange
- Yellow
- Green
- Blue
- Purple
- Brown
- Black
- White

Kids can easily switch between colors while drawing.

---

## ☁️ Auto Save System

One of the main features of Kids Drawing Buddy is **automatic progress saving**.

The drawing is automatically saved whenever the child:

- Fills a drawing area
- Paints with the brush
- Uses the eraser
- Uses Undo
- Resets the drawing
- Changes drawing progress

The child does not need to manually press a Save button.

---

## 🔄 Continue Drawing Later

When a child opens an unfinished drawing again, the application restores:

- Previously filled colors
- Brush strokes
- Drawing progress

This allows kids to continue exactly where they stopped.

---

## 📊 Drawing Progress Status

The gallery shows the current status of each drawing.

### Start

The drawing has not been started yet.

### In Progress

The child has started coloring the drawing and the progress has been automatically saved.

### Completed

The child has finished the drawing.

---

## 🎉 Drawing Completion

When the child finishes coloring, they can click:

**✓ Finish**

The application then:

1. Saves the latest drawing progress.
2. Marks the drawing as completed.
3. Displays a celebration popup.
4. Shows a **Great Job!** message.
5. Displays the completed drawing in the gallery.

---

## 🎨 Application Theme

Kids Drawing Buddy uses a warm and playful color theme.

### Desert Sun

```text
#DC9750
```

### Dark Blue

```text
#1E2640
```

The drawing canvas remains white so children can clearly see the black drawing outlines and their selected colors.

---

## 🦁 Drawing Buddy Mascot

The application includes a friendly lion mascot that represents **Kids Drawing Buddy**.

The mascot helps make the application more attractive, welcoming, and suitable for young children.

---

## 💻 Technologies Used

### Frontend

- HTML5
- CSS3
- JavaScript
- SVG

### Backend

- Python
- Flask

### Database

- SQLite

### Other Technologies

- Jinja2 Templates
- Werkzeug Password Hashing
- Fetch API
- JSON
- Responsive CSS

---

## 🗂️ Project Structure

```text
Kids-Drawing-Buddy/
│
├── app.py
├── requirements.txt
├── START_HERE.bat
├── README.md
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── age.html
│   ├── gallery.html
│   └── draw.html
│
├── static/
│   │
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── draw.js
│   │
│   └── images/
│       └── lion-drawing-buddy.png
│
└── kids_coloring.db
```

---


# 🔄 Application Flow

```text
User Registration / Login
          ↓
     Select Age
        4–8
          ↓
    Drawing Gallery
          ↓
     Select Drawing
          ↓
 Select Drawing Tool
   Fill / Brush
          ↓
     Choose Color
          ↓
      Start Coloring
          ↓
       Auto Save
          ↓
   Continue Later
          ↓
        Finish
          ↓
    🎉 Great Job!
          ↓
 Drawing Marked Completed
```
## 📸 Application Screenshots

### Login Screen

<img width="1920" height="1080" alt="Screenshot 2026-11-25 010247" src="https://github.com/user-attachments/assets/af95e193-3128-461a-b62e-eb1e591ccd36" />


---

### Registration Screen

<img width="1920" height="1080" alt="Screenshot 2026-11-25 010812" src="https://github.com/user-attachments/assets/337d06ce-4570-47a1-9bfe-89b1a35a9a34" />


---

### Age Selection Screen

<img width="1920" height="1080" alt="Screenshot 2026-11-25 010224" src="https://github.com/user-attachments/assets/b4dbbff3-607c-430d-9d3a-be7dfc27b902" />


---

### Drawing Gallery

<img width="1920" height="1080" alt="Screenshot 2026-11-25 010309" src="https://github.com/user-attachments/assets/01f5fe48-d906-412e-901a-8b494256b0bd" />

---

### Drawing & Coloring Screen

<img width="1920" height="1080" alt="Screenshot 2026-11-25 010321" src="https://github.com/user-attachments/assets/6f5e801f-017d-4fbd-90e3-cc60def0a9a5" />
<img width="1920" height="1080" alt="Screenshot 2026-11-25 010538" src="https://github.com/user-attachments/assets/eed8cacd-e7d2-4012-ad4d-3d11017c185e" />
<img width="1920" height="1080" alt="Screenshot 2026-11-25 010559" src="https://github.com/user-attachments/assets/58127296-4be7-412b-84b4-fd843f8a1db1" />


---

### Completed Drawing

<img width="1920" height="1080" alt="Screenshot 2026-11-25 010547" src="https://github.com/user-attachments/assets/cdb4f446-97d1-41a1-be72-04758e51807d" />
---

# About the Project

Kids Drawing Buddy combines creativity and technology to provide children with an easy and enjoyable digital coloring experience.

The main focus of the project is:

**Draw. Color. Save. Continue. Create. 🎨**

---
