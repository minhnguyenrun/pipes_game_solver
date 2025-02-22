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
        self.pipe_width = 8
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
    
    def visualize_solution(self, grid, solution_moves: List[Tuple[int, int, int]], delay: float = 0.5) -> None:
        """Visualize solution step by step."""
        screen = self.create_window(grid.width, grid.height)
        current_grid = grid.copy()
        
        # Show initial state
        self.draw_grid(screen, current_grid)
        pygame.display.flip()
        pygame.time.wait(int(delay * 1000))
        
        # Apply each move
        for x, y, target_rotation in solution_moves:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                
            # Set pipe to target rotation directly
            pipe = current_grid.get_pipe(x, y)
            pipe._rotation = target_rotation
            pipe._connections = pipe._calculate_connections()
            
            # Update display
            self.draw_grid(screen, current_grid)
            pygame.display.flip()
            pygame.time.wait(int(delay * 1000))
                    
        # Show final state
        pygame.time.wait(int(delay * 2000))  # Longer pause at end
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
    def __init__(self, width: int, height: int, wrap_enabled: bool = False):
        self.width = width
        self.height = height
        self.wrap_enabled = wrap_enabled
        # Initialize with STRAIGHT pipes instead of EMPTY
        self.grid = [[Pipe(PipeType.STRAIGHT) for _ in range(width)] for _ in range(height)]
        self.start_pos = None
        self.end_positions = set()

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
        new_grid = Grid(self.width, self.height, self.wrap_enabled)
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

@dataclass
class SearchState:
    grid: Grid
    moves: List[Tuple[int, int, int]]  # (x, y, rotation) for each move
    score: float = float('inf')

    def __init__(self, grid: Grid, moves: List[Tuple[int, int, int]], score: float = float('inf')):
        # Debug log for start state
        if moves == []:
            # print("Initial state grid:")
            for y in range(grid.height):
                for x in range(grid.width):
                    pipe = grid.get_pipe(x, y)
                    # print(f"({x},{y}): type={pipe.pipe_type}, is_end={pipe.is_end}")

        self.grid = grid.copy()
        self.moves = moves
        self.score = score

    def get_next_states(self) -> List['SearchState']:
        """Generate next states by rotating one pipe at a time."""
        next_states = []
        
        # For each cell in grid
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                pipe = self.grid.get_pipe(x, y)
                if pipe and pipe.pipe_type != PipeType.EMPTY:
                    # Print pipe info before rotation
                    # print(f"Processing pipe at ({x},{y}): type={pipe.pipe_type}, is_end={pipe.is_end}")
                    
                    current_rotation = pipe._rotation
                    # Try only the next rotation from current
                    new_rotation = (current_rotation + 1) % 4
                    
                    new_grid = self.grid.copy()
                    new_pipe = new_grid.get_pipe(x, y)
                    new_pipe._rotation = new_rotation
                    new_pipe._connections = new_pipe._calculate_connections()
                    
                    next_states.append(SearchState(
                        grid=new_grid,
                        moves=self.moves + [(x, y, new_rotation)],
                        score=float('inf')
                    ))
        return next_states
    
    def calculate_score(self) -> float:
        if not self.grid.start_pos:
            return float('inf')

        if self.grid.is_valid_solution():
            return -1000  # Best possible score

        connected = self.grid.find_all_connected_pipes(*self.grid.start_pos)
        score = 0

        # 1. Manhattan Distance to Unconnected Endpoints
        for end_x, end_y in self.grid.end_positions:
            if (end_x, end_y) not in connected:
                min_dist = float('inf')
                for connected_x, connected_y in connected:
                    dist = abs(end_x - connected_x) + abs(end_y - connected_y)
                    # Handle wrapping if enabled
                    if self.grid.wrap_enabled:
                        dist = min(dist, self.grid.width - abs(end_x - connected_x) + abs(end_y - connected_y))
                        dist = min(dist, abs(end_x - connected_x) + self.grid.height - abs(end_y - connected_y))
                    min_dist = min(min_dist, dist)
                score += min_dist * 10 # Experiment with weight

        # 2. Number of disconnected pipes (simple and admissible)
        score += (self.grid.width * self.grid.height - len(connected)) * 5

        # 3. Penalize number of moves.
        score += len(self.moves) * 2
        return score

    def __hash__(self):
        return hash(str(self.grid))
    
    def __eq__(self, other):
        if not isinstance(other, SearchState):
            return False
        return str(self.grid) == str(other.grid)
    
    def __lt__(self, other):
        return self.score < other.score

