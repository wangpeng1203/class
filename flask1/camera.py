import cv2

if __name__ == '__main__':
    i = 0
    cap = cv2.VideoCapture(0)
    while (i<1):
        ret, frame = cap.read()
        cv2.imshow("capture", frame)

        k = cv2.waitKey(1)
        if k == ord('s'):
            cv2.imwrite('static/photo/' + str(i) + '.jpg', frame)
            i += 1
        elif k == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
