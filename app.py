from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

app = Flask(__name__)

os.makedirs("output", exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form["quote"]
        text_color = request.form["color"]

        # Image settings
        image_width = 1080
        image_height = 1080
        font_size = 48

        # Load background
        background = Image.open("backgrounds/bg.jpg")
        background = background.resize((image_width, image_height))
        draw = ImageDraw.Draw(background)

        # Font
        font_path = r"C:\Windows\Fonts\arial.ttf"
        font = ImageFont.truetype(font_path, font_size)

        # Wrap text
        wrapped_text = textwrap.fill(text, width=30)

        bbox = draw.textbbox((0, 0), wrapped_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (image_width - text_width) // 2
        y = (image_height - text_height) // 2

        # Draw text
        draw.text((x, y), wrapped_text, fill=text_color, font=font, align="center")

        output_path = "output/quote.png"
        background.save(output_path)

        return send_file(output_path, as_attachment=True)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
