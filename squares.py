# noinspection PyUnresolvedReferences
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
from itertools import cycle

palette = cycle(plotly.colors.qualitative.Light24)


class Square:

    def __init__(self, side):
        self._center = None
        self._area = None
        self.side = float(side)
        self.coordinates = [
            [0, 0], [0, side], [side, 0], [side, side]
        ]  # (x, y)

        self.length = self.side
        self.width = self.side
        self.xy_symmetry = self.length != self.width

    def __repr__(self):
        return f"Square{int(self.side)}::ctr@{self.center}"

    @property
    def area(self):
        self._area = self.side ** 2
        return self._area

    @property
    def center(self):
        self._center = [
            (self.coordinates[0][0] + self.coordinates[3][0]) / 2,
            (self.coordinates[0][1] + self.coordinates[3][1]) / 2,
        ]
        return self._center

    def add_x(self, displacement):
        for v, _ in enumerate(self.coordinates):
            self.coordinates[v][0] += displacement

        return self.coordinates

    def add_y(self, displacement):
        for v, _ in enumerate(self.coordinates):
            self.coordinates[v][1] += displacement

        return self.coordinates

    def add_xy(self, x0, y0):
        self.add_x(x0)
        self.add_y(y0)

        return self.coordinates


class SquareCanvas:

    def __init__(
            self,
            max_bound=None,
            contents=None,
            frame_override=None,
            validate=True,
            rotation=True
    ):
        if contents is None:
            contents = []
        self._contents = []

        if max_bound is None:
            max_bound = 10

        if frame_override is None:
            self.frame = np.zeros((max_bound, max_bound), dtype=int)
        else:
            self.frame = frame_override

        self.rotation_allowed = rotation

        self.x_max = self.frame.shape[0]
        self.y_max = self.frame.shape[1]
        self.x_min = 0
        self.y_min = 0

        sorted(contents, key=lambda x: x.length * x.width, reverse=True)

        for sq in contents:
            self.add_contents(sq)

        if validate:
            self.check_all_filled(contents)

    def add_contents(self, sq: Square):
        for (x, y), value in np.ndenumerate(self.frame):
            if value == 0:

                length = sq.length
                width = sq.width

                rotate = not sq.xy_symmetry and self.rotation_allowed
                if rotate:
                    if x + length > self.x_max and x + width > self.x_max:
                        continue
                    if y + width > self.y_max and y + length > self.y_max:
                        continue
                else:
                    if x + length > self.x_max:
                        continue
                    if y + width > self.y_max:
                        continue

                fit, rotate = check_bounds(sq, self.frame, x, y, rotation=rotate)

                if not fit:
                    continue

                self._contents.append(sq)
                sq.add_xy(x, y)
                x_ = list(range(int(length if not rotate else width)))
                y_ = list(range(int(width if not rotate else length)))
                for cellx in x_:
                    for celly in y_:
                        y0 = celly + y
                        x0 = cellx + x

                        self.frame[x0][y0] = int(len(self._contents))

                break

    def check_all_filled(self, contents):
        if np.amax(self.frame) != int(len(contents)):
            raise IndexError("Not all placed...")

    @property
    def x_list(self):
        return [i.center[0] for i in self.contents]

    @property
    def y_list(self):
        return [i.center[1] for i in self.contents]

    @property
    def center_list(self):
        return [str(i.center) for i in self.contents]

    @property
    def contents(self):
        return self._contents

    def generate_plotly(self, show_text=True, use_palette=palette):
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=self.x_list,
                y=self.y_list,
                text=self.center_list,
                mode="markers+text" if show_text else "markers",
                textposition="bottom center",
                textfont=dict(family="sans serif", size=13, color="green"),
            ))

        fig.update_xaxes(range=[0, self.x_max])
        fig.update_yaxes(range=[0, self.y_max])

        shape_list = []

        for sq in self.contents:
            shape_list.append(
                dict(type="rect",
                     x0=sq.coordinates[0][0],
                     y0=sq.coordinates[0][1],
                     x1=sq.coordinates[3][0],
                     y1=sq.coordinates[3][1],
                     line=dict(color="RoyalBlue"),
                     fillcolor=next(use_palette),
                     opacity=0.2))

        for (x, y), value in np.ndenumerate(self.frame):
            if value == -1:
                shape_list.append(
                    dict(type="rect",
                         x0=x,
                         y0=y,
                         x1=x + 1,
                         y1=y + 1,
                         line=dict(color="RoyalBlue"),
                         fillcolor="black",
                         opacity=0.5))

            if value == 0:
                shape_list.append(
                    dict(type="rect",
                         x0=x,
                         y0=y,
                         x1=x + 1,
                         y1=y + 1,
                         line=dict(color="RoyalBlue"),
                         fillcolor="white",
                         opacity=0.5))

        fig.update_layout(
            width=600,
            height=600,
            shapes=shape_list
        )
        fig.show()


def check_bounds(sq: Square, frame: np.array, x: float, y: float, rotation=False):
    out = True
    rotated = False

    for cellx in list(range(int(sq.length))):
        for celly in list(range(int(sq.width))):
            y0 = celly + y
            x0 = cellx + x

            if int(frame[x0][y0]) != 0:
                out = False

    if rotation and out is False:
        out = True
        rotated = True
        for cellx in list(range(int(sq.width))):
            for celly in list(range(int(sq.length))):
                y0 = celly + y
                x0 = cellx + x

                if int(frame[x0][y0]) != 0:
                    out = False

    return out, rotated


class Rect:

    def __init__(self, length, width):
        self._center = None
        self._area = None
        self.length = float(length)
        self.width = float(width)
        self.coordinates = [
            [0, 0], [0, width], [length, 0], [length, width]
        ]  # (x, y)

        self.xy_symmetry = self.length != self.width

    def __repr__(self):
        return f"Rect{int(self.length)}x{self.width}::ctr@{self.center}"

    @property
    def area(self):
        self._area = self.length * self.width
        return self._area

    @property
    def center(self):
        self._center = [
            (self.coordinates[0][0] + self.coordinates[3][0]) / 2,
            (self.coordinates[0][1] + self.coordinates[3][1]) / 2,
        ]
        return self._center

    def add_x(self, displacement):
        for v, _ in enumerate(self.coordinates):
            self.coordinates[v][0] += displacement

        return self.coordinates

    def add_y(self, displacement):
        for v, _ in enumerate(self.coordinates):
            self.coordinates[v][1] += displacement

        return self.coordinates

    def add_xy(self, x0, y0):
        self.add_x(x0)
        self.add_y(y0)

        return self.coordinates
