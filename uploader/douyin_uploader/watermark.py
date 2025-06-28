from PIL import Image, ImageDraw, ImageFont
import os

# Set text and watermark
watermark_text_top = "SleepyKitty"  # Top-left watermark text
watermark_text_bottom_1 = "Cat Purring"  # Black text with white border part 1
watermark_text_bottom_2 = "&Soothing Music"  # Black text with white border part 2
font_path = "Y:/sucai/youran.ttf"  # Replace with your font file path

# Directory for batch processing images
input_folder = "Y:/sucai/pic"
output_folder = "Y:/sucai/picdone"

# Set border color and width
border_color = (255, 255, 255, 255)  # White
border_width = 2  # Border width
text_color = (0, 0, 0, 255)  # Black text

# Create output folder
os.makedirs(output_folder, exist_ok=True)

# Draw text with border
def draw_text_with_border(draw, position, text, font, border_color, text_color):
    x, y = position
    # Draw border
    for offset in range(-border_width, border_width + 1):
        draw.text((x + offset, y), text, font=font, fill=border_color)
        draw.text((x, y + offset), text, font=font, fill=border_color)
    # Draw text
    draw.text(position, text, font=font, fill=text_color)

# Iterate over images in input folder
for image_name in os.listdir(input_folder):
    if image_name.endswith(('jpg', 'jpeg', 'png')):  # Process specified image formats
        image_path = os.path.join(input_folder, image_name)
        img = Image.open(image_path).convert("RGBA")

        # Get image size
        width, height = img.size

        # Load font and set size
        font_size_top = int(width / 10)  # Top-left font size is 1/10 of image width
        font_size_bottom = int(width / 15)  # Bottom font is slightly smaller
        font_top = ImageFont.truetype(font_path, font_size_top)
        font_bottom = ImageFont.truetype(font_path, font_size_bottom)

        # Create transparent layer
        txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Top-left watermark (keep as is)
        draw.text((10, 10), watermark_text_top, font=font_top, fill=(255, 255, 255, 180))  # White text, slightly transparent

        # Bottom watermark position
        total_text_bottom = watermark_text_bottom_1 + watermark_text_bottom_2
        text_width_bottom = draw.textlength(total_text_bottom, font=font_bottom)
        text_position_bottom_x = (width - text_width_bottom) / 2
        text_position_bottom_y = height * 7 / 8 - font_bottom.getbbox('M')[3] / 2

        # Calculate position of semi-transparent rectangle
        padding = 10  # Padding for rectangle
        rect_x1 = text_position_bottom_x - padding
        rect_y1 = text_position_bottom_y - padding
        rect_x2 = text_position_bottom_x + text_width_bottom + padding
        rect_y2 = text_position_bottom_y + font_size_bottom + padding

        # Draw semi-transparent rectangle
        draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill=(255, 255, 255, 128))

        # Draw bottom text with white border
        x = text_position_bottom_x
        for char in watermark_text_bottom_1:
            draw_text_with_border(draw, (x, text_position_bottom_y), char, font_bottom, border_color, text_color)
            x += draw.textlength(char, font=font_bottom)  # Update x position

        for char in watermark_text_bottom_2:
            draw_text_with_border(draw, (x, text_position_bottom_y), char, font_bottom, border_color, text_color)
            x += draw.textlength(char, font=font_bottom)  # Update x position

        # Overlay watermark layer onto image
        watermarked_img = Image.alpha_composite(img, txt_layer)

        # Convert image to PNG format and save
        output_image_name = os.path.splitext(image_name)[0] + ".png"  # Replace with PNG extension
        output_image_path = os.path.join(output_folder, output_image_name)
        watermarked_img.save(output_image_path, format="PNG")

print("Batch processing and conversion to PNG format completed!")
