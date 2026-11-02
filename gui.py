import os
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

import tools


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Async Image Processor")
        self.geometry("1000x720")
        self.minsize(820, 620)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.parameter_vars = {}
        self.preview_images = {}
        logo_path = os.path.join(os.path.dirname(__file__), "image_files", "logo.png")
        icon_path = os.path.join(os.path.dirname(__file__), "image_files", "app_icon.ico")
        with Image.open(logo_path) as logo:
            logo.load()
            self.logo_image = ctk.CTkImage(
                light_image=logo.copy(),
                dark_image=logo.copy(),
                size=(48, 48),
            )
        self.iconbitmap(icon_path)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(22, 8))
        ctk.CTkLabel(header, text="", image=self.logo_image).pack(
            side="left", padx=(0, 14)
        )
        title_block = ctk.CTkFrame(header, fg_color="transparent")
        title_block.pack(side="left", fill="y")
        ctk.CTkLabel(
            title_block,
            text="Image Studio",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=("#18864b", "#45d483"),
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_block,
            text="Prepare, transform, and preview your images.",
            text_color=("gray40", "gray70"),
        ).pack(anchor="w", pady=(2, 0))

        self.pages = ctk.CTkTabview(self, corner_radius=12)
        self.pages.grid(row=1, column=0, sticky="nsew", padx=28, pady=(8, 8))
        self.process_page = self.pages.add("Process")
        self.preview_page = self.pages.add("Preview")
        self.build_process_page()
        self.build_preview_page()
        self.pages.set("Process")

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, sticky="ew", padx=28, pady=(0, 16))
        footer.grid_columnconfigure(0, weight=1)
        self.status_label = ctk.CTkLabel(
            footer,
            text="Select your files and processing options to get started.",
            text_color=("gray40", "gray70"),
            anchor="w",
        )
        self.status_label.grid(row=0, column=0, sticky="ew", padx=(0, 16))
        ctk.CTkButton(
            footer,
            text="Process image",
            width=180,
            height=42,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.execute_operation,
        ).grid(row=0, column=1, sticky="e")

    def build_process_page(self):
        page = self.process_page
        page.grid_columnconfigure(0, weight=1)
        page.grid_rowconfigure(0, weight=1)
        content = ctk.CTkScrollableFrame(page, corner_radius=0, fg_color="transparent")
        content.grid(row=0, column=0, sticky="nsew")
        content.grid_columnconfigure(0, weight=1)

        file_card = ctk.CTkFrame(content, corner_radius=10)
        file_card.grid(row=0, column=0, sticky="ew", padx=12, pady=(14, 10))
        file_card.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            file_card, text="IMAGE FILES", font=ctk.CTkFont(size=12, weight="bold")
        ).grid(row=0, column=0, columnspan=3, sticky="w", padx=16, pady=(14, 8))

        ctk.CTkLabel(file_card, text="Input image").grid(
            row=1, column=0, sticky="w", padx=(16, 10), pady=6
        )
        self.input_path_entry = ctk.CTkEntry(
            file_card, placeholder_text="Choose an image to process"
        )
        self.input_path_entry.grid(row=1, column=1, sticky="ew", pady=6)
        ctk.CTkButton(
            file_card, text="Browse", width=90, command=self.browse_input
        ).grid(row=1, column=2, padx=(10, 16), pady=6)

        ctk.CTkLabel(file_card, text="Output folder").grid(
            row=2, column=0, sticky="w", padx=(16, 10), pady=6
        )
        self.output_folder_entry = ctk.CTkEntry(
            file_card, placeholder_text="Choose a folder for the processed image"
        )
        self.output_folder_entry.grid(row=2, column=1, sticky="ew", pady=6)
        ctk.CTkButton(
            file_card, text="Browse", width=90, command=self.browse_output_folder
        ).grid(row=2, column=2, padx=(10, 16), pady=6)

        ctk.CTkLabel(file_card, text="Output name").grid(
            row=3, column=0, sticky="w", padx=(16, 10), pady=(6, 14)
        )
        validate_name = self.register(self.is_valid_output_name)
        self.output_name_entry = ctk.CTkEntry(
            file_card,
            placeholder_text="Enter a name without an extension",
            validate="key",
            validatecommand=(validate_name, "%P"),
        )
        self.output_name_entry.grid(row=3, column=1, sticky="ew", pady=(6, 14))
        ctk.CTkLabel(file_card, text="No extension").grid(
            row=3, column=2, padx=(10, 16), pady=(6, 14)
        )

        operation_card = ctk.CTkFrame(content, corner_radius=10)
        operation_card.grid(row=1, column=0, sticky="ew", padx=12, pady=10)
        operation_card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            operation_card,
            text="PROCESSING",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(14, 8))

        self.operation_combobox = ctk.CTkComboBox(
            operation_card,
            values=[
                "resize",
                "watermark",
                "convert",
                "make_watermark",
                "add_text_watermark",
            ],
            command=lambda _: self.update_operation_fields(),
        )
        self.operation_combobox.pack(fill="x", padx=16, pady=(0, 10))
        self.operation_combobox.set("resize")

        self.options_frame = ctk.CTkFrame(operation_card, fg_color="transparent")
        self.options_frame.pack(fill="x", padx=16, pady=(0, 12))

        ctk.CTkLabel(
            file_card, text="Output format", font=ctk.CTkFont(size=13)
        ).grid(row=4, column=0, sticky="w", padx=(16, 10), pady=(0, 14))
        self.output_format = ctk.CTkComboBox(
            file_card,
            values=["PNG (.png)", "JPEG (.jpg)", "WebP (.webp)"],
            state="readonly",
            width=180,
        )
        self.output_format.set("PNG (.png)")
        self.output_format.grid(
            row=4, column=1, sticky="w", padx=0, pady=(0, 14)
        )

        self.update_operation_fields()

    def build_preview_page(self):
        page = self.preview_page
        page.grid_columnconfigure(0, weight=1, uniform="preview")
        page.grid_columnconfigure(1, weight=1, uniform="preview")
        page.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            page, text="Image previews", font=ctk.CTkFont(size=20, weight="bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(14, 12))

        self.input_preview, self.input_details = self.create_preview_panel(
            page, "Original image", 0
        )
        self.output_preview, self.output_details = self.create_preview_panel(
            page, "Processed image", 1
        )

    def create_preview_panel(self, parent, title, column):
        panel = ctk.CTkFrame(parent, corner_radius=10)
        panel.grid(row=1, column=column, sticky="nsew", padx=8, pady=(0, 12))
        panel.grid_columnconfigure(0, weight=1)
        panel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            panel, text=title, font=ctk.CTkFont(size=15, weight="bold")
        ).grid(row=0, column=0, sticky="w", padx=14, pady=(14, 8))
        preview = ctk.CTkLabel(
            panel,
            text="Choose an image to see a preview",
            text_color=("gray45", "gray65"),
            fg_color=("gray90", "gray17"),
            corner_radius=8,
        )
        preview.grid(row=1, column=0, sticky="nsew", padx=14, pady=6)
        details = ctk.CTkLabel(
            panel, text="No image loaded", text_color=("gray40", "gray70"), anchor="w"
        )
        details.grid(row=2, column=0, sticky="ew", padx=14, pady=(8, 14))
        return preview, details

    def update_operation_fields(self):
        for child in self.options_frame.winfo_children():
            child.destroy()
        self.parameter_vars.clear()

        operation = self.operation_combobox.get()
        if operation == "resize":
            self.add_field("Width (pixels)", "width", "800")
            self.add_field("Height (pixels)", "height", "600")
        elif operation == "watermark":
            self.add_file_field("Watermark image", "watermark_path")
            self.add_field("Position X", "position_x", "0")
            self.add_field("Position Y", "position_y", "0")
        elif operation == "make_watermark":
            self.add_field("Width (pixels)", "width", "100")
            self.add_field("Height (pixels)", "height", "100")
            self.add_field("Opacity (0-255)", "opacity", "128")
            self.add_field("Keep background (True/False)", "background", "False")
        elif operation == "add_text_watermark":
            self.add_field("Watermark text", "text", "AIP STANDARD")
            self.add_field("Font size", "font_size", "50")
            self.add_field("Opacity (0-255)", "opacity", "65")
            self.add_field("Angle", "angle", "35")
            self.add_field("Spacing X", "spacing_x", "400")
            self.add_field("Spacing Y", "spacing_y", "200")

    def add_field(self, label, name, default):
        row = len(self.parameter_vars)
        ctk.CTkLabel(self.options_frame, text=label).grid(
            row=row, column=0, sticky="w", padx=(0, 12), pady=5
        )
        value = ctk.StringVar(value=default)
        ctk.CTkEntry(self.options_frame, textvariable=value).grid(
            row=row, column=1, sticky="ew", pady=5
        )
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.parameter_vars[name] = value

    def add_file_field(self, label, name):
        row = len(self.parameter_vars)
        ctk.CTkLabel(self.options_frame, text=label).grid(
            row=row, column=0, sticky="w", padx=(0, 12), pady=5
        )
        value = ctk.StringVar()
        ctk.CTkEntry(self.options_frame, textvariable=value).grid(
            row=row, column=1, sticky="ew", pady=5
        )
        ctk.CTkButton(
            self.options_frame,
            text="Browse",
            width=80,
            command=lambda: self.browse_watermark(value),
        ).grid(row=row, column=2, padx=(8, 0), pady=5)
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.parameter_vars[name] = value

    def browse_input(self):
        path = filedialog.askopenfilename(
            parent=self,
            title="Select input image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp *.tif *.tiff"), ("All files", "*.*")],
        )
        if path:
            self.input_path_entry.delete(0, "end")
            self.input_path_entry.insert(0, path)
            try:
                self.update_preview(path, self.input_preview, self.input_details)
            except OSError as error:
                messagebox.showerror("Could not open image", str(error), parent=self)

    @staticmethod
    def is_valid_output_name(name):
        return not any(character in name for character in '.\\/<>:"|?*')

    def browse_output_folder(self):
        path = filedialog.askdirectory(parent=self, title="Choose output folder")
        if path:
            self.output_folder_entry.delete(0, "end")
            self.output_folder_entry.insert(0, path)

    def browse_watermark(self, variable):
        path = filedialog.askopenfilename(
            parent=self,
            title="Select watermark image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.webp *.bmp"), ("All files", "*.*")],
        )
        if path:
            variable.set(path)

    def update_preview(self, path, preview, details):
        with Image.open(path) as image:
            image.load()
            width, height = image.size
            mode = image.mode
            display_image = image.copy()

        display_image.thumbnail((520, 390))
        ctk_image = ctk.CTkImage(
            light_image=display_image,
            dark_image=display_image,
            size=display_image.size,
        )
        self.preview_images[preview] = ctk_image
        preview.configure(image=ctk_image, text="")
        details.configure(
            text=f"{os.path.basename(path)}  |  {width} x {height}  |  {mode}"
        )

    def execute_operation(self):
        input_path = self.input_path_entry.get().strip()
        output_folder = self.output_folder_entry.get().strip()
        output_name = self.output_name_entry.get().strip()
        if not input_path or not output_folder or not output_name:
            messagebox.showwarning(
                "Files required",
                "Choose an input image and output folder, then enter an output name.",
                parent=self,
            )
            return

        if not self.is_valid_output_name(output_name):
            messagebox.showwarning(
                "Invalid output name",
                "Enter a name without a file extension or path characters.",
                parent=self,
            )
            return

        output_format = self.output_format.get()
        format_name, extension = {
            "PNG (.png)": ("PNG", ".png"),
            "JPEG (.jpg)": ("JPEG", ".jpg"),
            "WebP (.webp)": ("WEBP", ".webp"),
        }[output_format]
        output_path = os.path.join(output_folder, output_name + extension)
        operation = self.operation_combobox.get()
        values = {name: variable.get().strip() for name, variable in self.parameter_vars.items()}
        try:
            if operation == "resize":
                tools.resize(input_path, output_path, (int(values["width"]), int(values["height"])))
            elif operation == "watermark":
                tools.apply_watermark(
                    input_path,
                    output_path,
                    values["watermark_path"],
                    (int(values["position_x"]), int(values["position_y"])),
                )
            elif operation == "convert":
                tools.convert_format(input_path, output_path, format_name)
            elif operation == "make_watermark":
                tools.make_watermark(
                    input_path,
                    output_path,
                    (int(values["width"]), int(values["height"])),
                    int(values["opacity"]),
                    values["background"].lower() in ("true", "yes", "1"),
                )
            elif operation == "add_text_watermark":
                tools.add_text_watermark(
                    input_path,
                    values["text"],
                    output_path,
                    int(values["font_size"]),
                    int(values["opacity"]),
                    int(values["angle"]),
                    int(values["spacing_x"]),
                    int(values["spacing_y"]),
                )
            else:
                raise ValueError(f"Unknown operation: {operation}")

            self.update_preview(input_path, self.input_preview, self.input_details)
            self.update_preview(output_path, self.output_preview, self.output_details)
            self.status_label.configure(
                text=f"Done. Saved processed image to {output_path}",
                text_color=("#2fa572", "#2fa572"),
            )
            self.pages.set("Preview")
        except (ValueError, OSError, TypeError) as error:
            messagebox.showerror("Could not process image", str(error), parent=self)
            self.status_label.configure(
                text="Processing failed. Check the file paths and option values.",
                text_color=("#d94f4f", "#ff6b6b"),
            )


if __name__ == "__main__":
    app = App()
    app.mainloop()
