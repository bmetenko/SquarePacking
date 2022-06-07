from argparse import ArgumentParser
from typing import List, Dict

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
    "-o", "--output_file",
    default=None,
    help="Send output to specified filepath."
    "Image type inferred by extension type."
    "Overrides array display and plot display."
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

        if args.plot_display is not None:
            args.array_display = "false"

            if args.output_file is None:
                canvas.generate_plotly(render=args.plot_display)

            else:
                canvas.generate_plotly(out_file=args.output_file)
    
        if args.array_display.lower() not in ["f", "false", "none"]:
            print(canvas.contents)
            print(canvas.frame)



if __name__ == "__main__":
    main()
