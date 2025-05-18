import cv2
import face_recognition
import pickle
import datetime
import os

def recognize_and_log():
    data = pickle.load(open("encodings.pickle", "rb"))
    known_encodings = data["encodings"]
    known_names = data["names"]

    cam = cv2.VideoCapture(0)
    today = datetime.date.today().strftime("%Y-%m-%d")
    log_file = f"attendance/{today}.csv"
    seen = set()

    os.makedirs("attendance", exist_ok=True)
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("Name,Time\n")

    while True:
        ret, frame = cam.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)

        for encoding, box in zip(encodings, boxes):
            matches = face_recognition.compare_faces(known_encodings, encoding)
            name = "Unknown"

            if True in matches:
                matched_idx = matches.index(True)
                name = known_names[matched_idx]

                if name not in seen:
                    time_str = datetime.datetime.now().strftime("%H:%M:%S")
                    with open(log_file, "a") as f:
                        f.write(f"{name},{time_str}\n")
                    seen.add(name)

            top, right, bottom, left = box
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

        cv2.imshow("Attendance System", frame)
        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

recognize_and_log()