#!/usr/bin/env python
from keras.models import load_model
import numpy as np
import cv2 as cv


def predict(model, frame):
    # make predictions with model on frame
    size = (224, 224)
    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1.
    data = np.ndarray(shape=(1, *size, 3), dtype=np.float32)
    # resize the image to a 224x224 with the same strategy as in TM2:
    # resizing the image to be at least 224x224 and then cropping from the center
    image = cv.resize(frame, size)
    # turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    # run the inference
    prediction = model.predict(data)
    return prediction


def load_labels(path):
    # load labels file from path
    with open(path) as fp:
        return dict(map(lambda line: line.split(" ", 1), map(str.strip, fp.readlines())))


def main():
    # Load the model
    model = load_model("src/keras_model.h5")
    labels = load_labels("src/labels.txt")

    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        prediction = predict(model, frame)
        labelidx = str(np.argmax(prediction[0, :]))
        labelstr = labels[labelidx]
        print("pred: {:.2f}, {:.2f}".format(
            prediction[0, 0], prediction[0, 1]), end="\t")
        print("labelidx: {}\t labelstr: {}".format(labelidx, labelstr))

        cv.putText(
            frame,
            "Label: {}".format(labelstr),  # print text on frame
            (25, 35), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA,  # pos
        )

        # Display the resulting frame
        cv.imshow("frame", frame)
        if cv.waitKey(1) == ord("q"):
            break

    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
