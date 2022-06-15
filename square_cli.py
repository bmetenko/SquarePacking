from argparse import ArgumentParser
from typing import List, Dict

import numpy as np
import PIL
import PIL.Image

from squares import Rect, Square, SquareCanvas

parser = ArgumentParser()
parser.add_argument(
    "-s", "--square_list", dest="square_list",
    help="Specify square radius list to populate."
)

parser.add_argument(
    "-r", "--rect_list", dest="rect_list",
    help="Specify rectangles ( ex. '[1x3]*3, [4x3]*2' ) list to populate."
)

parser.add_argument(
    "-f", "--fill_canvas_size", dest='canvas_size',
    help="Specify canvas size to fill supllied square_list with."
)

parser.add_argument(
    "-a", "--array_display", default="True",
    help="Show numpy array structure after computation completes."
)

parser.add_argument(
    "-p", "--plot_display", default="browser",
    help="Display plotly plot in browser. Overrides array display."
)

parser.add_argument(
    "-i0", "--input_image_zero", dest='image_zero', default=None,
    help="Input based on image parsing, where pure white is a placable 'tile', " +
         "and any other color is blocked. Overrides canvas_size."
)

parser.add_argument(
    "-ia", "--input_image_average", dest="image_average", default=None,
    help="Input based on image parsing, " +
         "images averaged into 0s and 1s and used to fill 'tiles'. " +
         "Overrides canvas_size, and input_image_zero"
)

parser.add_argument(
    "-ir", "--image_rotate", dest="image_rotate", default=0,
    help="Rotates provided image by specified degrees, if present, before population."
)

parser.add_argument(
    "-o", "--output_file", default=None,
    help="Send output to specified filepath." +
         "Image type inferred by extension type." +
         "Overrides array display and plot display."
)

parser.add_argument(
    "-ar", "--autopopulate_rectangles_max_side",
    dest="rect_max_side",
    default=None,
    help="Specify autopopulation of remaining canvas " +
         "with rectangles starting with maximum sides supplied. " +
         "Overrides square population using -as argument."
)

parser.add_argument(
    "-as", "--autopopulate_squares_max_side", dest="square_max_side", default=None,
    help="Specify autopopulation of remaining canvas " +
         "with squares starting with maximum sides supplied. "
)


def count_expand(expand_dict: List[Dict[str, int]]):
    out_list = []

    for element in expand_dict:
        for _ in list(range(0, element['count'])):
            out_list.append({
                "length": element['length'],
                "width": element['width']}
            )

    return out_list


parser.add_argument(
    "-dp", "--display_points",
    dest="display_points",
    action='store_true',
    help="Toggle display of center point values in ouput."
)

parser.add_argument(
    "-dpp", "--display_path_points",
    dest="display_path_points",
    action='store_true',
    help="Toggle display of element addition path."
)

parser.add_argument(
    '-dr', '--disallow_rotation',
    dest="disallow_rotation",
    action='store_true',
    help='toggle to dissallow rotation of rectangles when adding to SquareCanvas.'
)


# noinspection PyTypeChecker
def main():
    args = parser.parse_args()
    print(args)

    list_shapes = []

    if args.square_list is not None:
        list_square_radii = [int(i) for i in args.square_list.replace(",", "").split(" ")]
        list_shapes = list_shapes + [Square(radius) for radius in list_square_radii]

    if args.rect_list is not None:
        list_rect_defs = args.rect_list.replace(",", "").split(" ")
        dict_list_rects = [
            {
                "count": int(rect.split("*")[1]),
                "length": int(rect.split("[")[1].split("x")[0]),
                "width": int(rect.split("[")[1].split("x")[1].split("]")[0])
            }
            for rect in list_rect_defs
        ]

        list_rects = count_expand(dict_list_rects)

        # noinspection PyTypeChecker
        list_shapes = list_shapes + [
            Rect(length=element['length'], width=element['width']) for element in list_rects
        ]

    if args.canvas_size is not None:
        canvas = SquareCanvas(
            max_bound=int(args.canvas_size),
            contents=list_shapes,
            allow_rotation=(not args.disallow_rotation)
        )

    if args.image_zero is not None:
        # noinspection PyTypeChecker
        image = np.asarray(PIL.Image.open(args.image_zero)).astype(int)

        # transform black and white
        where_not0 = np.where(image != 0)
        where_0 = np.where(image == 0)

        image[where_0] = 0
        image[where_not0] = -1

    if args.image_average is not None:
        img = PIL.Image.open(args.image_average)
        thresh = np.asarray(img).astype(int).mean(axis=0).mean()
        img = img.convert('L').point(lambda x: 255 if x > thresh else 0, mode='1')
        image = np.asarray(img).astype(int)

    if "img" in locals():
        # noinspection PyUnboundLocalVariable
        img = img.rotate(int(args.image_rotate), expand=True)
        image = np.asarray(img).astype(int)
        image = image * -1 if np.amax(image) == 1 else image

    # noinspection PyUnboundLocalVariable
    canvas = SquareCanvas(
        frame_override=image if "image" in locals() else None,
        contents=list_shapes,
        allow_rotation=(not args.disallow_rotation)
    )

    display_text = args.display_points
    display_path = args.display_path_points

    if "canvas" in locals():

        if args.rect_max_side is not None:
            canvas.autofill(max_side=int(args.rect_max_side), square_only=False)

        if args.square_max_side is not None:
            canvas.autofill(max_side=int(args.square_max_side), square_only=True)

        if args.plot_display is not None:
            args.array_display = "false"

            if args.output_file is None:
                canvas.generate_plotly(
                    render=args.plot_display, 
                    show_text=display_text,
                    trace_path=display_path
                    )

            else:
                canvas.generate_plotly(
                    out_file=args.output_file, 
                    show_text=display_text,
                    trace_path=display_path
                    )

        if args.array_display.lower() not in ["f", "false", "none"]:
            print(canvas.contents)
            print(canvas.frame)


if __name__ == "__main__":
    main()
