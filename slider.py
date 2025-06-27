# slider.py
import pygame

class Slider:
    def __init__(self, x, y, width, min_value=1, max_value=10, knob_color=(0,120,255)):
        self.x = x
        self.y = y
        self.knob_color = knob_color
        self.width = width
        self.min_value = min_value
        self.max_value = max_value
        self.steps = max_value - min_value
        self.step_width = width // self.steps
        self.knob_radius = 15
        self.knob_x = self.x + self.step_width * ((self.max_value - self.min_value) // 2)
        self.dragging = False
        self.font = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if abs(mx - self.knob_x) <= self.knob_radius and abs(my - self.y) <= self.knob_radius:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.knob_x = self.snap_to_nearest_step(self.knob_x)

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx, _ = pygame.mouse.get_pos()
            self.knob_x = max(self.x, min(mx, self.x + self.width))


    def set_knob_color(self,color):
        self.knob_color = color


    def snap_to_nearest_step(self, pos_x):
        relative_x = pos_x - self.x
        step_index = round(relative_x / self.step_width)
        step_index = max(0, min(step_index, self.steps))
        return self.x + step_index * self.step_width

    def draw(self, surface ):
        pygame.draw.line(surface, (180, 180, 180), (self.x, self.y), (self.x + self.width, self.y), 4)
        for i in range(self.steps + 1):
            tick_x = self.x + i * self.step_width
            pygame.draw.line(surface, (100, 100, 100), (tick_x, self.y - 10), (tick_x, self.y + 10), 2)
        pygame.draw.circle(surface, self.knob_color, (self.knob_x, self.y), self.knob_radius)

        # Value display
        value_text = self.font.render(f"Value: {self.get_value()}", True, (255, 255, 255))
        surface.blit(value_text, (self.x, self.y + 30))

    def get_value(self):
        return self.min_value + round((self.knob_x - self.x) / self.step_width)
