from PIL import Image, ImageDraw

def create_icon():
    size = (256, 256)
    # Create a new image with a transparent background
    image = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw a red circle (YouTube style)
    circle_center = (128, 128)
    circle_radius = 120
    draw.ellipse(
        [
            (circle_center[0] - circle_radius, circle_center[1] - circle_radius),
            (circle_center[0] + circle_radius, circle_center[1] + circle_radius),
        ],
        fill="#FF0000",
        outline=None
    )

    # Draw a white play triangle
    triangle_points = [(85, 70), (85, 186), (190, 128)]
    draw.polygon(triangle_points, fill="white")

    # Draw a musical note (simple representation)
    # Let's add a small musical note in the corner or overlay
    # Actually, let's keep it simple: Red Circle + Play Button is very recognizable.
    # Maybe add a small note icon in blue or black to signify MP3?
    # Let's draw a simple beam note in the bottom right
    
    note_color = "#333333"
    # Stem 1
    draw.rectangle([160, 140, 170, 200], fill=note_color)
    # Stem 2
    draw.rectangle([200, 130, 210, 190], fill=note_color)
    # Beam
    draw.polygon([(160, 140), (210, 130), (210, 150), (160, 160)], fill=note_color)
    # Head 1
    draw.ellipse([150, 190, 180, 210], fill=note_color)
    # Head 2
    draw.ellipse([190, 180, 220, 200], fill=note_color)

    # Save as PNG
    image.save("icon.png")
    
    # Save as ICO (for Windows)
    image.save("icon.ico", format="ICO", sizes=[(256, 256)])
    
    print("Icons created: icon.png, icon.ico")

if __name__ == "__main__":
    create_icon()
