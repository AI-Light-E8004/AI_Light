
# Import Module
from PIL import Image
 
def most_common_used_color(img):
    # Get width and height of Image
    width, height = img.size
 
    # Initialize Variable
    r_total = 0
    g_total = 0
    b_total = 0
 
    count = 0
 
    # Iterate through each pixel
    for x in range(0, width):
        for y in range(0, height):
            # r,g,b value of pixel
            r, g, b = img.getpixel((x, y))
 
            r_total += r
            g_total += g
            b_total += b
            count += 1
 
    return (int(r_total/count), int(g_total/count), int(b_total/count))
 
# Read Image
img = Image.open("testimage2.jpeg")
 
# Convert Image into RGB
img = img.convert('RGB')
 
# call function
common_color = most_common_used_color(img)
 
print(common_color)
# Output is (R, G, B)

new_img = Image.new("RGB", (300, 300), common_color)

new_img.save("generated_color_2.jpg")