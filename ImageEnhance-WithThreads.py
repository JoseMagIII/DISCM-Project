import os
import threading
import time
import textwrap
from PIL import Image, ImageEnhance

image_lock = threading.Lock() 
start_time = 0
images_processed_cnt = 0
 
# Array of image files
images = []

def enhance_thread(sharpness, contrast, brightness, directory, output, secs):
    
    global images
    global start_time
    global images_processed_cnt
    
    while images and (time.time() - start_time) <= secs:
        
        # Get an image from list
        image_lock.acquire()
        image = images.pop()
        images_processed_cnt += 1
        image_lock.release()
        
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

        # Save image to output path
        output_path = os.path.join(output, og_image)
        image.save(output_path)


def main():
    sharpness = float(input("Input New Sharpness:"))
    contrast = float(input("Input New Contrast:"))
    brightness = float(input("Input New Brightness:"))
    directory = input("Input Directory of Images:")
    output = input("Input Output Folder:")
    secs = int(float(input("Input Number of Mins to Spend Enhancing:"))*60)
    numthreads = int(input("Input Number of Threads to Use:"))
    
    
    # Set images array
    global images 
    images = os.listdir(directory)
    
    
    # Create output directory if does not exist
    isExist = os.path.exists(output)
    if not isExist:
        os.makedirs(output)
    
    
    # Create threads
    thread_list = []
    
    for i in range(0, numthreads):
        thread = threading.Thread(target=enhance_thread, args=(sharpness, contrast, brightness, directory, output, secs))
        thread_list.append(thread)
    
    global start_time
    start_time = time.time()
    for thread in thread_list:
        thread.start()
    
    for thread in thread_list:
        thread.join()
        

    # Track execution time
    exec_time = time.time() - start_time
    print("--- %s seconds ---" % (exec_time))
    
    
    # Process text file
    global images_processed_cnt
    write_text =    f"""
                    Number of Images Processed: {images_processed_cnt}
                    Output Folder: {os.path.abspath(output)}
                    Execution Time: {exec_time}
                    Number of Threads: {numthreads}
                    Sharpness: {sharpness}
                    Brightness: {brightness}
                    Contrast: {contrast}
                    """
    
    text_path = output+'.txt'
    
    with open(text_path, 'w') as f:
        f.write(textwrap.dedent(write_text))
    
if __name__== "__main__" :
    main()