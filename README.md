# College Transport Management System (College_SRM_TMS)

A Flask-based web application to manage college bus transport, student assignments, and related complaints—complete with user authentication, route & boarding-point management, AI-powered travel-time estimates, and an integrated chatbot.

---

## Features

- **User Authentication & Authorization**  
  - Login/logout with Flask-Login  
  - Admin vs. regular user roles  

- **Bus Management**  
  - Create, view, and delete buses (bus number, driver name)  

- **Route Management**  
  - Define routes (route number & name)  
  - Import pre-defined “CET” routes via schema or Python script  

- **Boarding-Point Management**  
  - Add/remove boarding points (stop number, location, pickup time) per route  
  - AI-powered travel-time estimates between stops using Google’s Gemini API  

- **Student Management**  
  - Register students with enrollment numbers  
  - Assign route & boarding point  

- **Complaints Module**  
  - Students submit complaints tied to a selected bus  
  - Admins view & filter complaints  

- **Chatbot**  
  - Simple AI chatbot interface via Gemini API  

- **Extras**  
  - Dark/light theme toggle  
  - Auto-login endpoint for quick admin access (for development/demo)  

---

## Tech Stack

- **Backend**: Python, Flask, Flask-Migrate, Flask-Login, SQLAlchemy  
- **Database**: SQLite (via SQLAlchemy)  
- **AI Integration**: Google Gemini AI (via `google.generativeai`)  
- **Templates & Static Assets**: Jinja2, Bootstrap (or your choice)  

---

## Prerequisites

- Python 3.8+  
- Git  
- (Optional) Virtual environment tool: `venv`, `virtualenv`, or `pipenv`  

---

## Installation & Setup

1. **Clone the repository**  
   ```bash
   git clone https://github.com/TheSuper-Media3004/College_SRM_TMS.git
   cd College_SRM_TMS
