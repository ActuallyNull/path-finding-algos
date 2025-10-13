import numpy as np
import matplotlib.pyplot as plt
from heapq import heappush, heappop
from collections import deque
import random
from PIL import Image
import io 

# =====================================================
# Maze Generation (Unchanged)
# =====================================================
def generate_maze(width, height):
    maze = np.ones((height, width), dtype=int)
    def carve(x, y):
        directions = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < height-1 and 1 <= ny < width-1 and maze[nx, ny] == 1:
                maze[nx - dx//2, ny - dy//2] = 0
                maze[nx, ny] = 0
                carve(nx, ny)
    maze[1, 1] = 0
    carve(1, 1)
    return maze

# =====================================================
# Pathfinding Algorithms (Unchanged)
# =====================================================

def reconstruct_path(came_from, start, goal):
    path = []
    current = goal
    while current in came_from:
        path.append(current)
        current = came_from[current]
    if path:
        path.append(start)
        path.reverse()
    return path

# --- A* ---
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])
def a_star(maze, start, goal):
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    visited_order = []
    while open_set:
        _, current = heappop(open_set)
        visited_order.append(current)
        if current == goal:
            break
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = current[0]+dx, current[1]+dy
            if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] == 0:
                tentative_g = g_score.get(current, float('inf')) + 1
                if tentative_g < g_score.get((nx,ny), float('inf')):
                    came_from[(nx,ny)] = current
                    g_score[(nx,ny)] = tentative_g
                    f_score = tentative_g + heuristic((nx,ny), goal)
                    heappush(open_set, (f_score, (nx,ny)))
    return reconstruct_path(came_from, start, goal), visited_order

# --- Dijkstra's Algorithm ---
def dijkstra(maze, start, goal):
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    visited_order = []
    while open_set:
        dist, current = heappop(open_set)
        visited_order.append(current)
        if current == goal:
            break
        if dist > g_score.get(current, float('inf')):
             continue 
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = current[0]+dx, current[1]+dy
            if 0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and maze[nx, ny] == 0:
                tentative_g = dist + 1
                if tentative_g < g_score.get((nx,ny), float('inf')):
                    came_from[(nx,ny)] = current
                    g_score[(nx,ny)] = tentative_g
                    heappush(open_set, (tentative_g, (nx,ny)))
    return reconstruct_path(came_from, start, goal), visited_order

# --- Breadth-First Search (BFS) ---
def bfs(maze, start, goal):
    queue = deque([start])
    came_from = {start: None}
    visited_order = []
    while queue:
        current = queue.popleft()
        visited_order.append(current)
        if current == goal:
            break
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = current[0]+dx, current[1]+dy
            neighbor = (nx, ny)
            if (0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and 
                maze[nx, ny] == 0 and neighbor not in came_from):
                came_from[neighbor] = current
                queue.append(neighbor)
    return reconstruct_path(came_from, start, goal), visited_order

# --- Depth-First Search (DFS) ---
def dfs(maze, start, goal):
    stack = [start]
    came_from = {start: None}
    visited_order = []
    while stack:
        current = stack.pop()
        if current in visited_order:
            continue
        visited_order.append(current)
        if current == goal:
            break
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        random.shuffle(directions) 
        for dx, dy in directions:
            nx, ny = current[0]+dx, current[1]+dy
            neighbor = (nx, ny)
            if (0 <= nx < maze.shape[0] and 0 <= ny < maze.shape[1] and 
                maze[nx, ny] == 0 and neighbor not in came_from):
                came_from[neighbor] = current
                stack.append(neighbor)
    return reconstruct_path(came_from, start, goal), visited_order


# =====================================================
# GIF Generation with Pauses (UPDATED for RGBA colors)
# =====================================================

# Define RGBA colors for various states
COLOR_WALL = np.array([0., 0., 0., 1.])       # Black, Opaque
COLOR_OPEN = np.array([1., 1., 1., 1.])       # White, Opaque
COLOR_VISITED = np.array([0.7, 0.7, 0.7, 1.]) # Light Gray, Opaque
COLOR_PATH = np.array([0.85, 0.65, 0.12, 0.6]) # Gold, 60% Opaque (RGB for gold, last is alpha)

