import subprocess

import cv2
import numpy as np
import utils
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

#find resolution of current monitor
def get_screen_resolution():
    output = subprocess.check_output(['xrandr'])
    resolution = output.split()[7]
    resolution = resolution.split(b'x')
    return resolution
def replicate_border(image: object, ratio: object) -> object:
    # Get the dimensions of the image
    rows, cols, _ = image.shape

    # Initialize variables to keep track of the start and end points of the border
    start_row = 0
    end_row = 0
    start_col = 0
    end_col = 0

    # Find the start and end points of the border
    for row in range(rows):
        if not np.array_equal(image[row, 0], image[row, cols - 1]):
            start_row = row
            break

    for row in range(rows - 1, 0, -1):
        if not np.array_equal(image[row, 0], image[row, cols - 1]):
            end_row = row
            break

    for col in range(cols):
        if not np.array_equal(image[0, col], image[rows - 1, col]):
            start_col = col
            break

    for col in range(cols - 1, 0, -1):
        if not np.array_equal(image[0, col], image[rows - 1, col]):
            end_col = col
            break

    # Calculate the thickness of the border
    border_thickness = min(end_row - start_row, end_col - start_col)

    # Check if the border thickness is above the ratio
    if border_thickness / min(rows, cols) > ratio:
        # Replicate the border around the entire image
        image[:border_thickness, :] = image[start_row:start_row + border_thickness, :]
        image[-border_thickness:, :] = image[end_row - border_thickness:end_row, :]
        image[:, :border_thickness] = image[:, start_col:start_col + border_thickness]
        image[:, -border_thickness:] = image[:, end_col - border_thickness:end_col]


def get_dominant_color(image: object) -> object:
    """

    :param image:
    :return:
    """
    # reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # cluster the pixel intensities
    clt = KMeans(n_clusters=4)
    clt.fit(image)

    # build a histogram of clusters and then create a figure
    # representing the number of pixels labeled to each color
    hist = utils.centroid_histogram(clt)
    bar = utils.plot_colors(hist, clt.cluster_centers_)

    # Show our color bar
    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.show()

    # get the dominant color
    dominant_color = clt.cluster_centers_[np.argmax(hist)]
    brightness = (0.2126 * dominant_color[0] + 0.7152 * dominant_color[1] + 0.0722 * dominant_color[2]) / 255

    # check if the image is mostly black and white and sutable for nightmode
    if abs(dominant_color[0] - dominant_color[1]) < 20 and abs(dominant_color[1] - dominant_color[2]) < 20 \
            and brightness < 0.5:
        return 'night'
    # return the dominant color
    return dominant_color


class Image:
    def __init__(self, filepath):
        # Open the image
        self.image = cv2.imread(filepath)
        # Get image size
        self.width, self.height = self.image.shape[:2]

    def get_dom_color(self):
        # get the dominant color
        dominant_color = get_dominant_color(self.image)
        return dominant_color

    def resize_to_screen(self, screen_width, screen_height):
        # Calculate new size to fill screen without stretching
        if self.width / self.height > screen_width / screen_height:
            new_height = screen_height
            new_width = int(self.width * screen_height / self.height)
        else:
            new_width = screen_width
            new_height = int(self.height * screen_width / self.width)
        # resize the image to maximize background
        self.image = cv2.resize(self.image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    def fill_borders(self, ratio):
        # fill in the borders
        replicate_border(self.image, ratio)

    def save(self, filepath):
        # save the resized and filled image
        cv2.imwrite(filepath, self.image)


class JImage:
    pass