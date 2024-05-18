import array
import zlib

from PIL import Image


def encode_invisible_watermark(input_image_path, output_image_path, watermark_text, txt_file=None):
    """
    Encodes an invisible watermark into an image using a steganography technique.
    This function embeds a compressed text message into the least significant bits of an image's pixels.

    example: r & 0xf8 | (c & 0xe0) >> 5
    1. In an 8-bit color depth image, r is an integer ranging from 0 to 255, represented in binary as RRRRRRRR (where each R is a bit).
    2. Masking with 0xf8:
        - The binary representation of 0xf8 is 11111000.
        - When you perform a bitwise AND (&) between r and 0xf8, it keeps the 5 most significant bits of r and sets the last 3 bits to 0.
        - r & 0xf8 results in RRRRR000, essentially clearing the least significant 3 bits of r
    3.Extracting Bits from Watermark Data (c):
        - c is a byte from the compressed watermark data.
        - 0xe0 is 11100000 in binary.
        - (c & 0xe0) keeps only the top 3 bits of c and sets the rest to 0. The result is CCC00000.
    4. Shifting the Bits:
        - >> 5 is a right bitwise shift by 5 positions.
        - Shifting CCC00000 right by 5 positions results in 00000CCC.
    5. Combining the Two Values:
        - Finally, the bitwise OR (|) combines RRRRR000 and 00000CCC.
        - This results in RRRRRCCC, where the top 5 bits are from the original red component of the pixel, and the bottom 3 bits are now carrying part of the watermark data.


    :param txt_file:
    :param input_image_path: Path to the input image file.
    :param output_image_path: Path where the watermarked image will be saved.
    :param watermark_text: The text message to encode as a watermark.
    """
    img = Image.open(input_image_path).convert("RGB")

    if txt_file is not None:
        with open(txt_file, 'r') as file:
            watermark_text = file.read()

    # Convert the watermark text to bytes and compress it
    txtdata = zlib.compress(watermark_text.encode('utf-8'))
    # Convert the compressed text data into an array of bytes
    txtarr = array.array('B')
    txtarr.frombytes(txtdata)

    # Check if the watermark data fits within the image
    if len(txtarr) > len(img.getdata()):
        raise ValueError("Watermark is too large for the given image")

    # Copy the original image to embed the watermark
    newimg = img.copy()

    # Embed the watermark data into the least significant bits of the image pixels
    # Red channel: Keep the most significant 5 bits of the red value, then add the top 3 bits of the watermark byte.
    # Green channel: Keep the most significant 6 bits of the green value, then add the middle 2 bits of the watermark
    # byte.
    # Blue channel: Keep the most significant 5 bits of the blue value, then add the bottom 3 bits of the watermark
    # byte.
    new_data = [
        (
            r & 0xf8 | (c & 0xe0) >> 5,
            g & 0xfc | (c & 0x18) >> 3,
            b & 0xf8 | (c & 0x07),
        ) if i < len(txtarr) else (r, g, b)
        for i, ((r, g, b), c) in enumerate(zip(img.getdata(), txtarr))
    ]

    newimg.putdata(new_data)

    # Save the watermarked image in PNG format to avoid lossy compression
    newimg.save(output_image_path, "PNG")


def decode_invisible_watermark(input_image_path):
    """
    Decodes an invisible watermark embedded into the least significant bits of an image's pixels.

    The function assumes the watermark was encoded in the following way:
    - The top 3 bits of the LSBs were used for the red color channel.
    - The middle 2 bits of the LSBs were used for the green color channel.
    - The bottom 3 bits of the LSBs were used for the blue color channel.
    """
    # Load the watermarked image and create an array for the watermark data
    img = Image.open(input_image_path)
    arrdata = array.array('B')

    try:
        # Extract the least significant bits from the image's pixel data
        for r, g, b in img.getdata():
            arrdata.append((r & 0x7) << 5 | (g & 0x3) << 3 | (b & 0x7))

        # Convert the array to bytes
        watermark_bytes = arrdata.tobytes()

        # Decompress the bytes to retrieve the original watermark data
        decompressed_data = zlib.decompress(watermark_bytes)

        # Decode the bytes object to a string using UTF-8 encoding
        watermark_string = decompressed_data.decode('utf-8')
    except Exception as e:
        return "Image was modified! >:("

    # Return the watermark string
    return watermark_string
