from calibration import (
    create_homography,
    trajectory_to_world
)

from physics_engine import (
    physics_cross_check_calibrated,
    estimate_drop_height
)


# --------------------------------------------------
# Calibration setup
# --------------------------------------------------

# Example image coordinates
# representing a 2 m x 1 m floor rectangle.

image_points = [
    [100, 100],
    [500, 100],
    [500, 300],
    [100, 300]
]


# Corresponding real-world coordinates in metres.

world_points = [
    [0, 0],
    [2, 0],
    [2, 1],
    [0, 1]
]


# Create homography

homography = create_homography(
    image_points,
    world_points
)


# --------------------------------------------------
# Pixel trajectory
# --------------------------------------------------

trajectory = [
    {"t": 0.0, "x": 100, "y": 100},
    {"t": 0.1, "x": 200, "y": 150},
    {"t": 0.2, "x": 300, "y": 200},
    {"t": 0.3, "x": 400, "y": 250}
]


# --------------------------------------------------
# Convert pixels → metres
# --------------------------------------------------

world_trajectory = trajectory_to_world(
    trajectory,
    homography
)


# --------------------------------------------------
# Run calibrated physics
# --------------------------------------------------

result = physics_cross_check_calibrated(
    world_trajectory
)


# --------------------------------------------------
# Estimate vertical drop / movement
# --------------------------------------------------

drop_height = estimate_drop_height(
    world_trajectory
)

# --------------------------------------------------
# Display results
# --------------------------------------------------

print()
print("================================")
print("   CALIBRATED PHYSICS TEST")
print("================================")

print()

print("World trajectory:")
print(world_trajectory)

print()

print(
    "Peak velocity:",
    result["peak_velocity_m_s"],
    "m/s"
)

print(
    "Peak downward velocity:",
    result["peak_downward_velocity_m_s"],
    "m/s"
)

print(
    "Peak acceleration:",
    result["peak_acceleration_m_s2"],
    "m/s²"
)

print(
    "Estimated vertical drop:",
    drop_height,
    "m"
)
print()

print("Velocity sequence:")
print(result["velocity"])

print()

print("Vertical velocity sequence:")
print(result["vertical_velocity"])

print()

print("Acceleration sequence:")
print(result["acceleration"])

print()