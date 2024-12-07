# Face Recognition System  

🚀 **A Real-Time Face Recognition System** integrating advanced facial recognition with a MySQL database for efficient user management. This project demonstrates the seamless combination of **AI**, **Computer Vision**, and **Database Management**.

---

## 🌟 Features  

- **User Enrollment**:  
  Capture and store user details (name, course, class) and face encoding in the database.

- **Real-Time Recognition**:  
  Identify registered users on the fly, display their details dynamically, and save recognized faces to a folder.

- **Duplicate Prevention**:  
  Ensure no duplicate registrations by checking existing faces in the database.

- **Interactive UI**:  
  Provides a real-time interface for user feedback and logging.

---

## 🛠️ Tech Stack  

- **Programming Language**: Python  
- **Libraries**:  
  - `OpenCV`: For image and video processing.  
  - `face_recognition`: For facial recognition.  
- **Database**: MySQL  
- **UI**: Real-time CV2 video interface

---

## 🧑‍💻 Installation and Setup  

### 1. Clone the Repository  
  ```bash
      git clone https://github.com/your_username/Face-Recognition-System.git
      cd Face-Recognition-System
  ```


### 2. Install Dependencies
Install the required Python libraries:

  ```bash
      pip install -r requirements.txt
  ```

### 3. Set Up the Database
- Install and configure MySQL on your system.
- Create a database named face_recognition.
- Run the SQL script to set up the users table:
  ```bash
      mysql -u root -p face_recognition < database/schema.sql
  ```
  
### 4. Update Database Credentials
Edit the connect_to_database() function in main.py with your MySQL credentials:

  ```bash
  mysql.connector.connect(
      host="127.0.0.1",
      user="your_username",
      password="your_password",
      database="face_recognition"
  )
  ```

### 5. Run the Project
  ```bash
    python main.py
  ```

## 📂 Folder Structure
  ```
    Face-Recognition-System/
    ├── main.py              # Main program logic
    ├── database/
    │   └── schema.sql       # SQL script to create database schema
    ├── requirements.txt     # Python dependencies
    ├── .gitignore           # Files to ignore
    └── README.md            # Project documentation
  ```

## 📜 How It Works
### Add User
- Use the system to capture the user's face via webcam.
- Stores the face encoding along with user details (name, course, class) in the MySQL database.
### Recognize User
- Detects faces in real-time from the webcam feed.
- Matches the detected face with database records.
- Displays user information dynamically on the interface and saves recognized faces in a local folder.
### Save Recognized Faces
- Each recognized user's snapshot is saved in the recognized_faces folder.


📜 License
This project is licensed under the MIT License.