class DFSSearch:
    def __init__(self, grid: Grid):
        self.initial_grid = grid
        self.nodes_explored = 0
        self.max_memory = 0
        self.solution_path = []

    def solve(self, time_limit: float = 300.0, memory_limit: int = 1000000000) -> Optional[SearchState]:
        """
        Improved DFS search with better validation handling.
        """
        logger.info("Starting DFS search")
        start_time = time.time()
        self.nodes_explored = 0
        self.max_memory = 0

        # Check if initial state is already a solution
        if self.initial_grid.is_valid_solution():
            logger.info("Initial state is already a solution")
            return SearchState(grid=self.initial_grid, moves=[])

        # Initialize stack with all possible rotations of the start pipe
        stack = []
        visited_states = set()
        
        # Get start position
        if not self.initial_grid.start_pos:
            logger.error("No start position found")
            return None
            
        start_x, start_y = self.initial_grid.start_pos
        
        # Try each possible rotation of start pipe
        for rotation in range(4):
            new_grid = self.initial_grid.copy()
            new_pipe = new_grid.get_pipe(start_x, start_y)
            
            # Set rotation directly and update connections
            new_pipe._rotation = rotation
            new_pipe._connections = new_pipe._calculate_connections()
            
            # Create new state
            new_state = SearchState(
                grid=new_grid,
                moves=[(start_x, start_y, rotation)]
            )
            
            # Add to stack if not visited
            state_str = str(new_grid)
            if state_str not in visited_states:
                stack.append(new_state)
                visited_states.add(state_str)

        # Main DFS loop
        while stack and (time.time() - start_time) < time_limit:
            # Memory check
            current_memory = len(stack) + len(visited_states)
            self.max_memory = max(self.max_memory, current_memory)
            if current_memory > memory_limit:
                logger.warning("Memory limit exceeded")
                return None

            current_state = stack.pop()
            self.nodes_explored += 1

            # Debug logging for validation
            logger.debug(f"Checking state after {len(current_state.moves)} moves")
            if current_state.grid.is_valid_solution():
                logger.info(f"Solution found with {len(current_state.moves)} moves!")
                return current_state

            # Generate and process next states
            for next_state in current_state.get_next_states():
                state_str = str(next_state.grid)
                if state_str not in visited_states:
                    stack.append(next_state)
                    visited_states.add(state_str)

        if time.time() - start_time >= time_limit:
            logger.warning("Time limit exceeded")
        return None
    
class AStarSearch:
    def __init__(self, grid: Grid):
        self.initial_grid = grid
        self.nodes_explored = 0
        self.max_memory = 0
        self.solution_path = []

    def solve(self, time_limit: float = 3000.0) -> Optional[SearchState]:
        """Optimized A* search."""
        logger.info("Starting A* search")
        start_time = time.time()
        
        initial_state = SearchState(
            grid=self.initial_grid.copy(),
            moves=[]
        )
        
        # Use dictionary for faster lookup
        visited = {}
        queue = [(initial_state.calculate_score(), 0, initial_state)]
        heapq.heapify(queue)
        
        while queue and (time.time() - start_time) < time_limit:
            current_score, _, current_state = heapq.heappop(queue)
            
            if current_state.grid.is_valid_solution():
                logger.info(f"Solution found! Score: {current_score}")
                return current_state
                
            state_hash = str(current_state.grid)
            if state_hash in visited and visited[state_hash] <= current_score:
                continue
                
            visited[state_hash] = current_score
            
            # Generate next states more efficiently
            for next_state in current_state.get_next_states():
                next_score = next_state.calculate_score()
                if str(next_state.grid) not in visited or next_score < visited[str(next_state.grid)]:
                    heapq.heappush(queue, (next_score, len(next_state.moves), next_state))
        
        logger.warning("No solution found within time limit")
        return None

