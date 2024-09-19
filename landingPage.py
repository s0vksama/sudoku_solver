import pygame
import configuration as confi

pygame.init()

# Fonts
font = pygame.font.SysFont(None, 36)

# Function to load an image from a file path
def load_image(file_path):
    if os.path.exists(file_path):
        try:
            image = pygame.image.load(file_path)
            return pygame.transform.scale(image, (confi.screen_width, confi.screen_height))
        except pygame.error as e:
            print(f"Cannot load image: {e}")
    else:
        print("File does not exist.")
    return None

# Function to draw text
def draw_text(surface, text, position, color=confi.BLACK):
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, position)

# Function to create a button
def draw_button(surface, text, position, size, color, text_color=confi.BLACK):
    rect = pygame.Rect(position, size)
    pygame.draw.rect(surface, color, rect)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    surface.blit(text_surf, text_rect)
    return rect

# Main loop
running = True
uploaded_image = None

def landing_page_func(window):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = event.pos
                if upload_button.collidepoint(mouse_pos):  # Check if the button was clicked
                    # Open file dialog to choose an image
                    file_path = filedialog.askopenfilename(
                        title="Select an image",
                        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
                    )
                    if file_path:
                        uploaded_image = load_image(file_path)

    # Draw the upload button
    upload_button = draw_button(window, "Upload Image", (300, 250), (200, 50), confi.GRAY)

    # Display the uploaded image
    if uploaded_image:
        window.blit(uploaded_image, (0, 0))

    pygame.display.update()
