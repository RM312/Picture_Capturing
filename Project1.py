import cv2
import os
from PIL import Image

# Load the pre-trained face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to detect faces in an image
def detect_faces(frame):
    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Return the frame with faces detected
    return frame

# Function to save the captured photo with a different name if the same name is already present
def save_photo(photo_name, frame):
    base_name, ext = os.path.splitext(photo_name)
    ext = ext if ext else ".png"  # Set default extension to .png if no extension is provided
    counter = 1

    # Append a counter to the photo name until it becomes unique
    while os.path.exists(photo_name):
        photo_name = f"{base_name}_{counter}{ext}"
        counter += 1

    try:
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        image.save(photo_name)
        print(f"Photo saved as '{photo_name}'")
    except Exception as e:
        print(f"Error saving the photo: {e}")

# Main program
def main():
    # Open the default camera
    camera = cv2.VideoCapture(0)

    # Ask the user for the number of photos to capture
    n = int(input("Enter the number of photos to capture: "))

    # Counter to keep track of the number of photos taken
    photo_counter = 1

    while True:
        # Read the current frame from the camera
        ret, frame = camera.read()

        # Perform face detection on the frame
        frame_with_faces = detect_faces(frame)

        # Display the frame with faces detected
        cv2.imshow('Faces Detected', frame_with_faces)

        # Check if Enter key is pressed
        if cv2.waitKey(1) == 13:  # 13 is the ASCII code for Enter key
            while True:
                # Ask the user for the picture name
                picture_name = input("Enter picture name (without extension): ")

                # Append .png extension if no extension is provided
                picture_name = f"{picture_name}.png"

                # Save the picture
                save_photo(picture_name, frame_with_faces)

                # Increment the photo counter
                photo_counter += 1

                # Break the loop if a unique name is provided or if the maximum number of photos is reached
                if not os.path.exists(picture_name) or photo_counter > n:
                    break

            # Break the loop after capturing the desired number of photos
            if photo_counter > n:
                break

    # Release the camera and close the window
    camera.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
