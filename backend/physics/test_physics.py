from physics_engine import physics_cross_check


# Simulated product drop trajectory

trajectory = [
    {"t": 0.0, "x": 420, "y": 180},
    {"t": 0.1, "x": 422, "y": 185},
    {"t": 0.2, "x": 424, "y": 200},
    {"t": 0.3, "x": 426, "y": 230},
    {"t": 0.4, "x": 428, "y": 275},
    {"t": 0.5, "x": 430, "y": 330},

    # Product reaches the floor
    # and suddenly stops.
    {"t": 0.6, "x": 431, "y": 335},
    {"t": 0.7, "x": 431, "y": 336}
]


# Run physics cross-check


result = physics_cross_check(trajectory)


# Display results


print()
print("================================")
print("       PHYSICS CROSS-CHECK")
print("================================")

print()

print(
    "Peak velocity:",
    result["peak_velocity_px_s"],
    "px/s"
)

print(
    "Peak downward velocity:",
    result["peak_downward_velocity_px_s"],
    "px/s"
)

print(
    "Peak acceleration:",
    result["peak_acceleration_px_s2"],
    "px/s²"
)

print(
    "Impact detected:",
    result["impact_detected"]
)

print(
    "Physics confirmed:",
    result["physics_confirmed"]
)

print(
    "Physics severity:",
    result["physics_severity"]
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