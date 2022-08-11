#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------
# Created By : bmetenko
# Start Date : 22May2022
# Project URL: https://github.com/bmetenko/SquarePacking
# ---------------

"""
Implementation and visualization logic for 
packing squares or rectangles on a square canvas.
"""

from itertools import cycle
from optparse import Option
from typing import List, Dict, Optional, Union
import pandas as pd
import numpy as np


class Square:
    __slots__ = (
        '_center', '_area', "side", 
        "coordinates", "length", "width", "rotate_times",
        "extra"
        )

    def __init__(
        self, 
        side: int,
        extra: Optional[Dict[str, Union[int, str]]] = None
    ):
        if extra is None:
            extra = {}

        self._center = None
        self._area = None
        self.side = float(side)
        self.coordinates = [
            [0, 0], [0, side], [side, 0], [side, side]
        ]  # (x, y)

        self.length = self.side
        self.width = self.side
        self.rotate_times = 1

        self.extra = extra

    def __repr__(self):
        return f"Square{int(self.side)}::ctr@{self.center}"

    @property
    def area(self) -> float:
        self._area = self.side ** 2
        return self._area

    @property
    def center(self) -> List[float]:
        self._center = [
            (self.coordinates[0][0] + self.coordinates[3][0]) / 2,
            (self.coordinates[0][1] + self.coordinates[3][1]) / 2,
            ]
        return self._center

    def add_x(self, displacement: int) -> List[List]:
        for v, _ in enumerate(self.coordinates):
            self.coordinates[v][0] += displacement

        return self.coordinates

    def add_y(self, displacement: int) -> List[List]:
        for v, _ in enumerate(self.coordinates):
            self.coordinates[v][1] += displacement

        return self.coordinates

    def add_xy(self, x0: int, y0: int) -> List[List]:
        self.add_x(x0)
        self.add_y(y0)

        return self.coordinates


def rotate_matrix(angle: Union[int, float]) -> np.array:
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    r = np.array(((c, -s), (s, c)))
    return r


class Rect:

    __slots__ = (
        "_area", "_center", "length",
        "width", "coordinates", "rotate_times",
        "extra"
        )

    def __init__(
        self, 
        length: int, 
        width: int,
        extra: Optional[Dict[str, Union[int, str]]] = None
    ):

        if extra is None:
            extra = {}

        self._area = None
        self._center = None
        self.length = float(length)
        self.width = float(width)
        self.coordinates = [
            [0, 0], [0, width], [length, 0], [length, width]
        ]  # (x, y)

        self.rotate_times = 4

        self.extra = extra

    def __repr__(self):
        return f"Rect{int(self.length)}x{int(self.width)}::ctr@{self.center}"

    @property
    def area(self) -> float:
        self._area = self.length * self.width
        return self._area

    @property
    def center(self) -> List[float]:
        self._center = [
            (self.coordinates[0][0] + self.coordinates[3][0]) / 2,
            (self.coordinates[0][1] + self.coordinates[3][1]) / 2,
            ]
        return self._center

    def add_x(self, displacement: int) -> List[List]:
        for v, _ in enumerate(self.coordinates):
            self.coordinates[v][0] += displacement

        return self.coordinates

    def add_y(self, displacement: int) -> List[List]:
        for v, _ in enumerate(self.coordinates):
            self.coordinates[v][1] += displacement

        return self.coordinates

    def add_xy(self, x0: int, y0: int) -> List[List]:
        self.add_x(x0)
        self.add_y(y0)

        return self.coordinates

    def rotate(self, angle: Union[int, float] = 90):

        r = rotate_matrix(angle)

        # Calculate rotation matrix conversion
        self.coordinates = np.round(self.coordinates @ r.T)

        # Recentering on 0,0 for x and y
        min_x = np.round(min(np.hsplit(self.coordinates, 2)[0]))
        min_y = np.round(min(np.hsplit(self.coordinates, 2)[1]))

        if min_x < 0:
            self.add_x(-min_x)
        if min_y < 0:
            self.add_y(-min_y)

        # Fixes placing
        l, w = self.length, self.width
        self.width, self.length = l, w

        self.coordinates = [
            self.coordinates[1],
            self.coordinates[3],
            self.coordinates[0],
            self.coordinates[2]
        ]

        return self


