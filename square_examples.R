source("rSquares.R")

s1 <- square$new(side = 3)
message <- glue(
    "first point x-value {s1$coordinates$p1$x}\n",
    "square side: {s1$side}\n",
    "square area: {s1$area}\n",
    "square center x-value: {s1$center$x}\n"
)
print(message)


s1$add_x(x0 = 2)$add_xy(x0 = 1, y0 = 2)
print(glue("Moved squared (+x2) (+x1, +y2) points:\n"))
print(s1)
print(s1$coordinates, sep = "")


a_square <- square_canvas$new(contents = c(square$new(6), square$new(4)))

b_square  <- square_canvas$new(
    contents = sapply(
      c(
        c(1, 2, 3, 4, 4, 3, 3, 3, 2, 1, 2, 3, 1),
        rep(c(1), 8)
      ), square$new)
  )

print(a_square$frame)
print(a_square$generate_ggplot())

print(b_square$frame)
print(b_square$generate_ggplot())


c_square <- square_canvas$new(
  contents = mapply(
    rectangle$new,
    c(1, 2, 3, 4, 5),
    c(2, 4, 3, 1, 3)
  ),
  max_bound = 14
)

print(c_square$frame)
print(c_square$generate_ggplot())