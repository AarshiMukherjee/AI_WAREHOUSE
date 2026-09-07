import numpy as np

def calculate_velocity(trajectory):
    """
    Calculate velocity and vertical velocity from an object trajectory.

    trajectory format:
    [
        {"t": 0.0, "x": 420, "y": 180},
        {"t": 0.1, "x": 423, "y": 195},
        {"t": 0.2, "x": 427, "y": 220},
        ...
    ]

    t = time in seconds
    x = x-coordinate in pixels
    y = y-coordinate in pixels

    Note:
    Coordinates are currently in pixels.
    Physical calibration will be added later.
    """

    if len(trajectory) < 3:
        raise ValueError(
            "At least 3 trajectory points are required."
        )

    times = np.array(
        [point["t"] for point in trajectory],
        dtype=float
    )

    x = np.array(
        [point["x"] for point in trajectory],
        dtype=float
    )

    y = np.array(
        [point["y"] for point in trajectory],
        dtype=float
    )

    # Time difference between consecutive points
    dt = np.diff(times)

    if np.any(dt <= 0):
        raise ValueError(
            "Timestamps must be strictly increasing."
        )

    # Position changes
    dx = np.diff(x)
    dy = np.diff(y)

    # Distance travelled between consecutive points
    distance = np.sqrt(dx**2 + dy**2)

    # Overall velocity / speed
    velocity = distance / dt

    # Vertical velocity
    # In image coordinates, increasing y means downward.
    vertical_velocity = dy / dt

    return velocity, vertical_velocity, dt


def calculate_acceleration(velocity, dt):
    """
    Calculate acceleration from velocity.
    """

    if len(velocity) < 2:
        return np.array([])

    acceleration = np.diff(velocity) / dt[1:]

    return acceleration


def physics_cross_check(trajectory):
    """
    Perform the physics cross-check on an object trajectory.

    Returns:
        - peak velocity
        - peak downward velocity
        - peak acceleration
        - impact detection
        - physics confirmation
        - physics severity
    """

    # Calculate velocity
    

    velocity, vertical_velocity, dt = calculate_velocity(
        trajectory
    )

    # Calculate acceleration

    acceleration = calculate_acceleration(
        velocity,
        dt
    )

    # Peak measurements
 

    peak_velocity = float(
        np.max(velocity)
    )

    peak_downward_velocity = float(
        np.max(vertical_velocity)
    )

    if len(acceleration) > 0:
        peak_acceleration = float(
            np.max(np.abs(acceleration))
        )
    else:
        peak_acceleration = 0.0

    # Impact detection
 

    # Prototype threshold.
    # This will be calibrated using real
    # warehouse footage later.

    IMPACT_THRESHOLD = 1000.0

    impact_detected = (
        peak_acceleration >= IMPACT_THRESHOLD
    )

    # Drop-like motion detection
   

    # Prototype threshold for fast
    # downward movement.

    DROP_VELOCITY_THRESHOLD = 200.0

    rapid_downward_motion = (
        peak_downward_velocity
        >= DROP_VELOCITY_THRESHOLD
    )

    # Physics confirms a drop-like event
    # only when both downward motion
    # and impact evidence are present.

    physics_confirmed = (
        rapid_downward_motion
        and impact_detected
    )

    # Physics severity
 

    # Normalize velocity to 0-1.
    velocity_score = min(
        peak_downward_velocity / 600.0,
        1.0
    )

    # Normalize acceleration to 0-1.
    acceleration_score = min(
        peak_acceleration / 3000.0,
        1.0
    )

    # Weighted physics severity.
    physics_severity = (
        0.5 * velocity_score
        + 0.5 * acceleration_score
    )

    # Return results
  

    return {
        "peak_velocity_px_s": round(
            peak_velocity,
            2
        ),

        "peak_downward_velocity_px_s": round(
            peak_downward_velocity,
            2
        ),

        "peak_acceleration_px_s2": round(
            peak_acceleration,
            2
        ),

        "impact_detected": bool(
            impact_detected
        ),

        "physics_confirmed": bool(
            physics_confirmed
        ),

        "physics_severity": round(
            float(physics_severity),
            2
        ),

        "velocity": [
            round(float(v), 2)
            for v in velocity
        ],

        "vertical_velocity": [
            round(float(v), 2)
            for v in vertical_velocity
        ],

        "acceleration": [
            round(float(a), 2)
            for a in acceleration
        ]
    }