import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
INITIAL_BOUNDARY_RADIUS = 150
BOUNDARY_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
NUM_PARTICLES = 80  # Reduced for better performance with interactions
PARTICLE_RADIUS = 4
FPS = 60

# Force constants
ATTRACTION_STRENGTH = 10000  # Reduced from 50000 for gentler interactions
REPULSION_STRENGTH = 20000   # Reduced from 100000 for gentler interactions
REPULSION_DISTANCE = 20      # Distance below which particles repel
MAX_FORCE = 200              # Reduced from 1000 for gentler acceleration

# Expansion constants
EXPANSION_RATE = 60          # Increased expansion rate for more visible effect
HUBBLE_CONSTANT = 0.05       # Slightly increased Hubble constant

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
YELLOW = (255, 255, 100)
PURPLE = (255, 100, 255)

class Particle:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx  # velocity in x direction
        self.vy = vy  # velocity in y direction
        self.color = color
        self.radius = PARTICLE_RADIUS
        self.mass = 1.0  # Mass for force calculations
        
    def apply_expansion(self, dt):
        # Calculate expansion velocity (Hubble flow)
        # Recession velocity = Hubble constant * distance from center
        center_x, center_y = BOUNDARY_CENTER
        distance_from_center_x = self.x - center_x
        distance_from_center_y = self.y - center_y
        distance_from_center = math.sqrt(distance_from_center_x**2 + distance_from_center_y**2)
        
        if distance_from_center > 0:
            # Normalized direction from center
            norm_dx = distance_from_center_x / distance_from_center
            norm_dy = distance_from_center_y / distance_from_center
            
            # Hubble velocity: v = H * d (recession velocity proportional to distance)
            hubble_velocity = HUBBLE_CONSTANT * distance_from_center
            
            # Add Hubble velocity to particle velocity
            self.vx += hubble_velocity * norm_dx * dt
            self.vy += hubble_velocity * norm_dy * dt
        
    def apply_force(self, fx, fy, dt):
        # Apply force using F = ma (acceleration = force / mass)
        ax = fx / self.mass
        ay = fy / self.mass
        
        # Update velocity
        self.vx += ax * dt
        self.vy += ay * dt
        
        # Limit velocity to prevent extreme speeds
        speed = math.sqrt(self.vx * self.vx + self.vy * self.vy)
        max_speed = 100  # Reduced from 400 for slower movement
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed
        
    def update(self, dt, current_boundary_radius):
        # Update position based on velocity
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Check collision with circular boundary
        center_x, center_y = BOUNDARY_CENTER
        dx = self.x - center_x
        dy = self.y - center_y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # If particle hits boundary, bounce it back
        if distance + self.radius > current_boundary_radius:
            # Normalize the distance vector
            if distance > 0:
                dx /= distance
                dy /= distance
                
                # Move particle back inside boundary
                self.x = center_x + dx * (current_boundary_radius - self.radius)
                self.y = center_y + dy * (current_boundary_radius - self.radius)
                
                # Reflect velocity (bounce)
                # Dot product of velocity and normal vector
                dot_product = self.vx * dx + self.vy * dy
                
                # Reflect velocity across the normal
                self.vx -= 2 * dot_product * dx
                self.vy -= 2 * dot_product * dy
                
                # Add some energy damping to make it more realistic
                self.vx *= 0.95
                self.vy *= 0.95
    
    def calculate_force_from_others(self, all_particles):
        # Calculate total force from all other particles
        total_fx = 0
        total_fy = 0
        
        for other in all_particles:
            if other != self:  # Don't calculate force from self
                fx, fy = self.calculate_force_from(other)
                total_fx += fx
                total_fy += fy
        
        return total_fx, total_fy
    
    def calculate_force_from(self, other):
        # Calculate distance between particles
        dx = other.x - self.x
        dy = other.y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        # Avoid division by zero and self-interaction
        if distance < 0.1:
            return 0, 0
        
        # Normalize direction vector
        nx = dx / distance
        ny = dy / distance
        
        # Calculate force magnitude based on distance
        if distance < REPULSION_DISTANCE:
            # Repulsive force (inverse square law)
            force_magnitude = REPULSION_STRENGTH / (distance * distance)
            # Repulsion: force points away from other particle
            force_magnitude = -force_magnitude
        else:
            # Attractive force (inverse square law)
            force_magnitude = ATTRACTION_STRENGTH / (distance * distance)
        
        # Limit force to prevent explosive behavior
        force_magnitude = max(-MAX_FORCE, min(MAX_FORCE, force_magnitude))
        
        # Calculate force components
        fx = force_magnitude * nx
        fy = force_magnitude * ny
        
        return fx, fy
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

