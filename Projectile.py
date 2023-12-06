import pygame
import sys
import math

# Initialize pygame
pygame.init()

# Set window size
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Projectile Simulator")

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Define object parameters
mass = 10.0  # Object mass
gravity = 9.8  # Gravity acceleration

# Define initial conditions
initial_velocity = 30.0
launch_angle = math.radians(80)  # Launch angle

# Calculate horizontal and vertical velocity components
initial_velocity_x = initial_velocity * math.cos(launch_angle)
initial_velocity_y = initial_velocity * math.sin(launch_angle)

# Define time interval
time_interval = 0.1

# Initialize landing point coordinates, maximum height, and energy consumed
landing_point_x = 0
landing_point_y = 0
max_height = 0
energy_consumed = 0

# Initialize trajectory points
trajectory_points = []

# Simulate projectile motion
step = 0
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update position
    position_x = int(initial_velocity_x * step * time_interval)
    position_y = int(
        (initial_velocity_y * step * time_interval)
        - (0.5 * gravity * (step * time_interval) ** 2)
    )

    # Check if the particle has reached the ground
    if position_y < 0:
        position_y = 0
        velocity_x = 0
        velocity_y = 0
        running = False

    # Calculate landing point coordinates
    if position_y >= 0:
        landing_point_x = position_x
        landing_point_y = position_y

    # Calculate maximum height
    if position_y > max_height:
        max_height = position_y

    # Calculate energy consumed
    energy_consumed = mass * gravity * max_height

    # Append current position to the trajectory points
    trajectory_points.append((position_x, height - position_y))

    # Clear the screen
    screen.fill(white)

    # Draw the projectile path
    pygame.draw.circle(screen, red, (position_x, height - position_y), 10)

    # Draw trajectory line
    if len(trajectory_points) > 1:
        pygame.draw.lines(screen, black, False, trajectory_points, 2)

    # Display numerical information
    font = pygame.font.Font(None, 36)
    angle_text = font.render(
        f"Angle: {math.degrees(launch_angle):.2f} degrees", True, black
    )
    landing_point_text = font.render(
        f"Landing Point: ({landing_point_x}, {landing_point_y})", True, black
    )
    max_height_text = font.render(f"Max Height: {max_height} m", True, black)
    energy_consumed_text = font.render(
        f"Energy Consumed: {energy_consumed:.2f} J", True, black
    )

    screen.blit(angle_text, (10, 10))
    screen.blit(landing_point_text, (10, 50))
    screen.blit(max_height_text, (10, 90))
    screen.blit(energy_consumed_text, (10, 130))

    # Update the screen
    pygame.display.flip()

    # Control frame rate
    pygame.time.Clock().tick(30)
    step += 1


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