class BFSSearch:
    def __init__(self, grid: Grid):
        self.initial_grid = grid
        self.nodes_explored = 0
        self.max_memory = 0

    def solve(self, time_limit: float = 300.0) -> Optional[SearchState]:
        """BFS implementation for pipe puzzle."""
        logger.info("Starting BFS search")
        start_time = time.time()
        self.nodes_explored = 0
        self.max_memory = 0

        # Initialize queue with initial state
        queue = deque([SearchState(self.initial_grid.copy(), [])])
        visited = set()

        while queue and (time.time() - start_time) < time_limit:
            current_state = queue.popleft()
            self.nodes_explored += 1

            # Update max memory usage
            current_memory = len(queue) + len(visited)
            self.max_memory = max(self.max_memory, current_memory)

            # Check if current state is solution
            if current_state.grid.is_valid_solution():
                logger.info(f"Solution found with {len(current_state.moves)} moves!")
                return current_state

            # Generate and process next states
            for next_state in current_state.get_next_states():
                state_str = str(next_state.grid)
                if state_str not in visited:
                    visited.add(state_str)
                    queue.append(next_state)

        logger.warning("No solution found within time limit")
        return None

class HillClimbingSearch:
    def __init__(self, grid: Grid):
        self.initial_grid = grid
        self.nodes_explored = 0
        self.max_memory = 0
        self.max_sideways_moves = 100  # Limit sideways moves to prevent infinite loops
        self.max_restarts = 5  # Number of random restarts

    def _get_random_state(self) -> SearchState:
        """Generate a random state by randomly rotating pipes."""
        grid = self.initial_grid.copy()
        moves = []
        
        for y in range(grid.height):
            for x in range(grid.width):
                pipe = grid.get_pipe(x, y)
                if pipe and pipe.pipe_type != PipeType.EMPTY:
                    rotation = random.randint(0, 3)
                    pipe._rotation = rotation
                    pipe._connections = pipe._calculate_connections()
                    moves.append((x, y, rotation))
        
        return SearchState(grid=grid, moves=moves)

    def solve(self, time_limit: float = 300.0) -> Optional[SearchState]:
        """Hill Climbing with random restarts for pipe puzzle."""
        logger.info("Starting Hill Climbing search")
        start_time = time.time()
        self.nodes_explored = 0
        self.max_memory = 1  # Hill Climbing uses constant memory

        # --- ADD THIS CHECK ---
        initial_state = SearchState(self.initial_grid.copy(), [])
        if initial_state.grid.is_valid_solution():
            logger.info("Initial state is already a solution!")
            return initial_state
        # --- END OF ADDED CHECK ---

        best_solution = None
        best_score = float('inf')

        for restart in range(self.max_restarts):
            if (time.time() - start_time) >= time_limit:
                break

            current_state = self._get_random_state()
            sideways_moves = 0
            
            while (time.time() - start_time) < time_limit:
                self.nodes_explored += 1
                current_score = current_state.calculate_score()

                if current_state.grid.is_valid_solution():
                    logger.info(f"Solution found with {len(current_state.moves)} moves!")
                    return current_state

                # Find best neighbor
                best_neighbor = None
                best_neighbor_score = current_score

                for next_state in current_state.get_next_states():
                    next_score = next_state.calculate_score()
                    if next_score < best_neighbor_score:
                        best_neighbor = next_state
                        best_neighbor_score = next_score

                # If no better neighbor found, try sideways move or terminate
                if best_neighbor_score >= current_score:
                    if sideways_moves < self.max_sideways_moves:
                        # Allow sideways moves
                        neighbors = list(current_state.get_next_states())
                        if neighbors:
                            best_neighbor = random.choice(neighbors)
                            best_neighbor_score = best_neighbor.calculate_score()
                            sideways_moves += 1
                    else:
                        break  # Stuck in local optimum
                else:
                    sideways_moves = 0

                if best_neighbor is None:
                    break

                current_state = best_neighbor
                
                # Update best solution if current is better
                if best_neighbor_score < best_score:
                    best_score = best_neighbor_score
                    best_solution = current_state

            logger.info(f"Restart {restart + 1} completed. Best score: {best_score}")

        return best_solution