def get_rgba_maze(maze_2d, path_coords=None, visited_coords=None):
    """Converts a 2D maze array into a 3D RGBA array for plotting."""
    h, w = maze_2d.shape
    rgba_maze = np.zeros((h, w, 4))

    # Initialize with walls and open paths
    rgba_maze[maze_2d == 1] = COLOR_WALL
    rgba_maze[maze_2d == 0] = COLOR_OPEN

    # Apply visited color (if provided)
    if visited_coords is not None:
        for r, c in visited_coords:
            # Only color if it's an open path cell and not a wall
            if np.all(rgba_maze[r,c] == COLOR_OPEN):
                rgba_maze[r,c] = COLOR_VISITED
                
    # Apply path color (if provided), blend with background
    if path_coords is not None:
        for r, c in path_coords:
            # This blends the path color over whatever is currently there
            # alpha * foreground_rgb + (1 - alpha) * background_rgb
            current_bg = rgba_maze[r,c, :3]
            alpha = COLOR_PATH[3]
            rgba_maze[r,c, :3] = alpha * COLOR_PATH[:3] + (1 - alpha) * current_bg
            rgba_maze[r,c, 3] = 1.0 # The final pixel is opaque, as we've done the blending

    return rgba_maze


def generate_solver_gif(maze, algorithm_name, start, goal, filename):
    import time
    start_time = time.time()
    
    # 1. Select Algorithm and Run Search
    if algorithm_name == "a_star":
        path, visited = a_star(maze, start, goal)
    elif algorithm_name == "dijkstra":
        path, visited = dijkstra(maze, start, goal)
    elif algorithm_name == "bfs":
        path, visited = bfs(maze, start, goal)
    elif algorithm_name == "dfs":
        path, visited = dfs(maze, start, goal)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm_name}")
    
    total_cells = sum(1 for row in maze for cell in row if cell == 0)  # Count traversable cells
    
    # --- Setup Figure ---
    fig, ax = plt.subplots(figsize=(6,6))
    im = ax.imshow(get_rgba_maze(maze), interpolation='nearest')
    # Initial title (will update with time)
    title_obj = ax.set_title(f"Solving with {algorithm_name.upper()}    Time: 0.00s", loc='left')
    ax.set_xticks([]); ax.set_yticks([])
    ax.plot(start[1], start[0], 'go', markersize=7)
    ax.plot(goal[1], goal[0], 'ro', markersize=7)
    fig.canvas.draw()
    # --------------------

    frames = []
    
    # Keep track of the actual cells that have been visited (for coloring)
    current_visited_cells = set() 

    def capture_frame(current_maze_state, duration_ms=40):
        """Updates the image data and captures the figure as a Pillow Image, with frame duration."""
        # 'current_maze_state' is now expected to be an RGBA array
        im.set_data(current_maze_state)
        fig.canvas.draw()
        
        w, h = fig.canvas.get_width_height()
        buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8).reshape(h, w, 4)
        rgb_image_array = buf[:, :, 1:] # Drop the Alpha channel from Matplotlib's output
        
        frames.append((Image.fromarray(rgb_image_array), duration_ms))

    # 1. Initial State Frame
    capture_frame(get_rgba_maze(maze))

    # 2. Animate visited cells (Exploration)
    step_freq = 5 if algorithm_name in ["a_star", "dijkstra", "bfs"] else 1
    goal_reached_in_visited_loop = False
    
    for i, (r, c) in enumerate(visited):
        current_visited_cells.add((r,c)) # Add to the set of visited cells
        # Update elapsed time in the title
        elapsed_time = time.time() - start_time
        title_obj.set_text(f"Solving with {algorithm_name.upper()}    Time: {elapsed_time:.2f}s")
        # Avoid coloring start/goal with visited color if they're already specifically marked
        if i % step_freq == 0 or i == len(visited) - 1:
            # Generate the RGBA frame for the current state of visited cells
            current_frame_rgba = get_rgba_maze(maze, visited_coords=list(current_visited_cells))
            capture_frame(current_frame_rgba)
            
        if (r, c) == goal and not goal_reached_in_visited_loop:
             # Pause 1 second when the goal is first found
             current_frame_rgba = get_rgba_maze(maze, visited_coords=list(current_visited_cells))
             capture_frame(current_frame_rgba, duration_ms=1000)
             goal_reached_in_visited_loop = True
             # After finding the goal, jump immediately to path tracing
             break 
    
    # 3. Animate final path
    # First, show the maze with all visited cells from the search, but no path yet
    # Then start showing the path, clearing visited cells as it progresses for a cleaner look.
    
    # Create a base RGBA maze with just the original maze and the fully explored visited cells
    # The path will be drawn over this
    base_rgba_for_path = get_rgba_maze(maze, visited_coords=list(current_visited_cells))
    
    # Initialize a temporary path list to build the animated path
    animated_path_coords = []

    path_steps = path[1:-1] # Exclude start and goal from iterated path animation
    
    for i, (r, c) in enumerate(path_steps):
        animated_path_coords.append((r,c))
        
        if i % 2 == 0 or i == len(path_steps) - 1:
            # Get RGBA for base (maze + visited) and then overlay the current animated path
            current_frame_rgba = get_rgba_maze(maze, 
                                               visited_coords=list(current_visited_cells),
                                               path_coords=animated_path_coords)
            capture_frame(current_frame_rgba)

    # 4. Final Pause: Wait 3 seconds
    # Ensure the final full path is shown
    final_rgba_frame = get_rgba_maze(maze, 
                                     visited_coords=list(current_visited_cells),
                                     path_coords=path[1:-1]) # Full path for final frame
    capture_frame(final_rgba_frame, duration_ms=3000)

    plt.close(fig) # Close the figure object

    # Save the frames as a GIF
    if frames:
        images = [img for img, _ in frames]
        durations = [dur for _, dur in frames]
        images[0].save(
            filename,
            format='GIF',
            append_images=images[1:],
            save_all=True,
            duration=durations, 
            loop=0       
        )
        print(f"GIF successfully generated and saved as: {filename}")
        # Return the full frame sequence for the grid GIF
        return frames
    else:
        print(f"No frames generated for {algorithm_name}.")
        return None

