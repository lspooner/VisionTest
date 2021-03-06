import cv2
import numpy as np

def retrieve_subsections(img):
    """Yield coordinates of boxes that contain interesting images

    Yields x, y coordinates; width and height as a tuple

    An example use:

        images = []
        for x, y, w, h in retrieve_subsections(img):
            image.append(img[y:y+h,x:x+w])
    """
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    results = cv2.cornerHarris(gray, 9, 3, 0.04)
    # Normalise harris points between 0 and 1
    hmin = results.min()
    hmax = results.max()
    results = (results - hmin)/(hmax-hmin)

    # Blur so we retrieve the surrounding details
    results = cv2.GaussianBlur(results, (31, 31), 5)

    # Create a threshold collecting the most interesting areas
    threshold = np.zeros(results.shape, dtype=np.uint8)
    threshold[results>results.mean() * 1.01] = 255

    # Find the bounding box of each threshold, and yield the image
    contour_response = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Different versions of cv2 return a different number of attributes
    if len(contour_response) == 3:
        contours = contour_response[1]
    else:
        contours = contour_response[0]

    for contour in contours:
        # x, y, w, h
        yield cv2.boundingRect(contour)

def retrieve_output_subsections(img):
    final_subsections = []
    for x, y, w, h in retrieve_subsections(img):
        subsection = ('ball', {'height': h, 'width': w, 'x': x, 'y': y})
        final_subsections.append(subsection)
    return final_subsections
