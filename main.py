import random
import sys
import asyncio

IS_WEB = sys.platform == "emscripten"

class Game3D2048:
    def __init__(self, size_x=4, size_y=4, size_z=2):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.grid = self.create_empty_grid()
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def create_empty_grid(self):
        return [[[0 for _ in range(self.size_z)] for _ in range(self.size_y)] for _ in range(self.size_x)]

    def add_random_tile(self):
        empty_cells = []
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    if self.grid[x][y][z] == 0:
                        empty_cells.append((x, y, z))

        if empty_cells:
            x, y, z = random.choice(empty_cells)
            self.grid[x][y][z] = 2 if random.random() < 0.9 else 4
            return True
        return False

    def _move_and_merge_line(self, line):
        # Remove zeros and slide
        new_line = [tile for tile in line if tile != 0]
        # Merge tiles
        i = 0
        while i < len(new_line) - 1:
            if new_line[i] == new_line[i+1]:
                new_line[i] *= 2
                self.score += new_line[i]
                new_line.pop(i+1)
            i += 1
        # Add zeros back
        return new_line + [0] * (len(line) - len(new_line))



    def move_left(self):
        moved = False
        for x in range(self.size_x):
            for z in range(self.size_z):
                original_line = [self.grid[x][y][z] for y in range(self.size_y)]
                new_line = self._move_and_merge_line(original_line)
                if original_line != new_line:
                    moved = True
                    for y in range(self.size_y):
                        self.grid[x][y][z] = new_line[y]
        return moved

    def move_right(self):
        moved = False
        for x in range(self.size_x):
            for z in range(self.size_z):
                original_line = [self.grid[x][y][z] for y in range(self.size_y)]
                reversed_line = original_line[::-1]  # Reverse to simulate moving right
                new_line_reversed = self._move_and_merge_line(reversed_line)
                if reversed_line != new_line_reversed:
                    moved = True
                    new_line = new_line_reversed[::-1]  # Reverse back
                    for y in range(self.size_y):
                        self.grid[x][y][z] = new_line[y]
        return moved

    def move_up(self):
        moved = False
        for y in range(self.size_y):
            for z in range(self.size_z):
                original_line = [self.grid[x][y][z] for x in range(self.size_x)]
                new_line = self._move_and_merge_line(original_line)
                if original_line != new_line:
                    moved = True
                    for x in range(self.size_x):
                        self.grid[x][y][z] = new_line[x]
        return moved

    def move_down(self):
        moved = False
        for y in range(self.size_y):
            for z in range(self.size_z):
                original_line = [self.grid[x][y][z] for x in range(self.size_x)]
                reversed_line = original_line[::-1]  # Reverse to simulate moving down
                new_line_reversed = self._move_and_merge_line(reversed_line)
                if reversed_line != new_line_reversed:
                    moved = True
                    new_line = new_line_reversed[::-1]  # Reverse back
                    for x in range(self.size_x):
                        self.grid[x][y][z] = new_line[x]
        return moved

    def move_front(self):
        moved = False
        for x in range(self.size_x):
            for y in range(self.size_y):
                original_line = [self.grid[x][y][z] for z in range(self.size_z)]
                new_line = self._move_and_merge_line(original_line)
                if original_line != new_line:
                    moved = True
                    for z in range(self.size_z):
                        self.grid[x][y][z] = new_line[z]
        return moved

    def move_back(self):
        moved = False
        for x in range(self.size_x):
            for y in range(self.size_y):
                original_line = [self.grid[x][y][z] for z in range(self.size_z)]
                reversed_line = original_line[::-1]  # Reverse to simulate moving back
                new_line_reversed = self._move_and_merge_line(reversed_line)
                if reversed_line != new_line_reversed:
                    moved = True
                    new_line = new_line_reversed[::-1]  # Reverse back
                    for z in range(self.size_z):
                        self.grid[x][y][z] = new_line[z]
        return moved

    def has_valid_moves(self):
        # Check for empty cells
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    if self.grid[x][y][z] == 0:
                        return True

        # Check for possible merges (horizontal, vertical, depth)
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    current_tile = self.grid[x][y][z]
                    # Check right
                    if y + 1 < self.size_y and current_tile == self.grid[x][y+1][z]:
                        return True
                    # Check down
                    if x + 1 < self.size_x and current_tile == self.grid[x+1][y][z]:
                        return True
                    # Check back (deeper)
                    if z + 1 < self.size_z and current_tile == self.grid[x][y][z+1]:
                        return True
        return False

    def game_over(self):
        return not self.has_valid_moves()

    def print_grid(self):
        for z in range(self.size_z):
            print(f"Layer {z + 1}:")
            for x in range(self.size_x):
                print(" ".join(str(self.grid[x][y][z]).rjust(4) for y in range(self.size_y)))
            print()

