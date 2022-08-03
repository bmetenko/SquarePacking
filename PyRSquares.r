library("reticulate")
use_virtualenv("../")
squares_lib <- import("squares")

list_square_radii_1 <- c(3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1)
list_squares_1 <- lapply(list_square_radii_1, squares_lib$Square)

B <- squares_lib$SquareCanvas(max_bound = 8L, contents = list_squares_1)

B$contents_frame()

B$generate_plotly(render = "browser")