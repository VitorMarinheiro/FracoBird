import pygame
import pygame.gfxdraw
import numpy as np

# Initialize pygame
pygame.init()

# Create a pygame window
window = pygame.display.set_mode((600, 400))

# Generate random data points
x = np.random.randint(1, 10, size=222)
y = np.random.randint(1, 1000, size=222)
print(y)

# Calculate the maximum Y value
max_y = max(y)

# Draw the chart on a surface
chart_surface = pygame.Surface((500, 100))
chart_surface.fill((255, 255, 255))
for i in range(len(x)-1):
    x1 = i*100
    y1 = int(100 - (y[i] / max_y) * 80)
    x2 = (i+1)*100
    y2 = int(100 - (y[i+1] / max_y) * 80)
    pygame.gfxdraw.line(chart_surface, x1, y1, x2, y2, (0, 0, 255))

# Blit the chart surface onto the main pygame window
window.blit(chart_surface, (50, 150))

# Update the display
pygame.display.update()

# Run the pygame main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
