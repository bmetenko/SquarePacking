# Simple OOP based square packing implementation
[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=logo=Jupyter)](https://jupyter.org/try)
 [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) ![Project_Type](https://img.shields.io/badge/project%20type-toy-blue)

Simple OOP (class-based) implementation of packing Square instances into a SquareCanvas.

Main functionality of the code exemplified in the pySquares.ipynb. 

Maintenance or updates unclear since only a toy project.
Rotation property currently WIP.

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
- [ ] polish above implementations
- [ ] (pixel) circle packing
- [ ] autopopulate (min_start)

---

Developed using python v3.9.13

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

Required Libraries:
- Pandas 
- Numpy
- Plotly
- PIL (pillow) (for image input)
- kaliedo (static file export from plotly calls)

CLI version:
- Currently only supporting square canvas filling minimal example.
---

R version:

![R](https://img.shields.io/badge/r-%23276DC3.svg?style=for-the-badge&logo=r&logoColor=white) 
- Currently only supporting squares