def install_pipe(grid: Grid, x: int, y: int, pipe_type: PipeType, rotation: int, is_end: bool = False):
    """Helper function to install a pipe and update end positions if needed."""
    grid.grid[y][x] = Pipe(pipe_type, rotation, is_end)
    if is_end:
        grid.end_positions.add((x, y))
        logger.debug(f"Added end position at ({x}, {y})")

def create_grid_from_image_5x5_TEXT_DESC_ROTATED() -> Grid:
    width = 5
    height = 5
    wrap_enabled = False
    grid = Grid(width, height, wrap_enabled)

    # Row 0: end, end, corner, end, corner
    install_pipe(grid, 0, 0, PipeType.END, 0, True)
    install_pipe(grid, 1, 0, PipeType.END, 0, True)
    install_pipe(grid, 2, 0, PipeType.CORNER, 0, False) # 0
    install_pipe(grid, 3, 0, PipeType.END, 0, True)
    install_pipe(grid, 4, 0, PipeType.CORNER, 0, False)

    # Row 1: corner, TEE, TEE, end, TEE
    install_pipe(grid, 0, 1, PipeType.CORNER, 0, False)
    install_pipe(grid, 1, 1, PipeType.TEE, 1, False)
    install_pipe(grid, 2, 1, PipeType.TEE, 2, False)
    install_pipe(grid, 3, 1, PipeType.END, 3, True) # 1
    install_pipe(grid, 4, 1, PipeType.TEE, 2, False)

    # Row 2: end, corner, corner (start), TEE, TEE
    install_pipe(grid, 0, 2, PipeType.END, 3, True)
    install_pipe(grid, 1, 2, PipeType.CORNER, 3, False)
    install_pipe(grid, 2, 2, PipeType.CORNER, 0, False) # Start position
    install_pipe(grid, 3, 2, PipeType.TEE, 1, False)
    install_pipe(grid, 4, 2, PipeType.TEE, 2, False)

    # Row 3: corner, TEE, straight, TEE, end
    install_pipe(grid, 0, 3, PipeType.CORNER, 1, False)
    install_pipe(grid, 1, 3, PipeType.TEE, 1, False)
    install_pipe(grid, 2, 3, PipeType.STRAIGHT, 1, False)
    install_pipe(grid, 3, 3, PipeType.TEE, 2, False)
    install_pipe(grid, 4, 3, PipeType.END, 2, True)

    # Row 4: end, end, end, TEE, end.
    install_pipe(grid, 0, 4, PipeType.END, 2, True)
    install_pipe(grid, 1, 4, PipeType.END, 2, True)
    install_pipe(grid, 2, 4, PipeType.END, 3, True)
    install_pipe(grid, 3, 4, PipeType.TEE, 3, False)
    install_pipe(grid, 4, 4, PipeType.END, 1, True)

    start_x = 2 # Column 2
    start_y = 2 # Row 2
    grid.set_start(start_x, start_y) # Set start AFTER pipes are installed - IMPORTANT!

    return grid

