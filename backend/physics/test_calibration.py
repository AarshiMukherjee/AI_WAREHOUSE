from calibration import (
    create_homography,
    pixel_to_world,
    trajectory_to_world
)


# --------------------------------------------------
# Calibration points
# --------------------------------------------------

# Points selected from the camera image.
# These are example pixel coordinates.

image_points = [
    [100, 100],
    [500, 100],
    [500, 300],
    [100, 300]
]


# Corresponding real-world floor coordinates.
# Rectangle = 2 metres x 1 metre.

world_points = [
    [0, 0],
    [2, 0],
    [2, 1],
    [0, 1]
]


# --------------------------------------------------
# Create homography
# --------------------------------------------------

homography = create_homography(
    image_points,
    world_points
)


# --------------------------------------------------
# Test one pixel point
# --------------------------------------------------

world_x, world_y = pixel_to_world(
    300,
    200,
    homography
)


print()
print("================================")
print("       CALIBRATION TEST")
print("================================")
print()

print("Pixel point:")
print("(300, 200)")

print()

print("World point:")
print(
    round(world_x, 3),
    "m,",
    round(world_y, 3),
    "m"
)


# --------------------------------------------------
# Test trajectory conversion
# --------------------------------------------------

trajectory = [
    {"t": 0.0, "x": 100, "y": 100},
    {"t": 0.1, "x": 200, "y": 150},
    {"t": 0.2, "x": 300, "y": 200},
    {"t": 0.3, "x": 400, "y": 250}
]


world_trajectory = trajectory_to_world(
    trajectory,
    homography
)


print()
print("World trajectory:")
print(world_trajectory)

print()