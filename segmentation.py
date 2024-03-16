class ImageSegmentation:
    def __init__(self, image_path):
        self.image_path = image_path

    def load_image(self):
        # TODO: Implement image loading logic
        pass

    def apply_segmentation(self):
        # TODO: Implement image segmentation logic
        pass

    def extract_location(self):
        # TODO: Implement location extraction logic
        pass

    def extract_place(self):
        # TODO: Implement place extraction logic
        pass


if __name__ == "__main__":
    from segment_anything import sam_model_registry
    from segment_anything import SamAutomaticMaskGenerator
    #sam = sam_model_registry["vit_h"](checkpoint="models/sam_vit_h_4b8939.pth")


    from PIL import Image
    import numpy as np

    # Load the image
    img = Image.open("images/example_0.jpg")

    # Convert the image to a NumPy array
    img_array = np.array(img, dtype=np.uint8)
        
    # mask_generator = SamAutomaticMaskGenerator(sam)
    # masks = mask_generator.generate(img_array)

    # print(masks)

    img_masks = "models/example_0_mask.pkl"

    # import pickle
    # # Assuming masks is your variable containing the results
    # with open(img_masks, 'wb') as f:
    #     pickle.dump(masks, f)
    import pickle 
    with open(img_masks,"rb") as f:
        masks = pickle.load(f)

    mask1 = masks[0]["segmentation"]

    #make hte mask be three dimension
    mask1 = np.expand_dims(mask1, axis=2)
    import numpy as np 
    #mask1 = np.ones_like(mask1, dtype=bool)
    
    masked_img_array = np.where(mask1==0, 0, img_array)

    # Convert the result back to an image
    masked_img = Image.fromarray(masked_img_array.astype('uint8'))

    # Save the result
    masked_img.save('masked_image.jpg')

    import matplotlib.pyplot as plt

    # Display the image
    plt.imshow(masked_img)
    plt.show()