def create_test_puzzle() -> Grid:
    """Create a test puzzle configuration for 4x4 grid."""
    grid = Grid(4, 4)
    
    # Row 0 (top row)
    install_pipe(grid, 0, 0, PipeType.CORNER, 1)
    install_pipe(grid, 1, 0, PipeType.STRAIGHT, 1)
    install_pipe(grid, 2, 0, PipeType.TEE, 1) # rotation 1
    install_pipe(grid, 3, 0, PipeType.END, 1, True) # rotation 1
    
    # Row 1
    install_pipe(grid, 0, 1, PipeType.END, 2, True)
    install_pipe(grid, 1, 1, PipeType.END, 0, True)
    install_pipe(grid, 2, 1, PipeType.TEE, 0)
    install_pipe(grid, 3, 1, PipeType.CORNER, 2)
    
    # Row 2
    install_pipe(grid, 0, 2, PipeType.CORNER, 1)
    install_pipe(grid, 1, 2, PipeType.TEE, 3)
    install_pipe(grid, 2, 2, PipeType.TEE, 2)
    install_pipe(grid, 3, 2, PipeType.END, 2, True)
    
    # Row 3
    install_pipe(grid, 0, 3, PipeType.END, 2, True)
    install_pipe(grid, 1, 3, PipeType.END, 3, True)
    install_pipe(grid, 2, 3, PipeType.TEE, 3)
    install_pipe(grid, 3, 3, PipeType.END, 1, True)

    # Mark the TEE pipe as start point
    grid.set_start(2, 2)
    logger.debug(f"Start position set at (2, 2)")
    logger.debug(f"Total end positions: {grid.end_positions}")
    
    return grid

def create_wrap_test_puzzle() -> Grid:
    """Create a test puzzle specifically for wrap variant."""
    grid = Grid(4, 4, wrap_enabled=True)
    
    # Set start point as a TEE pipe at top-left
    grid.grid[0][0] = Pipe(PipeType.TEE, rotation=1)
    grid.set_start(0, 0)
    
    # Add end points that require wrapping
    # Right edge endpoint
    install_pipe(grid, 3, 0, PipeType.END, 1, True)
    # Bottom edge endpoint
    install_pipe(grid, 0, 3, PipeType.END, 0, True)
    
    # Add pipes that require wrapping to solve
    # Top row
    install_pipe(grid, 1, 0, PipeType.STRAIGHT, 1)
    install_pipe(grid, 2, 0, PipeType.CORNER, 1)
    
    # Right column
    install_pipe(grid, 3, 1, PipeType.STRAIGHT, 0)
    install_pipe(grid, 3, 2, PipeType.CORNER, 2)
    install_pipe(grid, 3, 3, PipeType.TEE, 3)
    
    # Bottom row
    install_pipe(grid, 1, 3, PipeType.STRAIGHT, 1)
    install_pipe(grid, 2, 3, PipeType.CORNER, 0)
    
    # Middle section
    install_pipe(grid, 1, 1, PipeType.CROSS, 0)
    install_pipe(grid, 2, 1, PipeType.TEE, 2)
    install_pipe(grid, 1, 2, PipeType.TEE, 1)
    install_pipe(grid, 2, 2, PipeType.CORNER, 3)
    
    # Left column (excluding start and end)
    install_pipe(grid, 0, 1, PipeType.STRAIGHT, 0)
    install_pipe(grid, 0, 2, PipeType.CORNER, 1)
    
    return grid

