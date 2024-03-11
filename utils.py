import matplotlib.pyplot as plt


def display_image_with_matplotlib(img):
    """Display an image using matplotlib in a minimal window."""
    plt.figure(figsize=(10, 6))
    plt.imshow(img, cmap='gray')
    plt.axis('off')
    plt.show()