# =====================================================
# Grid Comparison GIF Generator (UPDATED for RGBA)
# =====================================================

def generate_comparison_grid_gif(solved_maze_rgba_frames, start, goal, original_maze_2d, filename="comparison_grid.gif"):
    """Creates a 2x2 grid GIF of the final solved mazes."""
    
    algorithms = list(solved_maze_rgba_frames.keys())
    if len(algorithms) != 4:
        print("Error: Need exactly 4 solved mazes for the 2x2 grid.")
        return

    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    axes = axes.flatten()
    frames = []

    # Find the max number of frames among all algorithms
    max_frames = max(len(solved_maze_rgba_frames[algo]) for algo in algorithms)

    # Pad each algorithm's frame list with its last frame if needed
    algo_frames = {}
    for algo in algorithms:
        frames_list = solved_maze_rgba_frames[algo]
        if len(frames_list) < max_frames:
            last_frame = frames_list[-1]
            frames_list = frames_list + [last_frame] * (max_frames - len(frames_list))
        algo_frames[algo] = frames_list

    # Animate the grid frame by frame
    for frame_idx in range(max_frames):
        for i, algo in enumerate(algorithms):
            ax = axes[i]
            ax.clear()
            img, duration = algo_frames[algo][frame_idx]
            ax.imshow(np.asarray(img), interpolation='nearest')
            ax.set_title(algo.upper(), fontsize=12)
            ax.set_xticks([]); ax.set_yticks([])
            ax.plot(start[1], start[0], 'go', markersize=6)
            ax.plot(goal[1], goal[0], 'ro', markersize=6)
        fig.canvas.draw()
        w, h = fig.canvas.get_width_height()
        buf = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8).reshape(h, w, 4)
        rgb_image_array = buf[:, :, 1:]
        # Use the duration of the first algorithm for each frame
        frame_duration = algo_frames[algorithms[0]][frame_idx][1]
        frames.append((Image.fromarray(rgb_image_array), frame_duration))

    plt.close(fig)

    # Save the frames as a GIF
    if frames:
        images = [img for img, _ in frames]
        durations = [dur for _, dur in frames]
        images[0].save(
            filename,
            format='GIF',
            append_images=images[1:],
            save_all=True,
            duration=durations,
            loop=0       
        )
        print(f"\nGIF successfully generated and saved as: {filename}")
    else:
        print("No frames generated for the comparison grid.")


# =====================================================
# Run All Algorithms on the Same Maze
# =====================================================
if __name__ == "__main__":
    
    # Configuration
    WIDTH, HEIGHT = 31, 31
    START = (1, 1)
    GOAL = (HEIGHT - 2, WIDTH - 2)
    ALGORITHMS = ["a_star", "dijkstra", "bfs", "dfs"]
    
    # 1. Generate a single maze 
    print("Generating maze...")
    base_maze = generate_maze(WIDTH, HEIGHT)

    # Dictionary to store the final solved RGBA maze frames for the grid GIF
    final_solved_rgba_frames = {}

    # 2. Loop through all algorithms and generate a GIF for each
    for algo in ALGORITHMS:
        filename = f"{algo}.gif"
        print(f"\nRunning {algo.upper()}")
        
        # The function now returns the final solved maze as an RGBA array
        final_rgba_maze_frame = generate_solver_gif(base_maze.copy(), algo, START, GOAL, filename)
        
        if final_rgba_maze_frame is not None:
             final_solved_rgba_frames[algo] = final_rgba_maze_frame

    # 3. Generate the 2x2 comparison grid GIF
    if len(final_solved_rgba_frames) == 4:
        print("\nCreating 2x2 Comparison Grid GIF with gold paths...")
        # Pass the dictionary of final RGBA frames
        generate_comparison_grid_gif(final_solved_rgba_frames, START, GOAL, base_maze, "algorithm_comparison_grid_gold.gif")
    
    print("\nAll GIF generations complete.")