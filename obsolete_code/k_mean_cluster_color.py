import cv2, numpy as np
from sklearn.cluster import KMeans

def visualize_colors(cluster, centroids):
    # Get the number of different clusters, create histogram, and normalize
    labels = np.arange(0, len(np.unique(cluster.labels_)) + 1)
    (hist, _) = np.histogram(cluster.labels_, bins = labels)
    hist = hist.astype("float")
    hist /= hist.sum()

    # Create frequency rect and iterate through each cluster's color and percentage
    rect = np.zeros((50, 300, 3), dtype=np.uint8)
    colors_percent = sorted([(percent, color) for (percent, color) in zip(hist, centroids)])
    colors = [x[1] for x in colors_percent]
    
    return colors

# Load image and convert to a list of pixels
image = cv2.imread('test_image3.jpg')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
reshape = image.reshape((image.shape[0] * image.shape[1], 3))

# Find and display most dominant colors
cluster = KMeans(n_clusters=5).fit(reshape)
visualize = visualize_colors(cluster, cluster.cluster_centers_)
# visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
# cv2.imshow('visualize', visualize)
# cv2.waitKey()
for color in visualize:
    print(color[1])