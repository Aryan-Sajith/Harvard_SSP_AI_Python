import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split
# Helps use a more optimized version of ReLU activation function
from tensorflow.keras.layers import LeakyReLU

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    # Important variables
    images = []
    labels = []

    # Here we walk through the directory
    for roots, _, files in os.walk(data_dir):
        # Here we iterate specifically through the files
        for file in files:
            # Here we make sure not to iterate over the .DS_Store file
            if not file.startswith('.'):
                # Now we read in the file(as numpy.ndarrays) and resize them
                image = cv2.imread(os.path.join(roots, file))
                image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
                # Here we add the image and label to lists of outputs
                images.append(image)
                labels.append(int(os.path.basename(roots)))

    # Once we've created our desired lists we return them as outputs
    return images, labels


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Here I create my model using tensorflow(and a more optimized relu activation function)
    leaky_relu = LeakyReLU(alpha=0.001)
    model = tf.keras.models.Sequential([

        # Convolutional layer. 32 different filters utilizing a 4 x 4 kernel matrix
        tf.keras.layers.Conv2D(
            32, (4, 4), activation=leaky_relu, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Another Convolutional layer. This time using 64 different filter utilizing a 3 x 3 kernel matrix.
        tf.keras.layers.Conv2D(
            64, (3, 3), activation=leaky_relu, input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)
        ),

        # Avg pooling layer. Uses 2x2 pool size
        tf.keras.layers.AvgPool2D(pool_size=(3, 3)),

        # Flattening units
        tf.keras.layers.Flatten(),

        # Hidden layer(s) with dropout(The second layer is using an average of both the first and third layers for units)
        tf.keras.layers.Dense(256, activation=leaky_relu),
        tf.keras.layers.Dense(192, activation=leaky_relu),
        tf.keras.layers.Dense(128, activation=leaky_relu),
        tf.keras.layers.Dropout(0.15),

        # An output layer with categorizations as provided
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Now we train the neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    # Here we return the model we trained
    return model


if __name__ == "__main__":
    main()
