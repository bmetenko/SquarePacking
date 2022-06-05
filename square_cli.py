from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-s", "--square_list", dest="square_list",
                    help="Specify square radius list to populate.")

parser.add_argument(
    "-f", "--fill_canvas_size", dest='canvas_size',
    help="Specify canvas size to fill supllied square_list with."
     )


def main():
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()