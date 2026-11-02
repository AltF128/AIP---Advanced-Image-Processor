import tools

def main():
    input_path = input("Input path: ")
    output_path = input("Output path: ")
    operation = input("Operation (resize, watermark, convert, make_watermark, add_text_watermark): ")

    if operation == "resize":
        width = int(input("Width: "))
        height = int(input("Height: "))
        tools.resize(input_path, output_path, (width, height))

    elif operation == "watermark":
        watermark_path = input("Watermark path: ")
        position_x = int(input("Position X: "))
        position_y = int(input("Position Y: "))
        tools.apply_watermark(input_path, output_path, watermark_path, (position_x, position_y))

    elif operation == "convert":
        format = input("Format (e.g., JPEG, PNG): ")
        tools.convert_format(input_path, output_path, format)

    elif operation == "make_watermark":
        size = tuple(map(int, input("Size (width height): ").split()))
        opacity = int(input("Opacity (0-255): "))
        background = input("Background (True/False): ").lower() == 'true'
        tools.make_watermark(input_path, output_path, size, opacity, background)

    elif operation == "add_text_watermark":
        text = input("Text: ")
        font_size = int(input("Font size: "))
        opacity = int(input("Opacity (0-255): "))
        angle = int(input("Angle: "))
        spacing_x = int(input("Spacing X: "))
        spacing_y = int(input("Spacing Y: "))
        tools.add_text_watermark(input_path, text, output_path, font_size, opacity, angle, spacing_x, spacing_y)

if __name__ == "__main__":
    while True:
        main()