def test_wrap_puzzle():
    """Test both DFS and A* solvers with a wrap-enabled puzzle."""
    print("Creating wrap test puzzle...")
    grid = create_wrap_test_puzzle()
    
    print("\nTesting DFS Solver on wrap puzzle...")
    dfs = DFSSearch(grid)
    dfs_start_time = time.time()
    dfs_solution = dfs.solve(time_limit=30000.0)
    dfs_time = time.time() - dfs_start_time
    
    if dfs_solution:
        print(f"DFS found wrap solution in {dfs_time:.2f} seconds!")
        print(f"DFS solution moves: {len(dfs_solution.moves)}")
        print(f"DFS nodes explored: {dfs.nodes_explored}")
        print(f"DFS max memory used: {dfs.max_memory}")
        
        # Visualize DFS solution
        print("\nVisualizing DFS wrap solution...")
        visualizer = PipeVisualizer()
        visualizer.visualize_solution(grid, dfs_solution.moves)
    else:
        print("DFS failed to find wrap solution!")

    print("\nTesting A* Solver on wrap puzzle...")
    astar = AStarSearch(grid)
    astar_start_time = time.time()
    astar_solution = astar.solve(time_limit=30000.0)
    astar_time = time.time() - astar_start_time
    
    if astar_solution:
        print(f"A* found wrap solution in {astar_time:.2f} seconds!")
        print(f"A* solution moves: {len(astar_solution.moves)}")
        print(f"A* nodes explored: {astar.nodes_explored}")
        print(f"A* max memory used: {astar.max_memory}")
        
        # Visualize A* solution
        print("\nVisualizing A* wrap solution...")
        visualizer = PipeVisualizer()
        visualizer.visualize_solution(grid, astar_solution.moves)
    else:
        print("A* failed to find wrap solution!")

    # Compare solutions if both found
    if dfs_solution and astar_solution:
        print("\nComparing wrap puzzle solutions:")
        print(f"DFS time: {dfs_time:.2f}s vs A* time: {astar_time:.2f}s")
        print(f"DFS moves: {len(dfs_solution.moves)} vs A* moves: {len(astar_solution.moves)}")
        print(f"DFS nodes: {dfs.nodes_explored} vs A* nodes: {astar.nodes_explored}")

def create_solution_grid() -> Grid:
    """Create a grid matching the provided solution state with wrap connections."""
    grid = Grid(4, 4, wrap_enabled=True)
    
    # Row 1 (top)
    install_pipe(grid, 0, 0, PipeType.STRAIGHT, 0) 
    install_pipe(grid, 1, 0, PipeType.END, 2, True) 
    install_pipe(grid, 2, 0, PipeType.CORNER, 0)    
    install_pipe(grid, 3, 0, PipeType.END, 1, True) 
    
    # Row 2
    install_pipe(grid, 0, 1, PipeType.END, 2, True)     
    install_pipe(grid, 1, 1, PipeType.END, 3, True)     
    install_pipe(grid, 2, 1, PipeType.TEE, 1)       
    install_pipe(grid, 3, 1, PipeType.END, 1, True)     
    
    # Row 3
    install_pipe(grid, 0, 2, PipeType.CORNER, 1)        
    install_pipe(grid, 1, 2, PipeType.TEE, 1) # rotation 1       
    install_pipe(grid, 2, 2, PipeType.TEE, 2)           
    install_pipe(grid, 3, 2, PipeType.END, 0, True)     
    
    # Row 4 (bottom)
    install_pipe(grid, 0, 3, PipeType.STRAIGHT, 0)      
    install_pipe(grid, 1, 3, PipeType.STRAIGHT, 2)      
    install_pipe(grid, 2, 3, PipeType.TEE, 0)           
    install_pipe(grid, 3, 3, PipeType.CORNER, 3)       

    # Set the start point (TEE pipe in third row)
    grid.set_start(2, 2)
    
    return grid


def test_solution_visualization():
    """Test the visualizer with the solution grid."""
    print("Creating solution grid...")
    grid = create_solution_grid()
    
    print("\nStarting visualization...")
    visualizer = PipeVisualizer()
    screen = visualizer.create_window(grid.width, grid.height)
    
    try:
        print("Displaying grid. Press Ctrl+C to exit...")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            visualizer.draw_grid(screen, grid)
            pygame.display.flip()
            pygame.time.wait(100)  # Small delay to prevent high CPU usage
            
    except KeyboardInterrupt:
        print("\nVisualization interrupted by user")
    finally:
        pygame.quit()


