def is_safe(graph, vertex, color, num_of_vertices):
  """
  Checks if it's safe to assign a color to a vertex.
  """
  for neighbor in range(num_of_vertices):
    if graph[vertex][neighbor] == 1 and color[neighbor] == color:
      return False
  return True

def graph_coloring_util(graph, m, color, current_index, num_of_vertices):
  """
  Recursive function to find valid colorings.
  """
  if current_index == num_of_vertices:
    # Base case: All vertices colored, print the solution
    print("Coloring found:", color)
    return True

  # Try all colors for the current vertex
  for c in range(1, m + 1):
    if is_safe(graph, current_index, color, num_of_vertices):
      color[current_index] = c
      # Recursively try coloring remaining vertices
      if graph_coloring_util(graph, m, color, current_index + 1, num_of_vertices):
        return True
      # Backtrack if assigning color c doesn't lead to a solution
      color[current_index] = -1

  # No valid coloring found
  return False

def graph_coloring(graph, m):
  """
  Main function to initiate the backtracking process.
  """
  num_of_vertices = len(graph)
  color = [-1] * num_of_vertices  # Initialize color array
  if graph_coloring_util(graph, m, color, 0, num_of_vertices) == False:
    print("No solution exists")


# Example usage
graph = [[0, 1, 1, 1],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [1, 0, 1, 0]]
m = 3  # Number of colors

graph_coloring(graph, m)