import pygame
import math

# --- Pygame UI Constants ---
SCREEN_WIDTH = 1010
SCREEN_HEIGHT = 600
GRID_SIZE = 4
TILE_SIZE = 60
GRID_MARGIN = 10
GRID_WIDTH = GRID_HEIGHT = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GRID_MARGIN

# 3D View Constants
VIEW_WIDTH = 400
VIEW_HEIGHT = 400
CUBE_SIZE = 40
LAYER_CENTER_SPACING = 3.5
ROTATION_SPEED = 0.01
MAX_VERTICAL_ANGLE = math.radians(30)
INITIAL_HORIZONTAL_ANGLE = math.radians(-35)
INITIAL_VERTICAL_ANGLE = math.radians(20)

# Colors
BG_COLOR = (187, 173, 160)
GRID_BG_COLOR = (205, 193, 180)
TILE_COLORS = {
    0: (218, 209, 199),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
TEXT_COLOR_DARK = (119, 110, 101)
TEXT_COLOR_LIGHT = (249, 246, 242)
POPUP_BG_COLOR = (250, 248, 239)
POPUP_BORDER_COLOR = (187, 173, 160)
BUTTON_BG_COLOR = (143, 122, 102)
BUTTON_HOVER_COLOR = (159, 138, 118)
STRIPE_COLOR_DARK = (119, 110, 101)
STRIPE_COLOR_LIGHT = (249, 246, 242)

class GameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("3D 2048")
        self.score_font = pygame.font.Font(None, 36)
        self.tile_font = pygame.font.Font(None, 55)
        self.game_over_font = pygame.font.Font(None, 72)
        self.popup_font = pygame.font.Font(None, 40)
        self.button_font = pygame.font.Font(None, 34)
        self.key_map_font = pygame.font.Font(None, 24)
        self.angle_x = INITIAL_VERTICAL_ANGLE
        self.angle_y = INITIAL_HORIZONTAL_ANGLE
        self.zoom = 8
        self.mouse_dragging = False
        self.last_mouse_pos = (0, 0)
        self.running = True
        self.game_over = False
        self.try_again_button = pygame.Rect(0, 0, 180, 52)
        self.game = None
        self.restart_game()

    def restart_game(self):
        self.game = Game3D2048()
        self.game_over = self.game.game_over()
        self.angle_x = INITIAL_VERTICAL_ANGLE
        self.angle_y = INITIAL_HORIZONTAL_ANGLE
        self.mouse_dragging = False
        self.last_mouse_pos = (0, 0)

    def draw_grid(self, surface, grid_data, start_x, start_y, layer_index):
        pygame.draw.rect(surface, GRID_BG_COLOR, (start_x, start_y, GRID_WIDTH, GRID_HEIGHT))
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                tile_value = grid_data[r][c]
                striped = self.can_merge_front_back_at(r, c, layer_index)
                self.draw_tile(surface, tile_value, r, c, start_x, start_y, striped=striped)

    def can_merge_front_back_at(self, x, y, z):
        value = self.game.grid[x][y][z]
        if value == 0:
            return False

        if z > 0 and self.game.grid[x][y][z - 1] == value:
            return True
        if z + 1 < self.game.size_z and self.game.grid[x][y][z + 1] == value:
            return True
        return False

    def draw_tile_stripes(self, surface, tile_rect, stripe_color):
        stripe_spacing = 20
        previous_clip = surface.get_clip()
        surface.set_clip(tile_rect)

        for offset in range(-tile_rect.height, tile_rect.width, stripe_spacing):
            start_pos = (tile_rect.x + offset, tile_rect.bottom)
            end_pos = (tile_rect.x + offset + tile_rect.height, tile_rect.y)
            pygame.draw.line(surface, stripe_color, start_pos, end_pos, 2)

        surface.set_clip(previous_clip)

    def draw_tile(self, surface, value, row, col, start_x, start_y, striped=False):
        x = start_x + GRID_MARGIN * (col + 1) + TILE_SIZE * col
        y = start_y + GRID_MARGIN * (row + 1) + TILE_SIZE * row
        color = TILE_COLORS.get(value, TILE_COLORS[2048])
        tile_rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, color, tile_rect)

        if value != 0:
            text_color = TEXT_COLOR_DARK if value in [2, 4] else TEXT_COLOR_LIGHT
            if striped:
                stripe_color = STRIPE_COLOR_DARK if text_color == TEXT_COLOR_DARK else STRIPE_COLOR_LIGHT
                self.draw_tile_stripes(surface, tile_rect, stripe_color)
            text = self.tile_font.render(str(value), True, text_color)
            text_rect = text.get_rect(center=(x + TILE_SIZE / 2, y + TILE_SIZE / 2))
            surface.blit(text, text_rect)

    def project_3d_to_2d(self, x, y, z):
        # Rotate around Y-axis
        x, z = x * math.cos(self.angle_y) - z * math.sin(self.angle_y), x * math.sin(self.angle_y) + z * math.cos(self.angle_y)
        # Rotate around X-axis
        y, z = y * math.cos(self.angle_x) - z * math.sin(self.angle_x), y * math.sin(self.angle_x) + z * math.cos(self.angle_x)

        # Apply perspective and scale
        factor = self.zoom / (z + 10)
        x = x * factor * CUBE_SIZE + VIEW_WIDTH / 2
        y = y * factor * CUBE_SIZE + VIEW_HEIGHT / 2
        return int(x), int(y)

    def draw_dotted_line(self, surface, color, start_pos, end_pos, dash_length=4, gap_length=4):
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)
        if distance == 0:
            return

        dashes = int(distance / (dash_length + gap_length))
        if dashes == 0:
            pygame.draw.line(surface, color, start_pos, end_pos, 1)
            return

        for i in range(dashes):
            start = (start_pos[0] + (dx * (i * (dash_length + gap_length))) / distance,
                     start_pos[1] + (dy * (i * (dash_length + gap_length))) / distance)
            end = (start_pos[0] + (dx * (i * (dash_length + gap_length) + dash_length)) / distance,
                   start_pos[1] + (dy * (i * (dash_length + gap_length) + dash_length)) / distance)
            pygame.draw.line(surface, color, start, end, 1)

    def get_layer_center_z(self, layer_index):
        return (layer_index - (self.game.size_z - 1) / 2) * LAYER_CENTER_SPACING

    def draw_grid_frame(self, surface):
        grid_line_color = (255, 255, 255)  # White for grid lines
        
        x_planes = [i - self.game.size_y / 2 - 0.5 for i in range(self.game.size_y + 1)]
        y_planes = [i - self.game.size_x / 2 - 0.5 for i in range(self.game.size_x + 1)]
        layer_planes = [
            (self.get_layer_center_z(layer_index) - 0.5, self.get_layer_center_z(layer_index) + 0.5)
            for layer_index in range(self.game.size_z)
        ]
        z_planes = [z for planes in layer_planes for z in planes]

        # Lines along X
        for y in y_planes:
            for z in z_planes:
                start_3d = (x_planes[0], y, z)
                end_3d = (x_planes[-1], y, z)
                self.draw_dotted_line(surface, grid_line_color, self.project_3d_to_2d(*start_3d), self.project_3d_to_2d(*end_3d))

        # Lines along Y
        for x in x_planes:
            for z in z_planes:
                start_3d = (x, y_planes[0], z)
                end_3d = (x, y_planes[-1], z)
                self.draw_dotted_line(surface, grid_line_color, self.project_3d_to_2d(*start_3d), self.project_3d_to_2d(*end_3d))

        # Lines along Z
        for x in x_planes:
            for y in y_planes:
                for z_start, z_end in layer_planes:
                    self.draw_dotted_line(
                        surface,
                        grid_line_color,
                        self.project_3d_to_2d(x, y, z_start),
                        self.project_3d_to_2d(x, y, z_end),
                    )

    def draw_key_mappings(self, surface):
        key_mappings = [
            "Controls:",
            "- Arrows / WASD: Move on plane",
            "- Q / E: Move between planes (Front/Back)",
            "- Mouse Drag: Rotate 3D view"
        ]
        y_offset = 420
        for line in key_mappings:
            text_surface = self.key_map_font.render(line, True, TEXT_COLOR_DARK)
            surface.blit(text_surface, (20, y_offset))
            y_offset += 25

    def get_cube_faces(self, x, y, z, value):
        # This function calculates and returns the faces of a single cube
        row = x
        col = y
        x = col - self.game.size_y / 2
        y = row - self.game.size_x / 2
        z_centered = self.get_layer_center_z(z)

        vertices = [
            (x - 0.5, y - 0.5, z_centered - 0.5), (x + 0.5, y - 0.5, z_centered - 0.5),
            (x + 0.5, y + 0.5, z_centered - 0.5), (x - 0.5, y + 0.5, z_centered - 0.5),
            (x - 0.5, y - 0.5, z_centered + 0.5), (x + 0.5, y - 0.5, z_centered + 0.5),
            (x + 0.5, y + 0.5, z_centered + 0.5), (x - 0.5, y + 0.5, z_centered + 0.5)
        ]

        rotated_vertices = []
        for vx, vy, vz in vertices:
            vx_r, vz_r = vx * math.cos(self.angle_y) - vz * math.sin(self.angle_y), vx * math.sin(self.angle_y) + vz * math.cos(self.angle_y)
            vy_r, vz_r = vy * math.cos(self.angle_x) - vz_r * math.sin(self.angle_x), vy * math.sin(self.angle_x) + vz_r * math.cos(self.angle_x)
            rotated_vertices.append((vx_r, vy_r, vz_r))

        base_color = TILE_COLORS.get(value, TILE_COLORS[2048])
        dark_color = tuple(max(0, c - 50) for c in base_color)
        light_color = tuple(min(255, c + 30) for c in base_color)

        face_definitions = [
            ((0, 1, 2, 3), base_color),
            ((4, 5, 6, 7), dark_color),
            ((0, 1, 5, 4), light_color),
            ((2, 3, 7, 6), dark_color),
            ((0, 3, 7, 4), dark_color),
            ((1, 2, 6, 5), base_color),
        ]

        cube_faces = []
        for face, color in face_definitions:
            avg_z = sum(rotated_vertices[j][2] for j in face) / 4
            projected_points = []
            for j in face:
                vx, vy, vz = rotated_vertices[j]
                factor = self.zoom / (vz + 10)
                px = vx * factor * CUBE_SIZE + VIEW_WIDTH / 2
                py = vy * factor * CUBE_SIZE + VIEW_HEIGHT / 2
                projected_points.append((px, py))
            cube_faces.append((projected_points, color, avg_z))
        return cube_faces

    def draw_3d_grid(self, surface, start_x, start_y):
        view_surface = pygame.Surface((VIEW_WIDTH, VIEW_HEIGHT))
        view_surface.fill((51, 51, 51))  # Dark gray background

        self.draw_grid_frame(view_surface)

        all_faces = []
        for x in range(self.game.size_x):
            for y in range(self.game.size_y):
                for z in range(self.game.size_z):
                    value = self.game.grid[x][y][z]
                    if value != 0:
                        all_faces.extend(self.get_cube_faces(x, y, z, value))

        # Draw farthest faces first so nearer cubes occlude them.
        all_faces.sort(key=lambda f: f[2], reverse=True)

        for points, color, _ in all_faces:
            pygame.draw.polygon(view_surface, color, points)
        
        surface.blit(view_surface, (start_x, start_y))

    def _handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.game_over and self.try_again_button.collidepoint(event.pos):
                    self.restart_game()
                    return
                if self.game_over:
                    return
                self.mouse_dragging = True
                self.last_mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.mouse_dragging:
                dx = event.pos[0] - self.last_mouse_pos[0]
                dy = event.pos[1] - self.last_mouse_pos[1]
                self.angle_y += dx * ROTATION_SPEED
                self.angle_x -= dy * ROTATION_SPEED
                self.angle_x = max(-MAX_VERTICAL_ANGLE, min(MAX_VERTICAL_ANGLE, self.angle_x))
                self.last_mouse_pos = event.pos

        if event.type == pygame.KEYDOWN and not self.game_over:
            moved = False
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                moved = self.game.move_left()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                moved = self.game.move_right()
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                moved = self.game.move_up()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                moved = self.game.move_down()
            elif event.key == pygame.K_q:
                moved = self.game.move_front()
            elif event.key == pygame.K_e:
                moved = self.game.move_back()

            if moved:
                self.game.add_random_tile()
            self.game_over = self.game.game_over()

    def _draw_game_over_popup(self):
        popup_width = 320
        popup_height = 220
        popup_rect = pygame.Rect(
            (SCREEN_WIDTH - popup_width) // 2,
            (SCREEN_HEIGHT - popup_height) // 2,
            popup_width,
            popup_height,
        )

        pygame.draw.rect(self.screen, POPUP_BG_COLOR, popup_rect, border_radius=18)
        pygame.draw.rect(self.screen, POPUP_BORDER_COLOR, popup_rect, 3, border_radius=18)

        title_text = self.game_over_font.render("Game Over!", True, TEXT_COLOR_DARK)
        title_rect = title_text.get_rect(center=(popup_rect.centerx, popup_rect.y + 56))
        self.screen.blit(title_text, title_rect)

        score_text = self.popup_font.render(f"Score: {self.game.score}", True, TEXT_COLOR_DARK)
        score_rect = score_text.get_rect(center=(popup_rect.centerx, popup_rect.y + 112))
        self.screen.blit(score_text, score_rect)

        self.try_again_button = pygame.Rect(0, 0, 180, 52)
        self.try_again_button.center = (popup_rect.centerx, popup_rect.y + 170)
        is_hovered = self.try_again_button.collidepoint(pygame.mouse.get_pos())
        button_color = BUTTON_HOVER_COLOR if is_hovered else BUTTON_BG_COLOR

        pygame.draw.rect(self.screen, button_color, self.try_again_button, border_radius=12)
        button_text = self.button_font.render("Try again", True, TEXT_COLOR_LIGHT)
        button_rect = button_text.get_rect(center=self.try_again_button.center)
        self.screen.blit(button_text, button_rect)

    def _draw_frame(self):
        self.screen.fill(BG_COLOR)

        score_text = self.score_font.render(f"Score: {self.game.score}", True, TEXT_COLOR_DARK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 30))
        self.screen.blit(score_text, score_rect)

        grid_y_pos = 100
        self.draw_grid(self.screen, [[self.game.grid[r][c][0] for c in range(self.game.size_y)] for r in range(self.game.size_x)], GRID_MARGIN, grid_y_pos, 0)
        self.draw_grid(self.screen, [[self.game.grid[r][c][1] for c in range(self.game.size_y)] for r in range(self.game.size_x)], GRID_WIDTH + GRID_MARGIN * 2, grid_y_pos, 1)

        self.draw_3d_grid(self.screen, GRID_WIDTH * 2 + GRID_MARGIN * 3, (SCREEN_HEIGHT - VIEW_HEIGHT) // 2)
        self.draw_key_mappings(self.screen)

        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((238, 228, 218, 128))
            self.screen.blit(overlay, (0, 0))
            self._draw_game_over_popup()

        pygame.display.flip()

    def _shutdown(self):
        pygame.quit()
        if not IS_WEB:
            sys.exit()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                self._handle_event(event)
            self._draw_frame()

        self._shutdown()

    async def run_web(self):
        while self.running:
            for event in pygame.event.get():
                self._handle_event(event)
            self._draw_frame()
            await asyncio.sleep(0)

        self._shutdown()


if __name__ == "__main__":
    ui = GameUI()
    if IS_WEB:
        asyncio.run(ui.run_web())
    else:
        ui.run()
