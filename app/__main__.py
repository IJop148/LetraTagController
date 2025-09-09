import argparse
import asyncio
from io import BytesIO

import barcode
from barcode.writer import ImageWriter
from dymo_bluetooth import Canvas, discover_printers
from PIL import Image, ImageDraw, ImageFont

# Constants for image dimensions and barcode configuration
DEFAULT_IMAGE_WIDTH = 500
DEFAULT_IMAGE_HEIGHT = 35
DEFAULT_FONT_SIZE = 28
MAX_CANVAS_HEIGHT = 31
BARCODE_MODULE_WIDTH = 2.0
BARCODE_QUIET_ZONE = 2


def _draw_image_to_canvas(img: Image.Image) -> Canvas:
    """
    Converts a PIL Image to a DYMO Canvas by drawing black pixels.
    """
    canvas = Canvas()
    for y in range(img.height):
        for x in range(img.width):
            if img.getpixel((x, y)) == 0:  # Black pixel
                canvas.set_pixel(x, y, True)
    return canvas


async def print_canvas(canvas: Canvas):
    """
    Prints a given Canvas object to a DYMO LetraTag 200B printer.
    """
    # Get a list of printers.
    printers = await discover_printers()

    if not printers:
        print("No printer found")
        return

    printer = printers[0]

    # Get the first discovered printer and print the
    # constructed Canvas. Returns the print status.
    await printer.connect()
    await printer.print(canvas)
    await printer.disconnect()


async def print_text(text_to_print: str, should_print: bool = False):
    """
    Generates an image with the given text and prints it to a DYMO LetraTag 200B.
    """
    # Create a new image with a white background.
    # The size is a bit arbitrary, we'll crop it later.
    img = Image.new("1", (DEFAULT_IMAGE_WIDTH, DEFAULT_IMAGE_HEIGHT), 1)
    draw = ImageDraw.Draw(img)

    # Use a default font.
    try:
        font = ImageFont.truetype("arial.ttf", DEFAULT_FONT_SIZE)
    except IOError:
        font = ImageFont.load_default()

    # Draw the text and get its bounding box.
    draw.text((0, 0), text_to_print, font=font, fill=0)

    # Crop the image to the text.
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)

    # Create a Canvas and draw the image on it.
    canvas = _draw_image_to_canvas(img)

    if should_print:
        await print_canvas(canvas)


async def generate_and_print_barcode(text_to_encode: str, should_print: bool = False):
    """
    Generates a barcode for the given text and prints it to a DYMO LetraTag 200B.
    """
    # Generate a barcode as a PNG image in memory.
    code128 = barcode.get_barcode_class("code128")
    # Configure the writer to create a wider barcode with a quiet zone for better
    # scanning.
    writer = ImageWriter(format="PNG")
    barcode_instance = code128(text_to_encode, writer=writer)

    options = {
        # Controls the width of the thinnest bar in mm
        "module_width": BARCODE_MODULE_WIDTH,
        # Margin on the left and right of the barcode
        "quiet_zone": BARCODE_QUIET_ZONE,
        # Do not write the text representation below the barcode
        "write_text": False,
    }
    buffer = BytesIO()
    barcode_instance.write(buffer, options)

    # Open the image with Pillow.
    buffer.seek(0)
    img = Image.open(buffer)

    # Resize the image to fit the canvas height limit, maintaining aspect ratio.
    if img.height > MAX_CANVAS_HEIGHT:
        aspect_ratio = img.width / img.height
        new_height = MAX_CANVAS_HEIGHT
        new_width = int(aspect_ratio * new_height)
        img = img.resize((new_width, new_height), Image.NEAREST)

    # Convert the image to 1-bit black and white.
    img = img.convert("1")

    # Create a Canvas and draw the barcode on it.
    canvas = _draw_image_to_canvas(img)

    if should_print:
        await print_canvas(canvas)


async def main():
    parser = argparse.ArgumentParser(
        description="Generate and print a barcode on a DYMO LetraTag 200B."
    )
    parser.add_argument(
        "text",
        nargs="?",
        default="1234567890",
        help='The text to encode in the barcode. Defaults to "1234567890".',
    )
    parser.add_argument(
        "--type",
        choices=["text", "barcode"],
        default="barcode",
        help="The type of print to generate.",
    )
    args = parser.parse_args()

    if args.type == "barcode":
        await generate_and_print_barcode(args.text, should_print=True)
    else:
        await print_text(args.text, should_print=True)


if __name__ == "__main__":
    asyncio.run(main())