class SquareCanvas:

    def __init__(
            self,
            max_bound: int = None,
            contents: Optional[List[Union[Square, Rect]]] = None,
            frame_override: np.ndarray = None,
            validate: bool = True,
            allow_rotation: bool = True
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

        self.x_max = self.frame.shape[0]
        self.y_max = self.frame.shape[1]
        self.x_min = 0
        self.y_min = 0

        sorted(contents, key=lambda x: x.length * x.width, reverse=True)
        self.rotation = allow_rotation

        for sq in contents:
            self.add_contents(sq)

        if validate:
            self.check_all_filled(contents)

    def add_contents(self, sq: Union[Square, Rect]):
        placed = False
        max_rotate = sq.rotate_times if self.rotation else 1
        for rot in list(range(0, max_rotate)):
            if not placed:
                sq = sq.rotate(90*rot) if isinstance(sq, Rect) else sq
                length = sq.width  # swap arbitrary since handled elsewhere
                width = sq.length

                for (x, y), value in np.ndenumerate(self.frame):
                    if value == 0 and not placed:

                        if x + length > self.x_max or x + length < 0:
                            continue
                        if y + width > self.y_max or y + width < 0:
                            continue

                        fit = check_bounds(self.frame, x, y, length, width)

                        if not fit:
                            continue

                        placed = True
                        self._contents.append(sq)
                        sq.add_xy(x, y)
                        for cellx in list(range(int(length))):
                            for celly in list(range(int(width))):
                                y0 = celly + y
                                x0 = cellx + x

                                self.frame[x0][y0] = int(len(self._contents))
            
        if not placed:
            raise IndexError("Not all placed...")

        return self
    
    def contents_frame(self) -> pd.DataFrame:
        out_df = pd.DataFrame()

        out_df["def"] = [str(sq) for sq in self._contents] 
        out_df["x_start"] = self.x_list
        out_df["y_start"] = self.y_list
        out_df["center"] = self.center_list
        out_df["area"] = [sq.area for sq in self._contents]
        out_df["length"] = [sq.length for sq in self._contents]
        out_df["width"] = [sq.width for sq in self._contents] 
        
        # region extra payload column logic
        extra_properties = [sq.extra for sq in self._contents]
        extra_properties_list = {k for i in extra_properties for k in i.keys()}

        for prop in extra_properties_list:
            out_df[prop] = [
                    sq.extra[prop] 
                    if prop in sq.extra.keys() 
                    else np.nan 
                    for sq in self._contents 
                ]

        # endregion

        return out_df

    def autofill(self, max_side: int, square_only: bool = False):
        fill_size = max_side

        if square_only:
            while True:

                sq = Square(side=fill_size)

                try:
                    self.add_contents(sq)
                except IndexError:
                    fill_size = fill_size - 1

                if fill_size == 0:
                    break
        else:
            x_side, y_side = \
                max_side, max_side

            while True:

                rec = Rect(x_side, y_side)

                try:
                    self.add_contents(rec)
                except IndexError:
                    rotated = False

                    if self.rotation:
                        try:
                            self.add_contents(rec.rotate())
                            rotated = True
                        except IndexError:
                            pass

                    if not rotated:
                        if x_side == y_side:
                            x_side -= 1
                        else:
                            y_side -= 1

                if x_side == 0:
                    break

        return self

    def check_all_filled(self, contents: List[Union[Square, Rect]]) -> None:
        max_frame = np.amax(self.frame)
        max_contents = int(len(contents))
        if max_frame != max_contents:
            print(f"{max_frame=}, {max_contents=}")
            raise IndexError("Not all placed...")

    @property
    def x_list(self) -> List[float]:
        return [i.center[0] for i in self.contents]

    @property
    def y_list(self) -> List[float]:
        return [i.center[1] for i in self.contents]

    @property
    def center_list(self) -> List[str]:
        return [str(i.center) for i in self.contents]

    @property
    def contents(self):
        return self._contents

    def remove(
        self, 
        lw_tuple=None, 
        element: Optional[Union[Square, Rect]]=None,
        silent_fail: bool=True
        ):
        if lw_tuple is None and element is None:
            raise \
                KeyError(
                    "Nothing specified to remove from Square Canvas. "
                    "Please pass in a length width tuple or Square|Rect "
                    "element or lists of the specified."
                )

        if lw_tuple is not None \
            or element is not None:

            lw_list = lw_tuple

            if lw_tuple is None \
                and element is not None:
                if isinstance(element, list):
                    lw_list = [(el.length, el.width) for el in element]
                else:
                    lw_list = [(element.length, element.width)]

            contents = self.contents.copy()
            for lw_tuple in lw_list:
                removed=False
                for elem in contents:
                    if not removed:
                        if elem.length == lw_tuple[0] \
                            and elem.width == lw_tuple[1]:
                            contents.remove(elem)
                            removed=True

                if not removed and not silent_fail:
                    raise IndexError(
                        f"Could not remove element with (l,w) of {lw_tuple}"
                        )
                            
            # TODO: can fail silently, add toggle.

            self._contents = contents

        return self

    def generate_plotly(
        self, 
        show_text: bool = True,
        palette: List = None,
        render: str = "svg",
        out_file: str = None,
        trace_path: bool = False
            ):
        
        import plotly
        import plotly.graph_objects as go

        if palette is None:
            palette = cycle(plotly.colors.qualitative.Light24)

        fig = go.Figure()
        
        scatter_mode = "markers"
        scatter_mode += "+text" if show_text else ''
        scatter_mode += "+lines" if trace_path else ''

        fig.add_trace(
            go.Scatter(
                x=self.x_list,
                y=self.y_list,
                text=self.center_list,
                mode=scatter_mode,
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
                     fillcolor=next(palette),
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
            shapes=shape_list
        )
        
        if out_file is None \
                and render != "object":
            if render == "browser":
                fig.update_layout(autosize=True)
            else:
                fig.update_layout(
                    width=600,
                    height=600
                )

            fig.show(renderer=render)
        else:
            if render == "object":
                return fig
            
            else:
                fig.write_image(out_file)


# noinspection PyUnusedLocal
def check_bounds(
        frame: np.array,
        x: float,
        y: float,
        length: Union[int, float],
        width: Union[int, float]
) -> bool:
    out = True

    for cellx in list(range(int(length))):
        for celly in list(range(int(width))):
            y0 = celly + y
            x0 = cellx + x

            if int(frame[x0][y0]) != 0:
                out = False
    return out