def test_all_algorithms():
    # """Test all four search algorithms with both puzzle configurations."""
    # print("\nTesting with test puzzle configuration...")
    # test_grid = create_test_puzzle()
    
    # algorithms = [
    #     ("DFS", DFSSearch(test_grid)),
    #     ("BFS", BFSSearch(test_grid)),
    #     ("A*", AStarSearch(test_grid)),
    #     ("Hill Climbing", HillClimbingSearch(test_grid))
    # ]
    
    # results = []
    
    # for name, algorithm in algorithms:
    #     print(f"\nTesting {name}...")
    #     start_time = time.time()
    #     solution = algorithm.solve(time_limit=3000.0)
    #     solve_time = time.time() - start_time
        
    #     result = {
    #         "name": name,
    #         "found_solution": solution is not None,
    #         "time": solve_time,
    #         "moves": len(solution.moves) if solution else None,
    #         "nodes": algorithm.nodes_explored,
    #         "memory": algorithm.max_memory
    #     }
    #     results.append(result)
        
    #     if solution:
    #         print(f"{name} found solution in {solve_time:.2f} seconds!")
    #         print(f"Moves: {result['moves']}")
    #         print(f"Nodes explored: {result['nodes']}")
    #         print(f"Max memory: {result['memory']}")
            
    #         # Visualize solution
    #         visualizer = PipeVisualizer()
    #         visualizer.visualize_solution(test_grid, solution.moves)
    #     else:
    #         print(f"{name} failed to find solution!")
            
    print("\nTesting with solution grid configuration...")
    solution_grid = create_grid_from_image_5x5_TEXT_DESC_ROTATED()
    
    for name, algorithm_class in [
        ("DFS", DFSSearch),
        ("BFS", BFSSearch),
        ("A*", AStarSearch),
        ("Hill Climbing", HillClimbingSearch)
    ]:
        print(f"\nTesting {name} on solution grid...")
        algorithm = algorithm_class(solution_grid)
        start_time = time.time()
        solution = algorithm.solve(time_limit=3000.0)
        solve_time = time.time() - start_time
        
        if solution:
            print(f"{name} recognized solution in {solve_time:.2f} seconds")
            print(f"Moves suggested: {len(solution.moves)}")
            print(f"Nodes explored: {algorithm.nodes_explored}")
        else:
            print(f"{name} failed to recognize solution!")

def main():
    """Test the pipe puzzle solver with visualization."""
    # Create and visualize the test puzzle
    grid = create_grid_from_image_5x5_TEXT_DESC_ROTATED()
    visualizer = PipeVisualizer()
    screen = visualizer.create_window(grid.width, grid.height)
    
    print("Initial Grid State:")
    # print(str(grid))
    print("\nPress Ctrl+C to exit...")
    
    try:
        while True:
            visualizer.draw_grid(screen, grid)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
    except KeyboardInterrupt:
        pygame.quit()

if __name__ == "__main__":
    # test_all_algorithms()
    grid = create_test_puzzle()
    print("Testing A* algortihm")
    astar = DFSSearch(grid)
    start_time = time.time()
    astar_solution = astar.solve(time_limit=300000.0)
    astar_time = time.time() - start_time
    if astar_solution:
        print(f"A* found wrap solution in {astar_time:.2f} seconds!")
        print(f"A* solution moves: {len(astar_solution.moves)}")
        print(f"A* nodes explored: {astar.nodes_explored}")
        print(f"A* max memory used: {astar.max_memory}")
        
        # Visualize A* solution
        print("\nVisualizing A* wrap solution...")
        visualizer = PipeVisualizer()
        visualizer.visualize_solution(grid, astar_solution.moves)
