# FriendsConnect

A real-time chat application built with **Django**, **Django Channels**, and **HTMX**. This app supports live messaging, media uploads and dynamic user interfaces.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Setup](#setup)
- [Screenshots](#screenshots)
- [Contact](#contact)

## Features

- **Real-time Messaging**: Instant messaging powered by Django Channels and WebSockets.
- **Media Uploads**: Upload images and files during chats. 
- **Dynamic UI with HTMX**: Enables this app to feel like SAP in certain section.
- **User Profiles and Friend Management**: Manage your profile and your friend list.
- **Email Verification**: Secure user registration and password change requests with email verification using Celery.

## Tech Stack

- **Backend**: Django, Django Channels
- **Frontend**: HTMX, Django Templates
- **Database**: SQLite (or your preferred relational database)
- **Task Queue**: Celery with Redis
- **Authentication**: Django's built-in authentication system

## Installation

### Prerequisites

- Python 3.8 or above
- Redis (for Celery)
- Git

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/chat-app.git
   cd chat-app
2. Create a Virtual Environment
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install dependencies
    ```bash
    pip install -r requirements.txt
4. Configure the database:
  -Update the DATABASES setting in your settings.py with your database credentials.
  -Run migrations:
     ```bash
     python manage.py migrate
5. Run redis
  -I prefere runing redis in docker you may run any way you like.
6. Start Celery Worker:
   ```bash
   celery -A chat_app worker --loglevel=info
7. Run the Django development server:
   ```bash
   python manage.py runserver
8. Access the application: Open your browser and go to http://127.0.0.1:8000/.
   
 ## Screenshots

Here are some screenshots of the application in action:

### Chat Interface
![Screenshot 2025-02-26 211833](https://github.com/user-attachments/assets/ad633016-83b8-4c06-83c0-b756561ba595)


### User Profile
![Screenshot 2025-02-26 211900](https://github.com/user-attachments/assets/4923a79e-14e0-4de8-aafb-c4b0b4d1def8)


> *Note: Screenshots are for illustration purposes. Actual UI might vary based on the current implementation.*  
   
## Contact

For any questions or inquiries, feel free to reach out to me at sagacharya77@gmail.com.
 


