import logging
from enum import Enum
from typing import List, Tuple, Set, Dict, Optional
import time
import os
import heapq
from dataclasses import dataclass
from collections import deque
import random
import pygame
import math
from typing import List, Tuple, Optional
from enum import Enum
from Visualizer.Greedy_unwrap import Greedy
from Visualizer.DFS_unwrap import DFS
from Visualizer.Greedy_wrap import Greedy_wrap
from Visualizer.DFS_wrap import DFS_wrap

# Initialize Pygame
pygame.init()
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PipeVisualizer:
    def __init__(self, cell_size: int = 60):
        self.cell_size = cell_size
        self.pipe_width = cell_size * 8 // 60
        self.colors = {
            'background': (30, 30, 30),     # Dark gray
            'pipe': (100, 149, 237),        # Cornflower blue
            'start': (220, 20, 60),         # Crimson red
            'end': (100, 149, 237),         # Same as pipe color
            'grid': (70, 70, 70),           # Grid lines
            'wrap_indicator': (200, 200, 200)  # Light gray for wrap indicators
        }

    def handle_resize(self, screen: pygame.Surface, width: int, height: int, grid) -> pygame.Surface:
        new_cell_size_w = (width - 100) // grid.width
        new_cell_size_h = (height - 100) // grid.height
        new_cell_size = min(new_cell_size_w, new_cell_size_h)
        new_cell_size = max(min(new_cell_size, self.max_cell_size), self.min_cell_size)
        self.cell_size = new_cell_size
        new_width = grid.width * self.cell_size + 100
        new_height = grid.height * self.cell_size + 100
        return pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    def draw_grid(self, screen: pygame.Surface, grid) -> None:
        padding = 30
        screen.fill(self.colors['background'])
        
        # Draw grid lines
        for x in range(grid.width + 1):
            pygame.draw.line(screen, self.colors['grid'], 
                            (x * self.cell_size + padding, padding), 
                            (x * self.cell_size + padding, grid.height * self.cell_size + padding))
        for y in range(grid.height + 1):
            pygame.draw.line(screen, self.colors['grid'], 
                            (padding, y * self.cell_size + padding), 
                            (grid.width * self.cell_size + padding, y * self.cell_size + padding))
        
        # Draw pipes
        for y in range(grid.height):
            for x in range(grid.width):
                pipe = grid.get_pipe(x, y)
                if pipe and pipe.pipe_type != PipeType.EMPTY:
                    self.draw_pipe(screen, x, y, pipe)
                        
        self.draw_wrap_indicators(screen, grid, padding)
        pygame.display.flip()

    def draw_pipe(self, screen: pygame.Surface, x: int, y: int, pipe) -> None:
        padding = 30
        center_x = x * self.cell_size + self.cell_size // 2 + padding
        center_y = y * self.cell_size + self.cell_size // 2 + padding
        radius = self.cell_size // 2.2
        
        color = self.colors['start'] if pipe.is_start else self.colors['pipe']
        
        if pipe.is_end:
            # Draw center circle for END pipe
            pygame.draw.circle(screen, color, (center_x, center_y), self.pipe_width * 1.5)
            # Draw connection line
            direction = next(iter(pipe.get_all_connections()))
            end_x = center_x
            end_y = center_y
            if direction == 0: end_y -= radius
            elif direction == 1: end_x += radius
            elif direction == 2: end_y += radius
            else: end_x -= radius
            pygame.draw.line(screen, color, (center_x, center_y), (end_x, end_y), self.pipe_width)
            return
        
        # Draw normal pipe connections
        connections = pipe.get_all_connections()
        for direction in connections:
            end_x = center_x
            end_y = center_y
            if direction == 0: end_y -= radius
            elif direction == 1: end_x += radius
            elif direction == 2: end_y += radius
            else: end_x -= radius
            pygame.draw.line(screen, color, (center_x, center_y), (end_x, end_y), self.pipe_width)
        
        if pipe.is_start:
            pygame.draw.circle(screen, color, (center_x, center_y), self.pipe_width * 2)
        elif pipe.pipe_type in [PipeType.TEE, PipeType.CROSS]:
            pygame.draw.circle(screen, color, (center_x, center_y), self.pipe_width)

    def create_window(self, width: int, height: int) -> pygame.Surface:
        """Create Pygame window based on grid size."""
        padding = 30  # Padding for wrap indicators
        window_width = width * self.cell_size + (padding * 2)
        window_height = height * self.cell_size + (padding * 2)
        screen = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption("Pipe Puzzle Solver")
        return screen

    def draw_wrap_indicators(self, screen: pygame.Surface, grid, padding: int) -> None:
        """Draw wrap indicators on all edges with padding."""
        if not grid.wrap_enabled:
            return
                
        arrow_size = 8
        line_length = 15
        
        # Draw wrap indicators for all edges
        for x in range(grid.width):
            # Top edge
            pygame.draw.line(screen, self.colors['wrap_indicator'],
                            (x * self.cell_size + self.cell_size//2 + padding, padding),
                            (x * self.cell_size + self.cell_size//2 + padding, padding - line_length), 2)
            # Bottom edge  
            pygame.draw.line(screen, self.colors['wrap_indicator'],
                            (x * self.cell_size + self.cell_size//2 + padding, grid.height * self.cell_size + padding),
                            (x * self.cell_size + self.cell_size//2 + padding, grid.height * self.cell_size + padding + line_length), 2)
                            
        for y in range(grid.height):
            # Left edge
            pygame.draw.line(screen, self.colors['wrap_indicator'],
                            (padding, y * self.cell_size + self.cell_size//2 + padding),
                            (padding - line_length, y * self.cell_size + self.cell_size//2 + padding), 2)
            # Right edge
            pygame.draw.line(screen, self.colors['wrap_indicator'],
                            (grid.width * self.cell_size + padding, y * self.cell_size + self.cell_size//2 + padding),
                            (grid.width * self.cell_size + padding + line_length, y * self.cell_size + self.cell_size//2 + padding), 2)
        
        # Draw connection indicators
        for x in range(grid.width):
            for y in range(grid.height):
                pipe = grid.get_pipe(x, y)
                if not pipe:
                    continue
                        
                connections = pipe.get_all_connections()
                
                if x == 0 and 3 in connections:  # Left wrap
                    pygame.draw.circle(screen, self.colors['wrap_indicator'], 
                                    (padding - 5, y * self.cell_size + self.cell_size//2 + padding), 4)
                        
                if x == grid.width-1 and 1 in connections:  # Right wrap
                    pygame.draw.circle(screen, self.colors['wrap_indicator'],
                                    (grid.width * self.cell_size + padding + 5, y * self.cell_size + self.cell_size//2 + padding), 4)
                        
                if y == 0 and 0 in connections:  # Top wrap
                    pygame.draw.circle(screen, self.colors['wrap_indicator'],
                                    (x * self.cell_size + self.cell_size//2 + padding, padding - 5), 4)
                        
                if y == grid.height-1 and 2 in connections:  # Bottom wrap
                    pygame.draw.circle(screen, self.colors['wrap_indicator'],
                                    (x * self.cell_size + self.cell_size//2 + padding, grid.height * self.cell_size + padding + 5), 4)
    
    def visualize_solution(self, n, matrix, algorithm, delay: float = 0.5) -> None:
        """Visualize solution step by step."""
        
        if algorithm == "DFS_unwrap":
            algorithm = DFS(n, matrix)
            current_grid = Grid(n, matrix)
        elif algorithm == "DFS_wrap":
            algorithm = DFS_wrap(n, matrix)
            current_grid = Grid(n, matrix, True)
        elif algorithm == "Greedy_unwrap":
            algorithm = Greedy(n, matrix)
            current_grid = Grid(n, matrix)
        elif algorithm == "Greedy_wrap":
            algorithm = Greedy_wrap(n, matrix)
            current_grid = Grid(n, matrix, True)
        ans = algorithm.solve()

        if ans == 0:
            print("----------------------------")
            print("Can't solve")
            _ = input("Press anything to continue")
            print("----------------------------")
            return


        delay = 30 / len(algorithm.visualizer) if len(algorithm.visualizer) > 60 else 0.5
        screen = self.create_window(current_grid.width, current_grid.height)
        
        # Show initial state
        self.draw_grid(screen, current_grid)
        pygame.display.flip()
        pygame.time.wait(int(delay * 1000))

        # Apply each move
        for rotation_matrix in algorithm.visualizer:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            # Set pipe to target rotation directly
            #pipe = current_grid.get_pipe(x, y)
            #pipe._rotation = target_rotation
            #pipe._connections = pipe._calculate_connections()

            current_grid.decode(n, rotation_matrix)
            
            # Update display
            self.draw_grid(screen, current_grid)
            pygame.display.flip()
            pygame.time.wait(int(delay * 1000))
        
        for row in ans:
            print(row)
        print("----------------------------")
        _ = input("Press anything to continue")
        print("----------------------------")

        # Show final state
        pygame.quit()

    def visualize(self, n, matrix, rotation_matrix, wrap_able = False) -> None:
        """Visualize solution step by step."""
        
        current_grid = Grid(n, matrix, wrap_able)
        current_grid.decode(n, rotation_matrix)

        screen = self.create_window(current_grid.width, current_grid.height)
        
        # Show initial state
        self.draw_grid(screen, current_grid)
        pygame.display.flip()

        for row in rotation_matrix:
            print(row)
        print("----------------------------")
        _ = input("Press anything to continue")
        print("----------------------------")

        # Show final state
        pygame.quit()

class PipeType(Enum):
    STRAIGHT = "│─"    # Vertical and horizontal
    CORNER = "└┘┐┌"    # Corner pieces
    TEE = "┬┤┴├"       # T-junctions
    CROSS = "┼"        # Cross junction
    END = "○"          # End point (circle)
    EMPTY = " "        # Empty cell

class Pipe:
    def __init__(self, pipe_type: PipeType, rotation: int = 0, is_end: bool = False, is_start: bool = False):
        self.pipe_type = pipe_type
        self._rotation = rotation % 4
        self.is_end = is_end or pipe_type == PipeType.END  # Fix: Also set is_end if type is END
        self.is_start = is_start
        self._connections = self._calculate_connections()
        logger.debug(f"Created pipe: type={self.pipe_type}, is_end={self.is_end}, rotation={self._rotation}")


    def __init__(self, pipe_type: PipeType, rotation: int = 0, is_end: bool = False, is_start: bool = False):
        self.pipe_type = pipe_type
        self._rotation = rotation % 4
        self.is_end = is_end or pipe_type == PipeType.END  # Fix: Also set is_end if type is END
        self.is_start = is_start
        self._connections = self._calculate_connections()
        logger.debug(f"Created pipe: type={self.pipe_type}, is_end={self.is_end}, rotation={self._rotation}")


    def __init__(self, pipe_type: PipeType, rotation: int = 0, is_end: bool = False, is_start: bool = False):
        self.pipe_type = pipe_type
        self._rotation = rotation % 4
        self.is_end = is_end or pipe_type == PipeType.END  # Fix: Also set is_end if type is END
        self.is_start = is_start
        self._connections = self._calculate_connections()
        logger.debug(f"Created pipe: type={self.pipe_type}, is_end={self.is_end}, rotation={self._rotation}")
    
    def rotate(self):
        """Rotate the pipe 90 degrees clockwise."""
        self._rotation = (self._rotation + 1) % 4
        self._connections = self._calculate_connections()
        return self
    
    def connects_to(self, direction: int) -> bool:
        """Check if the pipe connects in the given direction."""
        return direction in self._connections

    def get_all_connections(self) -> set:
        """Get all directions this pipe connects to."""
        # print(f"Getting connections for pipe: type={self.pipe_type}, rotation={self._rotation}, is_end={self.is_end}")
        return self._connections

    def _calculate_connections(self) -> set:
        """Calculate which directions this pipe connects to based on type and rotation"""
        if self.is_end:  # Change: Check is_end flag instead of pipe_type
            # END pipes only connect in one direction based on rotation
            direction_map = {
                0: {2},  # South
                1: {3},  # West
                2: {0},  # North
                3: {1}   # East
            }
            return direction_map[self._rotation]
        
        # Base connections for other pipe types    
        base_connections = {
            PipeType.STRAIGHT: [{0,2}, {1,3}],
            PipeType.CORNER: [{0,1}, {1,2}, {2,3}, {3,0}],
            PipeType.TEE: [{0,1,2}, {1,2,3}, {2,3,0}, {3,0,1}],
            PipeType.CROSS: [{0,1,2,3}]
        }
        
        if self.pipe_type not in base_connections:
            return set()
            
        connections = base_connections[self.pipe_type]
        return connections[self._rotation % len(connections)]

    def copy(self) -> 'Pipe':
        """Create a deep copy of the pipe."""
        return Pipe(
            pipe_type=self.pipe_type,
            rotation=self._rotation,
            is_end=self.is_end,
            is_start=self.is_start
        )
    
    def __str__(self):
        chars = self.pipe_type.value
        return chars[self._rotation % len(chars)]




class Grid:
    def decode(self, n, rotation_matrix):
        for i in range(n):
            for j in range(n):
                if rotation_matrix[i][j] != "":
                    if rotation_matrix[i][j] == "D":
                        self.install_pipe(j, i, PipeType.END, 0)
                    elif rotation_matrix[i][j] == "L":
                        self.install_pipe(j, i, PipeType.END, 1)
                    elif rotation_matrix[i][j] == "U":
                        self.install_pipe(j, i, PipeType.END, 2)
                    elif rotation_matrix[i][j] == "R":
                        self.install_pipe(j, i, PipeType.END, 3)
                    elif rotation_matrix[i][j] == "UD":
                        self.install_pipe(j, i, PipeType.STRAIGHT, 0)
                    elif rotation_matrix[i][j] == "LR":
                        self.install_pipe(j, i, PipeType.STRAIGHT, 1)
                    elif rotation_matrix[i][j] == "UR":
                        self.install_pipe(j, i, PipeType.CORNER, 0)
                    elif rotation_matrix[i][j] == "DR":
                        self.install_pipe(j, i, PipeType.CORNER, 1)
                    elif rotation_matrix[i][j] == "DL":
                        self.install_pipe(j, i, PipeType.CORNER, 2)
                    elif rotation_matrix[i][j] == "UL":
                        self.install_pipe(j, i, PipeType.CORNER, 3)
                    elif rotation_matrix[i][j] == "UDR":
                        self.install_pipe(j, i, PipeType.TEE, 0)
                    elif rotation_matrix[i][j] == "DRL":
                        self.install_pipe(j, i, PipeType.TEE, 1)
                    elif rotation_matrix[i][j] == "UDL":
                        self.install_pipe(j, i, PipeType.TEE, 2)
                    elif rotation_matrix[i][j] == "URL":
                        self.install_pipe(j, i, PipeType.TEE, 3)
        self.set_start(n // 2, n // 2)

    def __init__(self, n, matrix, wrap_enabled: bool = False):
        self.width = n
        self.height = n
        self.wrap_enabled = wrap_enabled
        self.grid = [[Pipe(PipeType.STRAIGHT) for _ in range(n)] for _ in range(n)]
        self.start_pos = None
        self.end_positions = set()
        
        for i in range(n):
            for j in range(n):
                if matrix[i][j] == 1:
                    case = random.randint(1, 4)
                    self.install_pipe(j, i, PipeType.END, case)
                elif matrix[i][j] == 2:
                    case = random.randint(1, 2)
                    self.install_pipe(j, i, PipeType.STRAIGHT, case)
                elif matrix[i][j] == 2:
                    case = random.randint(1, 4)
                    self.install_pipe(j, i, PipeType.CORNER, case)
                else:
                    case = random.randint(1, 4)
                    self.install_pipe(j, i, PipeType.TEE, case)

        self.set_start(n // 2, n // 2)

    def install_pipe(self, x: int, y: int, pipe_type: PipeType, rotation: int, is_end: bool = False):
        """Helper function to install a pipe and update end positions if needed."""
        self.grid[y][x] = Pipe(pipe_type, rotation, is_end)
        if is_end:
            self.end_positions.add((x, y))
            logger.debug(f"Added end position at ({x}, {y})")


    #def __init__(self, width: int, height: int, wrap_enabled: bool = False):
    #    self.width = width
    #    self.height = height
    #    self.wrap_enabled = wrap_enabled
    #    # Initialize with STRAIGHT pipes instead of EMPTY
    #    self.grid = [[Pipe(PipeType.STRAIGHT) for _ in range(width)] for _ in range(height)]
    #    self.start_pos = None
    #    self.end_positions = set()

    def set_start(self, x: int, y: int) -> bool:
        """Mark a pipe as the start point. Only TEE, , or CORNER pipes can be start points."""
        pipe = self.get_pipe(x, y)
        if pipe and pipe.pipe_type in [PipeType.TEE, PipeType.CROSS, PipeType.CORNER]:
            # Clear any existing start point
            if self.start_pos:
                old_x, old_y = self.start_pos
                self.get_pipe(old_x, old_y).is_start = False
            
            pipe.is_start = True
            self.start_pos = (x, y)
            return True
        return False

    def find_all_connected_pipes(self, start_x: int, start_y: int) -> Set[Tuple[int, int]]:
        """Find all pipes connected to the given starting position."""
        connected = set()
        queue = deque([(start_x, start_y)])
        
        logger.debug(f"\nStarting connection search from ({start_x}, {start_y})")
        
        while queue:
            x, y = queue.popleft()
            if (x, y) in connected:
                continue
                
            current_pipe = self.get_pipe(x, y)
            logger.debug(f"\nChecking pipe at ({x}, {y}): {current_pipe.pipe_type}, connections={current_pipe.get_all_connections()}")
            connected.add((x, y))
            
            # Check all four directions
            for direction, (dx, dy) in enumerate([(0,-1), (1,0), (0,1), (-1,0)]):
                next_x, next_y = x + dx, y + dy
                
                if not self._is_valid_position(next_x, next_y):
                    logger.debug(f"  Invalid position: ({next_x}, {next_y})")
                    continue
                    
                if (next_x, next_y) in connected:
                    logger.debug(f"  Already connected: ({next_x}, {next_y})")
                    continue
                    
                next_pipe = self.get_pipe(next_x, next_y)
                logger.debug(f"  Checking connection to ({next_x}, {next_y}): {next_pipe.pipe_type}, connections={next_pipe.get_all_connections()}")
                
                if self.are_pipes_connected(x, y, next_x, next_y):
                    logger.debug(f"  Connected! Adding ({next_x}, {next_y}) to queue")
                    queue.append((next_x, next_y))
                else:
                    logger.debug(f"  Not connected to ({next_x}, {next_y})")
        
        logger.debug(f"\nFinal connected pipes: {connected}")
        logger.debug(f"Missing connections: {set((x, y) for x in range(self.width) for y in range(self.height)) - connected}")
        return connected

    def are_pipes_connected(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        """Check if two pipes are properly connected, handling wrapping."""
        if not self._is_valid_position(x1, y1) or not self._is_valid_position(x2, y2):
            return False

        pipe1 = self.get_pipe(x1, y1)
        pipe2 = self.get_pipe(x2, y2)
        
        if not pipe1 or not pipe2:
            return False

        # Calculate relative direction with wrap handling
        dx = x2 - x1
        dy = y2 - y1
        
        # Handle wrap-around for x-axis
        if self.wrap_enabled:
            if abs(dx) == self.width - 1:
                dx = -1 if dx > 0 else 1
            # Handle wrap-around for y-axis    
            if abs(dy) == self.height - 1:
                dy = -1 if dy > 0 else 1

        # Check if pipes are adjacent (including wrap)
        if abs(dx) + abs(dy) != 1:
            return False

        # Determine required directions for connection
        if dx == 1:  # Right
            dir1, dir2 = 1, 3  # Right from pipe1, Left from pipe2
        elif dx == -1:  # Left
            dir1, dir2 = 3, 1  # Left from pipe1, Right from pipe2
        elif dy == 1:  # Down
            dir1, dir2 = 2, 0  # Down from pipe1, Up from pipe2
        else:  # dy == -1, Up
            dir1, dir2 = 0, 2  # Up from pipe1, Down from pipe2

        return pipe1.connects_to(dir1) and pipe2.connects_to(dir2)

    def is_valid_solution(self) -> bool:
        """Check if current grid state is a valid solution."""
        if not self.start_pos:
            logger.debug("No start position found")
            return False
                
        # Check all end point connections
        for x, y in self.end_positions:
            pipe = self.get_pipe(x, y)
                
            if not pipe or not pipe.is_end:
                logger.debug(f"Invalid end point at ({x}, {y})")
                return False
                    
            # Check single connection for end pipes
            connections = pipe.get_all_connections()
            if len(connections) != 1:
                logger.debug(f"End pipe at ({x}, {y}) has {len(connections)} connections instead of 1")
                return False

            # Verify the end pipe connects to something
            direction = next(iter(connections))
            dx, dy = [(0,-1), (1,0), (0,1), (-1,0)][direction]
            next_x, next_y = x + dx, y + dy
                
            if not self.are_pipes_connected(x, y, next_x, next_y):
                logger.debug(f"End pipe at ({x}, {y}) is not properly connected")
                return False
            
        # Find all pipes connected to start
        connected_pipes = self.find_all_connected_pipes(*self.start_pos)
        logger.debug(f"Connected pipes from start: {len(connected_pipes)} of {self.width * self.height}")
        
        # Key change: If we can reach all pipes from start, this is a valid solution
        return len(connected_pipes) == self.width * self.height


    def _wrap_position(self, x: int, y: int) -> Tuple[int, int]:
        """Handle position wrapping for wrap-enabled grids."""
        if self.wrap_enabled:
            x = x % self.width
            y = y % self.height
        return (x, y)

    def _is_valid_position(self, x: int, y: int) -> bool:
        """Check if the position is within grid bounds."""
        if self.wrap_enabled:
            return True  # Allow wrap around
        return 0 <= x < self.width and 0 <= y < self.height

    def get_pipe(self, x: int, y: int) -> Optional[Pipe]:
        """Get the pipe at the specified position, handling wrapping."""
        if not self._is_valid_position(x, y):
            return None
        x, y = self._wrap_position(x, y)
        return self.grid[y][x]

    def set_pipe(self, x: int, y: int, pipe: Pipe):
        """Place a pipe at the specified position, handling wrapping."""
        if self._is_valid_position(x, y):
            x, y = self._wrap_position(x, y)
            self.grid[y][x] = pipe

    def copy(self) -> 'Grid':
        """Create a deep copy of the grid."""
        # print("Creating grid copy...")
        new_grid = Grid(self.width, [["" for _ in range(self.width)] for _ in range(self.width)]) #Grid(self.width, self.height, self.wrap_enabled)
        new_grid.start_pos = self.start_pos
        new_grid.end_positions = set(self.end_positions)
        
        # Copy all pipes with their states
        for y in range(self.height):
            for x in range(self.width):
                pipe = self.get_pipe(x, y)
                if pipe:
                    # print(f"Copying pipe at ({x},{y}): type={pipe.pipe_type}, is_end={pipe.is_end}, connections={pipe._connections}")
                    new_pipe = Pipe(pipe.pipe_type, pipe._rotation, pipe.pipe_type == PipeType.END, pipe.is_start)
                    # print(f"New pipe created: type={new_pipe.pipe_type}, rotation={new_pipe._rotation}, is_end={new_pipe.is_end}")
                    # print(f"New pipe connections: {new_pipe._connections}")
                    new_grid.set_pipe(x, y, new_pipe)
                    final_pipe = new_grid.get_pipe(x, y)
                    # print(f"Final pipe in grid: type={final_pipe.pipe_type}, rotation={final_pipe._rotation}, is_end={final_pipe.is_end}")
    
        return new_grid

    def __str__(self):
        """Return string representation of the grid."""
        return '\n'.join([''.join(str(pipe) for pipe in row) for row in self.grid])

    def has_valid_connections(self, x: int, y: int) -> bool:
        """Check if a pipe at position has valid connections with its neighbors."""
        pipe = self.get_pipe(x, y)
        if not pipe:
            return False
            
        # Check each direction for valid connections
        for direction, (dx, dy) in enumerate([(0,-1), (1,0), (0,1), (-1,0)]):
            next_x, next_y = x + dx, y + dy
            
            # Skip if next position is invalid
            if not self._is_valid_position(next_x, next_y):
                continue
                
            # If the pipe connects in this direction, there must be a valid pipe connection
            if direction in pipe.get_all_connections():
                if not self.are_pipes_connected(x, y, next_x, next_y):
                    return False
                    
        return True