class ParticleSimulator:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Expanding Universe Particle Simulator")
        self.clock = pygame.time.Clock()
        self.particles = []
        self.running = True
        
        # Universe expansion tracking
        self.current_boundary_radius = INITIAL_BOUNDARY_RADIUS
        self.initial_boundary_radius = INITIAL_BOUNDARY_RADIUS
        self.universe_age = 0.0  # Age of universe in seconds
        
        # Create random particles
        self.create_particles()
        
    def create_particles(self):
        colors = [BLUE, RED, GREEN, YELLOW, PURPLE]
        
        # Reset universe expansion
        self.current_boundary_radius = INITIAL_BOUNDARY_RADIUS
        self.initial_boundary_radius = INITIAL_BOUNDARY_RADIUS
        self.universe_age = 0.0
        
        for _ in range(NUM_PARTICLES):
            # Generate random position inside the initial circle
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(0, INITIAL_BOUNDARY_RADIUS - PARTICLE_RADIUS - 50)  # Keep away from edges
            
            x = BOUNDARY_CENTER[0] + radius * math.cos(angle)
            y = BOUNDARY_CENTER[1] + radius * math.sin(angle)
            
            # Much smaller random velocity for better expansion visibility
            vx = random.uniform(-20, 20)  # Reduced from -50,50
            vy = random.uniform(-20, 20)
            
            # Random color
            color = random.choice(colors)
            
            particle = Particle(x, y, vx, vy, color)
            self.particles.append(particle)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset simulation
                    self.particles.clear()
                    self.create_particles()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self, dt):
        # Update universe age and expansion
        self.universe_age += dt
        self.current_boundary_radius = self.initial_boundary_radius + (EXPANSION_RATE * self.universe_age)
        
        # Limit expansion to screen size
        max_radius = min(SCREEN_WIDTH, SCREEN_HEIGHT) // 2 - 20
        if self.current_boundary_radius > max_radius:
            self.current_boundary_radius = max_radius
        
        # Apply expansion to all particles (adds Hubble flow velocity)
        for particle in self.particles:
            particle.apply_expansion(dt)
        
        # Calculate forces from all other particles
        for particle in self.particles:
            fx, fy = particle.calculate_force_from_others(self.particles)
            particle.apply_force(fx, fy, dt)
        
        # Update all particles
        for particle in self.particles:
            particle.update(dt, self.current_boundary_radius)
    
    def draw(self):
        # Clear screen
        self.screen.fill(BLACK)
        
        # Draw boundary circle (expanding universe)
        pygame.draw.circle(self.screen, WHITE, BOUNDARY_CENTER, int(self.current_boundary_radius), 2)
        
        # Draw a faded circle showing the original size
        if self.current_boundary_radius > self.initial_boundary_radius:
            pygame.draw.circle(self.screen, (60, 60, 60), BOUNDARY_CENTER, int(self.initial_boundary_radius), 1)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw universe information
        font = pygame.font.Font(None, 24)
        text1 = font.render("SPACE: Reset | ESC: Quit", True, WHITE)
        text2 = font.render(f"Particles: {len(self.particles)}", True, WHITE)
        text3 = font.render(f"Universe Age: {self.universe_age:.1f}s", True, WHITE)
        text4 = font.render(f"Universe Radius: {self.current_boundary_radius:.0f}px", True, WHITE)
        text5 = font.render(f"Expansion Rate: {EXPANSION_RATE}px/s", True, WHITE)
        
        self.screen.blit(text1, (10, 10))
        self.screen.blit(text2, (10, 35))
        self.screen.blit(text3, (10, 60))
        self.screen.blit(text4, (10, 85))
        self.screen.blit(text5, (10, 110))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            # Calculate delta time in seconds
            dt = self.clock.tick(FPS) / 1000.0
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()

# Run the simulation
if __name__ == "__main__":
    simulator = ParticleSimulator()
    simulator.run()