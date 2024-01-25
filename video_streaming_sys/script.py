import cv2


def main():
    # Open a video capture
    cap = cv2.VideoCapture(0)  # 0 for default camera


    # Set video dimensions and frame rate
    width = 640
    height = 480
    fps = 30


    # Create a VideoWriter object for streaming
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))


    while True:
        ret, frame = cap.read()


        if not ret:
            break


        # Write frame to the VideoWriter
        out.write(frame)


        # Display the frame (optional)
        cv2.imshow('Live Stream', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    cap.release()
    out.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()