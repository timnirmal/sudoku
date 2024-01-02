import matplotlib.pyplot as plt
import numpy as np

def create_and_save_image_with_number(number, image_size=(28, 28), font_size=16, save_path='number_{}.png'):
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, str(number), fontsize=font_size, ha='center', va='center')
    ax.axis('off')

    # Resize the figure to fit the image size
    fig.set_size_inches(image_size[0] / fig.dpi, image_size[1] / fig.dpi)

    # Remove margins
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    # Save the figure as an image
    plt.savefig(save_path.format(number), dpi=fig.dpi, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

# Generate and save images for numbers 1 to 16
for number in range(1, 17):
    create_and_save_image_with_number(number)
