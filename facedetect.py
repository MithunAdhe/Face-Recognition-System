import cv2
import face_recognition
import mysql.connector
import pickle
import os

# Directory to save recognized images
SAVE_DIR = "recognized_faces"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

# Database connection
def connect_to_database():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="root",
            database="face_recognition"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit()

db = connect_to_database()
cursor = db.cursor()

# Setup database schema
def setup_database():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255),
            course VARCHAR(255),
            class VARCHAR(255),
            face_encoding BLOB
        )
    """)
    db.commit()

# Add a new user
def add_user(name, course, class_name):
    print("Capturing face for enrollment...")

    cap = cv2.VideoCapture(0)
    face_encoding = None

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        face_locations = face_recognition.face_locations(frame)

        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow("Press 'q' to capture", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            if face_locations:
                face_encoding = face_recognition.face_encodings(frame, face_locations)[0]
                
                # Check for duplicates in the database
                cursor.execute("SELECT name, course, class, face_encoding FROM users")
                users = cursor.fetchall()

                for user_name, course_name, class_name, encoded_data in users:
                    db_face_encoding = pickle.loads(encoded_data)

                    # Compare the captured face with existing database faces
                    matches = face_recognition.compare_faces([db_face_encoding], face_encoding, tolerance=0.6)

                    if True in matches:
                        print(f"{name} is already registered in the database!")
                        cap.release()
                        cv2.destroyAllWindows()
                        return

                # If no duplicate was found, add the new user to the database
                encoded_data = pickle.dumps(face_encoding)
                cursor.execute("INSERT INTO users (name, course, class, face_encoding) VALUES (%s, %s, %s, %s)",
                               (name, course, class_name, encoded_data))
                db.commit()

                print(f"{name} added to the database successfully.")
                cap.release()
                cv2.destroyAllWindows()
                return
            else:
                print("No face detected. Try again.")
            break

    cap.release()
    cv2.destroyAllWindows()


# Recognize users and display information
def recognize_and_display():
    print("Starting recognition...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Camera not accessible.")
        return

    recognized_users = set()  # Track already recognized users to avoid duplicate logging

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
            cursor.execute("SELECT id, name, course, class, face_encoding FROM users")
            users = cursor.fetchall()

            recognized_user = None

            for user_id, name, course, class_name, encoded_data in users:
                db_face_encoding = pickle.loads(encoded_data)
                matches = face_recognition.compare_faces([db_face_encoding], face_encoding, tolerance=0.6)

                if True in matches:
                    recognized_user = {"name": name, "course": course, "class": class_name}
                    user_id_str = f"{name}_{user_id}"

                    # Save the recognized user's image in SAVE_DIR
                    user_save_path = os.path.join(SAVE_DIR, f"{user_id_str}.jpg")
                    info_text = f"{name}, {course}, {class_name}"

                    cv2.putText(frame, info_text, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

                    cv2.imwrite(user_save_path, frame)

                    # Only log recognized users the first time
                    if user_id_str not in recognized_users:
                        recognized_users.add(user_id_str)
                        print(f"User recognized: {name}, Course: {course}, Class: {class_name}")

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                    break

            if not recognized_user:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, "Unknown", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Display the video interface
        cv2.imshow("Face Recognition", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




# Main menu
def main():
    setup_database()

    while True:
        print("\n--- Face Recognition System ---")
        print("1. Add User")
        print("2. Recognize and Display")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter name: ")
            course = input("Enter course: ")
            class_name = input("Enter class: ")
            add_user(name, course, class_name)
        elif choice == '2':
            recognize_and_display()
        elif choice == '3':
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
