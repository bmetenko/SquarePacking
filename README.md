# Simple OOP based square packing implementation
[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=logo=Jupyter)](https://jupyter.org/try)
 [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) ![Project_Type](https://img.shields.io/badge/project%20type-toy-blue)

Simple OOP (class-based) implementation of packing Square instances into a SquareCanvas.

Main functionality of the code exemplified in the pySquares.ipynb. 

Maintenance or updates unclear since only a toy project.

Live demo functionality POC, using pyscript web integration, available at https://bmetenko.github.io/SquarePacking/

Please note that loading and processing of larger images will take time.

Current command-line example:
```console
$ python3 square_cli.py -s "1 2 3 4 3" -f 7 -a true

$ echo "Expanded arguments of above:"
$ python3 square_cli.py --square_list "1 2 3 4 3" --fill_canvas_size 7 --array_display true
```

```console
$ python3 square_cli.py -s "1 2 3 4 3" -r "[3x2]*4" -f 9 -a true

$ echo "Expanded arguments of above:"
$ python3 square_cli.py --square_list "1 2 3 4 3" --rect_list "[3x2]*4" --fill_canvas_size 9 --array_display true

$ python3 square_cli.py -s "1 2 3 4 3" -r "[3x2]*500" -ia ./grass.png -a true -dp
```

```
usage: square_cli.py [-h] [-s SQUARE_LIST] [-r RECT_LIST] [-f CANVAS_SIZE] [-a ARRAY_DISPLAY] [-p PLOT_DISPLAY]
                     [-i0 IMAGE_ZERO] [-ia IMAGE_AVERAGE] [-ir IMAGE_ROTATE] [-o OUTPUT_FILE] [-ar RECT_MAX_SIDE]
                     [-as SQUARE_MAX_SIDE] [-ic INPUT_CSV] [-oc OUTPUT_CSV] [-ox OUTPUT_XLSX] [-dp] [-dpp] [-dr]

optional arguments:
  -h, --help            show this help message and exit
  -s SQUARE_LIST, --square_list SQUARE_LIST
                        Specify square radius list to populate.
  -r RECT_LIST, --rect_list RECT_LIST
                        Specify rectangles ( ex. '[1x3]*3, [4x3]*2' ) list to populate.
  -f CANVAS_SIZE, --fill_canvas_size CANVAS_SIZE
                        Specify canvas size to fill supllied square_list with.
  -a ARRAY_DISPLAY, --array_display ARRAY_DISPLAY
                        Show numpy array structure after computation completes.
  -p PLOT_DISPLAY, --plot_display PLOT_DISPLAY
                        Display plotly plot in browser. Overrides array display.
  -i0 IMAGE_ZERO, --input_image_zero IMAGE_ZERO
                        Input based on image parsing, where pure white is a placable 'tile', and any other color is blocked. Overrides canvas_size.
  -ia IMAGE_AVERAGE, --input_image_average IMAGE_AVERAGE
                        Input based on image parsing, images averaged into 0s and 1s and used to fill 'tiles'. Overrides canvas_size, and input_image_zero
  -ir IMAGE_ROTATE, --image_rotate IMAGE_ROTATE
                        Rotates provided image by specified degrees, if present, before population.
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Send output to specified filepath.Image type inferred by extension type.Overrides array display and plot display.
  -ar RECT_MAX_SIDE, --autopopulate_rectangles_max_side RECT_MAX_SIDE
                        Specify autopopulation of remaining canvas with rectangles starting with maximum sides supplied. Overrides square population using -as argument.
  -as SQUARE_MAX_SIDE, --autopopulate_squares_max_side SQUARE_MAX_SIDE
                        Specify autopopulation of remaining canvas with squares starting with maximum sides supplied.
  -ic INPUT_CSV, --input_csv INPUT_CSV
                        Specify csv to use with length, and width columns. Others will be treated as extra payload.
  -oc OUTPUT_CSV, --output_csv OUTPUT_CSV
                        Specify csv to populate with the specified information about plot.
  -ox OUTPUT_XLSX, --output_xlsx OUTPUT_XLSX
                        Specify xlsx to populate with the specified information about plot.
  -dp, --display_points
                        Toggle display of center point values in ouput.
  -dpp, --display_path_points
                        Toggle display of element addition path.
  -dr, --disallow_rotation
                        toggle to dissallow rotation of rectangles when adding to SquareCanvas.
```


Todo:
- [x] command line interface
- [x] rewrite in other languages
- [x] custom shape inputs (CustomCanvas) (-1 fill blank) and all check in bounds for zero
- [x] color individual squares
- [x] split classes and functions as needed
- [x] assumed structure from numpy array/matrix 
- [x] sorting square input
- [x] rectangle input
- [x] rotatable property, rotate function (Rect-specific)
- [x] CLI based preview of output
- [x] auto-populate (min_start) (py-cli)
- [x] PyScript web POC
- [x] CSV and image file input/output
- [ ] polish above implementations
- [ ] (pixel) circle packing
- [ ] verbose population of squares (debug)

---

Developed using python v3.9.13

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Required Libraries:
- Pandas 
- Numpy
- Plotly
- PIL (pillow) (for image input)
- kaliedo (static file export from plotly calls)

Note: PyScript HTML code are independent and loaded on their own at page load.

---

R version:

![R](https://img.shields.io/badge/r-%23276DC3.svg?style=for-the-badge&logo=r&logoColor=white) 
- Currently only supporting squares
- Less feature-rich than python implementation