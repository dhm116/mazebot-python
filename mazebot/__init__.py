import argparse
import sys

# from mazebot import graph
# from mazebot import noops

from mazebot.dijkstra.dijkstra import Dijkstra
from mazebot.graph.graph import Graph
from mazebot.noops.maze import ExampleSolution, Maze
from mazebot.noops.solution import MazeSolution
from mazebot.shared.logging import Logging


def main(argv):
  logger = Logging.logger

  args = _parse_arguments(argv)

  if args.verbose:
    Logging.enable_debugging()

  logger.debug(f'Command Line Arguments: {args}')

  maze = Maze.fetch(args.size)

  logger.info(maze)

  graph = Graph.from_maze(maze)

  maze.print()

  dijkstra = Dijkstra(nodes=graph.nodes, starting_node=maze.start)

  shortest_path = dijkstra.shortest_path_to(maze.finish)

  # solution_steps = Maze.directions_for_solution(shortest_path)
  solution = MazeSolution(*shortest_path)

  maze.print(solution=solution)
  result = maze.submit(solution=solution)
  logger.info(result)


def _parse_arguments(argv):
  parser = argparse.ArgumentParser(description='Noops challenge MazeBot solver')
  parser.add_argument(
      '-s',
      '--size',
      type=int,
      default=10,
  )
  parser.add_argument(
      '-vv',
      '--verbose',
      action='store_true',
      help='print out extra logging information while running')
  return parser.parse_args(argv[1:])


def run_main():
  try:
    sys.exit(main(sys.argv))
  except Exception as err:
    sys.stderr.write(str(err))
    sys.exit(1)


if __name__ == '__main__':
  run_main()
