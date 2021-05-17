import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random
import numpy as np
import math
from pprint import pprint

from typing import Tuple, Callable, List, Union

# Constants
ENV_SIZE = (300, 300)

START_PT = (100, 100)
END_POINT = (250, 200)
GOAL_RADIUS = 5

STEP_SIZE = 10

MAX_ITER = 10_000

OBSTACLES = [
    # Follows the format - [x, y, radius]
    [150, 150, 4],
    [180, 180, 2],
    [200, 200, 10],
    [10, 100, 5],
]


# Class to represent a node
class Node:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.trace_x = []
        self.trace_y = []

    def get_trace(self) -> Tuple[List[int], List[int]]:
        return self.trace_x, self.trace_y

    def get_points(self) -> Tuple[int, int]:
        return self.x, self.y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


# Main class to perform RRT
class RRT:
    def __init__(
        self,
        env_size: Tuple[int, int] = ENV_SIZE,
        start_pt: Tuple[int, int] = START_PT,
        end_pt: Tuple[int, int] = END_POINT,
        goal_radius: int = GOAL_RADIUS,
        step_size: int = STEP_SIZE,
        max_iter: int = MAX_ITER,
        obstacles: List[List[int]] = OBSTACLES,
    ) -> None:
        self.points = []
        self.iter = 0

        self.env_size = env_size
        self.start_pt = start_pt
        self.end_pt = end_pt
        self.goal_radius = goal_radius
        self.step_size = step_size
        self.max_iter = max_iter
        self.obstacles = obstacles

        self.height = self.env_size[0]
        self.width = self.env_size[1]

        self.points.append(Node(*self.start_pt))
        self.points[-1].trace_x = [self.start_pt[0]]
        self.points[-1].trace_y = [self.start_pt[1]]

        # Simple Helper Utils
        self.__in_limits: Callable[[int, int], bool] = lambda x, y: not (
            x < 0 or y < 0 or x > self.height or y > self.width
        )
        self.__generate_random: Callable[[None], Tuple[int, int]] = lambda: (
            random.randint(0, self.height),
            random.randint(0, self.width),
        )
        self.__final_state: Callable[[int, int], bool] = (
            lambda x, y: (x - self.end_pt[0]) ** 2 + (y - self.end_pt[1]) ** 2
            <= self.goal_radius ** 2
        )
        self.__np_arr: Callable[
            List[Union[int, float]], np.ndarray
        ] = lambda *arr: np.array(arr)

    def __minimum_distance_idx(self, x: int, y: int) -> int:
        dists = [
            np.linalg.norm(np.subtract(list(self.points[i].get_points()), [x, y]))
            for i in range(len(self.points))
        ]
        return np.argmin(dists)

    def __collision(self, x1: int, y1: int, x2: int, y2: int) -> bool:
        for obstacle in self.obstacles:
            d = self.__np_arr(x2, y2) - self.__np_arr(x1, y1)
            f = self.__np_arr(obstacle[0], obstacle[1]) - self.__np_arr(x1, y1)

            a = np.dot(d, d)
            b = 2 * np.dot(f, d)
            c = np.dot(f, f) - obstacle[2] ** 2

            discriminant = (b ** 2) - (4 * a * c)
            if discriminant < 0:
                continue

            discriminant = np.sqrt(discriminant)
            t1 = (-b - discriminant) / (2 * a)
            t2 = (-b + discriminant) / (2 * a)

            if (t1 >= 0 and t1 <= 1) or (t2 >= 0 and t2 <= 1):
                return True

        return False

    def __get_path(self) -> List[Tuple[int, int]]:
        x, y = self.points[-1].get_trace()
        return [(x[i], y[i]) for i in range(len(x))]

    def run(
        self,
    ) -> Tuple[Union[str, List[Tuple[int, int]]], Union[plt.Figure, str], int]:
        for i in range(self.max_iter):
            rand_x, rand_y = self.__generate_random()
            near_idx = self.__minimum_distance_idx(rand_x, rand_y)

            near_x, near_y = self.points[near_idx].get_points()
            trace_near_x, trace_near_y = self.points[near_idx].get_trace()

            direct_dist = np.linalg.norm(
                self.__np_arr(near_x, near_y) - self.__np_arr(rand_x, rand_y)
            )

            if direct_dist < self.step_size:
                continue

            # Possibility of casting to int
            x_forward = (
                rand_x * self.step_size + (direct_dist - self.step_size) * near_x
            ) / direct_dist
            y_forward = (
                rand_y * self.step_size + (direct_dist - self.step_size) * near_y
            ) / direct_dist

            if not self.__in_limits(x_forward, y_forward):
                continue
            if self.__collision(near_x, near_y, x_forward, y_forward):
                continue

            self.points.append(Node(x_forward, y_forward))
            self.points[-1].trace_x = [*trace_near_x, x_forward]
            self.points[-1].trace_y = [*trace_near_y, y_forward]

            if self.__final_state(x_forward, y_forward):
                self.iter = i
                break

        else:
            print("No path")
            print(f"{self.max_iter} iterations taken")
            return ("No Path", "", self.max_iter)

        print("Done. Path Taken: ")
        print(f"{self.iter} iterations taken")
        pprint(self.__get_path())

        fig, ax = plt.subplots()
        plt.title("RRT Graph")
        for obstacle in self.obstacles:
            c = plt.Circle(
                xy=(obstacle[0], obstacle[1]),
                radius=obstacle[2],
                color="blue",
                fill=True,
            )
            ax.add_patch(c)
        plt.scatter(*self.start_pt, color="green")
        ax.add_patch(
            plt.Circle(xy=self.end_pt, radius=self.goal_radius, color="red", fill=True)
        )
        plt.xlim([0, self.height])
        plt.ylim([0, self.width])

        plt.legend(
            handles=[
                mpatches.Patch(color="green", label="Start Point"),
                mpatches.Patch(color="red", label="End Point"),
                mpatches.Patch(color="blue", label="Obstacles"),
            ],
            loc="center left",
            bbox_to_anchor=(1, 0.5),
        )

        for x in range(len(self.points)):
            plt.plot(self.points[x].get_trace()[0], self.points[x].get_trace()[1])

        plt.tight_layout()
        return (self.__get_path(), fig, self.iter)


if __name__ == "__main__":
    RRT().run()
    plt.show()
