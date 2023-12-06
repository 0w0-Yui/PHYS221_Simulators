import pygame
import sys
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Constants
width, height = 800, 600
gravity = 9.8
friction = 0.0

# Colors
white = (255, 255, 255)
black = (0, 0, 0)


# Function to calculate kinetic energy
def kinetic_energy(mass, velocity):
    return 0.5 * mass * velocity**2


# Function to calculate potential energy
def potential_energy(mass, height):
    return mass * gravity * height


# Particle class
class Particle(pygame.sprite.Sprite):
    def __init__(self, mass, initial_height):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, initial_height)
        self.mass = mass
        self.velocity = 0
        self.height = initial_height
        self.landed = False
        self.fall_time = 0

    def update(self):
        if not self.landed:
            # Calculate forces
            conservative_force = self.mass * gravity
            non_conservative_force = -friction * self.velocity

            # Calculate acceleration
            acceleration = (conservative_force + non_conservative_force) / self.mass

            # Update velocity and position
            self.velocity += acceleration
            self.height += self.velocity

            if self.height >= height:
                self.height = height
                self.velocity = 0
                self.landed = True
                self.fall_time = (
                    pygame.time.get_ticks() / 1000
                )  # Convert milliseconds to seconds

        self.rect.y = self.height


# Set up the screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Free Fall Simulator")

# Create a particle with initial mass and height
initial_mass = 1
initial_height = 50
particle = Particle(mass=initial_mass, initial_height=initial_height)

# Create a sprite group
all_sprites = pygame.sprite.Group()
all_sprites.add(particle)

# Lists to store kinetic and potential energy values
kinetic_energy_values = []
potential_energy_values = []
velocity_values = []
conservative_force_values = []
non_conservative_force_values = []

# Main game loop
clock = pygame.time.Clock()
frame_rate = 5  # Increase the frame rate
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update
    all_sprites.update()

    # Record kinetic and potential energy values
    kinetic_energy_values.append(kinetic_energy(particle.mass, particle.velocity))
    potential_energy_values.append(
        potential_energy(particle.mass, height - particle.height)
    )
    velocity_values.append(particle.velocity)
    conservative_force_values.append(particle.mass * gravity)
    non_conservative_force_values.append(-friction * particle.velocity)

    # Draw
    screen.fill(white)
    all_sprites.draw(screen)

    # Display energies and forces
    kinetic_energy_text = (
        f"Kinetic Energy: {kinetic_energy(particle.mass, particle.velocity):.2f} J"
    )
    potential_energy_text = f"Potential Energy: {potential_energy(particle.mass, height - particle.height):.2f} J"
    velocity_text = f"Velocity: {particle.velocity:.2f} m/s"
    conservative_force_text = f"Conservative Force: {particle.mass * gravity:.2f} N"
    non_conservative_force_text = (
        f"Non-Conservative Force: {-friction * particle.velocity:.2f} N"
    )

    font = pygame.font.Font(None, 36)
    kinetic_energy_surface = font.render(kinetic_energy_text, True, black)
    potential_energy_surface = font.render(potential_energy_text, True, black)
    velocity_surface = font.render(velocity_text, True, black)
    conservative_force_surface = font.render(conservative_force_text, True, black)
    non_conservative_force_surface = font.render(
        non_conservative_force_text, True, black
    )

    screen.blit(kinetic_energy_surface, (10, 10))
    screen.blit(potential_energy_surface, (10, 50))
    screen.blit(velocity_surface, (10, 90))
    screen.blit(conservative_force_surface, (10, 130))
    screen.blit(non_conservative_force_surface, (10, 170))

    pygame.display.flip()
    clock.tick(frame_rate)

    # Check if the particle has landed
    if particle.landed:
        break

# Display the plot after the particle has landed
plt.figure(figsize=(8, 6))
plt.subplot(3, 1, 1)
plt.plot(kinetic_energy_values, label="Kinetic Energy")
plt.plot(potential_energy_values, label="Potential Energy")
plt.ylabel("Energy (Joules)")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(velocity_values, label="Velocity")
plt.ylabel("Velocity (m/s)")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(conservative_force_values, label="Conservative Force")
plt.plot(non_conservative_force_values, label="Non-Conservative Force")
plt.xlabel("Time (frames)")
plt.ylabel("Force (N)")
plt.legend()

plt.tight_layout()
plt.savefig("energy_and_forces_plot.png")  # Save the plot as an image (optional)
plt.show()
