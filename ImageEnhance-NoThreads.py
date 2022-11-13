from PIL import Image
from PIL import ImageEnhance
import os
import time


def main():
    sharpness = float(input("Input New Sharpness:"))
    contrast = float(input("Input New Contrast:"))
    brightness = float(input("Input New Brightness:"))
    directory = input("Input Directory of Images:")
    output = input("Input Output Folder:")
    
    
    images = os.listdir(directory)
    
    
    # Create output directory if does not exist
    isExist = os.path.exists(output)
    if not isExist:
        os.makedirs(output)
    
    start_time = time.time()
    
    for image in images:
        
        og_image = image
        
        
        # Open image
        input_path = os.path.join(directory, og_image)
        image = Image.open(input_path)
        
        # Brighten up image
        curr_bri = ImageEnhance.Brightness(image)
        image = curr_bri.enhance(brightness)
        
        
        # Enhance Contrast
        curr_con = ImageEnhance.Contrast(image)
        image = curr_con.enhance(contrast)
        
        
        # Enhance Sharpness
        curr_sharp = ImageEnhance.Sharpness(image)
        image = curr_sharp.enhance(sharpness)
    
        output_path = os.path.join(output, og_image)
        image.save(output_path)
        
    
    
    # Track execution time
    print("--- %s seconds ---" % (time.time() - start_time))
    
    
    
if __name__== "__main__" :
    main()