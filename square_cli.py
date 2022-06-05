from argparse import ArgumentParser
from ast import arg
from squares import Square, SquareCanvas

parser = ArgumentParser()
parser.add_argument("-s", "--square_list", dest="square_list",
                    help="Specify square radius list to populate.")

parser.add_argument(
    "-f", "--fill_canvas_size", dest='canvas_size',
    help="Specify canvas size to fill supllied square_list with."
     )

parser.add_argument(
    "-a", "--array_display",
    default="True",
    help="Show numpy array structure after computation completes."
)


def main():
    args = parser.parse_args()
    print(args)

    if args.square_list is not None:
        list_square_radii = [int(i) for i in args.square_list.replace(",", "").split(" ")]
        list_squares = [Square(radius) for radius in list_square_radii]
        
    if args.canvas_size is not None:
        canvas = SquareCanvas(max_bound=int(args.canvas_size), contents=list_squares)
    
    if (args.array_display).lower() not in ["f", "false", "none"]:
        print(canvas.frame)

    

if __name__ == "__main__":
    main()