import sys
from PIL import Image

def encode_image(image_path, message):
    """
    Encodes a hidden message into an image using the LSB (Least Significant Bit) method.

    Args:
        image_path (str): The path to the input image file.
        message (str): The message to be encoded.
    """
    img = Image.open(image_path)
    width, height = img.size
    
    # Convert the message to binary, adding a delimiter to mark the end of the message
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Delimiter for message end

    data_index = 0
    # Iterate through each pixel and color channel to embed the message
    for row in range(height):
        for col in range(width):
            pixel = list(img.getpixel((col, row)))

            for color_channel in range(3):  # Iterate through R, G, B channels
                if data_index < len(binary_message):
                    # Modify the least significant bit of the color channel
                    # by replacing it with a bit from the binary message
                    current_color_binary = format(pixel[color_channel], '08b')
                    modified_color_binary = current_color_binary[:-1] + binary_message[data_index]
                    pixel[color_channel] = int(modified_color_binary, 2)
                    data_index += 1

            img.putpixel((col, row), tuple(pixel))

            # Stop encoding if the entire message has been embedded
            if data_index >= len(binary_message):
                break
        if data_index >= len(binary_message):
            break

    encoded_image_path = 'encoded_image.png'
    img.save(encoded_image_path)
    print(f"Steganography complete. Encoded image saved as {encoded_image_path}")

def main():
    """
    Main function to handle command-line arguments for image encoding.
    """
    if len(sys.argv) != 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return

    image_path = sys.argv[1]
    message = sys.argv[2]
    encode_image(image_path, message)

if __name__ == "__main__":
    main()