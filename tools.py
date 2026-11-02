import os

from PIL import Image, ImageDraw, ImageFont


def _save_image(image, output_path, format=None, **options):
    output_format = format or Image.registered_extensions().get(
        os.path.splitext(output_path)[1].lower()
    )
    if output_format and output_format.upper() in ("JPEG", "JPG") and image.mode not in ("RGB", "L"):
        image = image.convert("RGB")
    if format is None:
        image.save(output_path, **options)
    else:
        image.save(output_path, format=format, **options)


def compress(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        _save_image(img, output_path, optimize=True, quality=quality)

def resize(input_path, output_path, size):
    with Image.open(input_path) as img:
        img.thumbnail(size)
        _save_image(img, output_path, optimize=True)

def apply_watermark(input_path, output_path, watermark_path, position=(0, 0)):
    with Image.open(input_path) as img:
        with Image.open(watermark_path) as watermark:
            if watermark.mode in ("RGBA", "P"):
                watermark = watermark.convert("RGBA")
            img.paste(watermark, position, watermark)
            _save_image(img, output_path, optimize=True)

def convert_format(input_path, output_path, format):
    with Image.open(input_path) as img:
        _save_image(img, output_path, format=format)

def make_watermark(input_path, output_path, size=(100, 100), opacity=128, background=False):
    with Image.open(input_path) as img:
        img = img.resize(size)
        if not background:
            img = img.convert("RGBA")
            alpha = img.split()[3]
            alpha = alpha.point(lambda p: p * (opacity / 255))
            img.putalpha(alpha)
        _save_image(img, output_path, optimize=True)

def add_text_watermark(image_path, text, output_path, font_size=50, opacity=65, angle=35, spacing_x=400, spacing_y=200):

    image = Image.open(image_path).convert("RGBA")
    width, height = image.size

    watermark = Image.new(
        "RGBA",
        (width * 2, height * 2),
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(watermark)
    font = ImageFont.truetype("arial.ttf", font_size)

    for x in range(0, width * 2, spacing_x):
        for y in range(0, height * 2, spacing_y):
            draw.text(
                (x, y),
                text,
                font=font,
                fill=(255, 255, 255, opacity)
            )

    watermark = watermark.rotate(angle, expand=False)
    left = (watermark.width - width) // 2
    top = (watermark.height - height) // 2

    watermark = watermark.crop((
        left,
        top,
        left + width,
        top + height
    ))

    image = Image.alpha_composite(image, watermark)
    image.convert("RGB").save(output_path)
