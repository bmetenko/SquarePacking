from argparse import ArgumentParser
from typing import List, Dict

import numpy as np
import PIL
import PIL.Image

from squares import Rect, Square, SquareCanvas

parser = ArgumentParser()
parser.add_argument("-s", "--square_list", dest="square_list",
                    help="Specify square radius list to populate.")

parser.add_argument("-r", "--rect_list", dest="rect_list",
                    help="Specify rectangles ( ex. '[1x3]*3, [4x3]*2' ) list to populate.")

parser.add_argument(
    "-f", "--fill_canvas_size", dest='canvas_size',
    help="Specify canvas size to fill supllied square_list with."
     )

parser.add_argument(
    "-a", "--array_display",
    default="True",
    help="Show numpy array structure after computation completes."
)

parser.add_argument(
    "-p", "--plot_display",
    default="browser",
    help="Display plotly plot in browser. Overrides array display."
)

parser.add_argument(
    "-i0", "--input_image_zero",
    dest='image_zero',
    default=None,
    help=\
    "Input based on image parsing, where pure white is a placable 'tile', "
    "and any other color is blocked. Overrides canvas_size."
)

parser.add_argument(
    "-ia", "--input_image_average",
    dest="image_average",
    default=None,
    help=\
    "Input based on image parsing, images averaged into 0s and 1s and used to fill 'tiles'. "
    "Overrides canvas_size, and input_image_zero"
)

parser.add_argument(
    "-ir", "--image_rotate",
    dest="image_rotate",
    default=0,
    help=\
    "Rotates provided image by specified degrees, if present, before population."
)

parser.add_argument(
    "-o", "--output_file",
    default=None,
    help="Send output to specified filepath."
    "Image type inferred by extension type."
    "Overrides array display and plot display."
)

parser.add_argument(
    "-dp", "--display_points",
    dest="display_points",
    default=True,
    help=\
    "Toggle display of point values in ouput."
)

def count_expand(expand_dict:  List[Dict[str, int]]):
    out_list = []

    for element in expand_dict:
        for _ in list(range(0, element['count'])):
            out_list.append({
                "length": element['length'],
                "width": element['width']}
            )

    return out_list


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

        list_shapes = list_shapes + [
            Rect(length=element['length'], width=element['width']) for element in list_rects
        ]
        
    if args.canvas_size is not None:
        canvas = SquareCanvas(max_bound=int(args.canvas_size), contents=list_shapes)

    if args.image_zero is not None:
        I = np.asarray(PIL.Image.open(args.image_zero)).astype(int)

        # transform black and white
        where_not0 = np.where(I != 0)
        where_0 = np.where(I == 0)

        I[where_0] = 0
        I[where_not0] = -1

    if args.image_average is not None:
        img = PIL.Image.open(args.image_average)
        thresh = np.asarray(img).astype(int).mean(axis=0).mean()
        fn = lambda x : 255 if x > thresh else 0
        img = img.convert('L').point(fn, mode='1')
        I = np.asarray(img).astype(int)
    
    if "img" in locals():
        img = img.rotate(int(args.image_rotate), expand=True)
        I = np.asarray(img).astype(int)
        
    canvas = SquareCanvas(frame_override=I, contents=list_shapes)
    display_text = args.display_points.lower() not in ["f", "false", "none"]

    if "canvas" in locals():
        if args.plot_display is not None:
            args.array_display = "false"

            if args.output_file is None:
                canvas.generate_plotly(render=args.plot_display, show_text=display_text)

            else:
                canvas.generate_plotly(out_file=args.output_file, show_text=display_text)

        if args.array_display.lower() not in ["f", "false", "none"]:
            print(canvas.contents)
            print(canvas.frame)



if __name__ == "__main__":
    main()
