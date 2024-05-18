from tkinter import messagebox

from PIL import Image, ImageDraw, ImageFont


def apply_visible_watermark(input_image_path, output_image_path, watermark_text, **options):
    """
    Applies a visible watermark to an image.

    :param input_image_path: Path to the input image file.
    :param output_image_path: Path where the watermarked image will be saved.
    :param watermark_text: The text to use as a watermark.
    :param options: Additional options such as opacity and font size.
    """
    # Retrieve options with defaults
    opacity = options.get('opacity', 128)
    font_size = options.get('font_size', 36)

    # Load the original image
    original_image = Image.open(input_image_path).convert("RGBA")
    # Create new transparent image for the watermark
    watermark_overlay = Image.new("RGBA", original_image.size)
    watermark_drawing_context = ImageDraw.Draw(watermark_overlay)

    # Load font or use default
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # Calculate text dimensions
    text_width = watermark_drawing_context.textlength(watermark_text, font)
    text_height = font.getbbox(watermark_text)[3] - font.getbbox(watermark_text)[1]

    # Calculate padding relative to the image size
    padding_x = original_image.width * 0.01  # padding of 1% of the image width
    padding_y = original_image.height * 0.01  # padding of 1% of the image height

    # Calculate position (bottom right corner)
    x = original_image.width - text_width - padding_x
    y = original_image.height - text_height - padding_y

    # Apply text onto the watermark overlay
    watermark_drawing_context.text((x, y), watermark_text, fill=(255, 255, 255, opacity), font=font)

    # Place watermark over the original image
    watermarked_image = Image.alpha_composite(original_image, watermark_overlay)
    # Convert from RGBA to RGB for broader format support (like jpeg)
    watermarked_image.convert("RGB").save(output_image_path, "JPEG")
