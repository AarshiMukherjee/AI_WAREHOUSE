import numpy as np


def calculate_velocity(trajectory):
    """
    Calculate velocity and vertical velocity from an object trajectory.

    trajectory format:
    [
        {"t": 0.0, "x": 420, "y": 180},
        {"t": 0.1, "x": 423, "y": 195},
        {"t": 0.2, "x": 427, "y": 220}
    ]

    t = time in seconds
    x = x-coordinate
    y = y-coordinate

    Coordinates are assumed to be in pixels.
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

    dt = np.diff(times)

    if np.any(dt <= 0):
        raise ValueError(
            "Timestamps must be strictly increasing."
        )

    dx = np.diff(x)
    dy = np.diff(y)

    distance = np.sqrt(
        dx**2 + dy**2
    )

    velocity = distance / dt

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
    Original pixel-based physics cross-check.

    This version is kept for backward compatibility
    with the original Version 1 test.
    """

    velocity, vertical_velocity, dt = calculate_velocity(
        trajectory
    )

    acceleration = calculate_acceleration(
        velocity,
        dt
    )

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

    # Original pixel-based prototype threshold.
    IMPACT_THRESHOLD = 1000.0

    impact_detected = (
        peak_acceleration >= IMPACT_THRESHOLD
    )

    DROP_VELOCITY_THRESHOLD = 200.0

    rapid_downward_motion = (
        peak_downward_velocity
        >= DROP_VELOCITY_THRESHOLD
    )

    physics_confirmed = (
        rapid_downward_motion
        and impact_detected
    )

    velocity_score = min(
        peak_downward_velocity / 600.0,
        1.0
    )

    acceleration_score = min(
        peak_acceleration / 3000.0,
        1.0
    )

    physics_severity = (
        0.5 * velocity_score
        + 0.5 * acceleration_score
    )

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


def physics_cross_check_calibrated(trajectory):
    """
    Perform the physics cross-check on a trajectory
    that has already been converted to metres.

    Input:
    [
        {"t": 0.0, "x": 0.0, "y": 0.0},
        {"t": 0.1, "x": 0.2, "y": 0.1},
        ...
    ]

    t = seconds
    x = metres
    y = metres

    Returns:
        - peak velocity
        - peak downward velocity
        - peak acceleration
        - impact detection
        - physics confirmation
        - physics severity
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

    dt = np.diff(times)

    if np.any(dt <= 0):
        raise ValueError(
            "Timestamps must be strictly increasing."
        )

    dx = np.diff(x)
    dy = np.diff(y)

    distance = np.sqrt(
        dx**2 + dy**2
    )

    # Velocity in m/s
    velocity = distance / dt

    # Vertical velocity in m/s
    # Positive y means downward.
    vertical_velocity = dy / dt

    # Acceleration in m/s²
    acceleration = calculate_acceleration(
        velocity,
        dt
    )

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

    # --------------------------------------------------
    # Impact detection
    # --------------------------------------------------

    # An impact is treated as:
    # significant downward motion
    # followed by sudden deceleration.

    IMPACT_ACCELERATION_THRESHOLD = 15.0
    DOWNWARD_VELOCITY_FOR_IMPACT = 1.5

    impact_detected = False

    if len(acceleration) > 0:

        for i in range(len(acceleration)):

            # Strong negative acceleration means
            # the object suddenly slowed down.

            sudden_deceleration = (
                acceleration[i]
                <= -IMPACT_ACCELERATION_THRESHOLD
            )

            # Downward velocity before the
            # deceleration event.

            downward_motion = False

            if i < len(vertical_velocity):
                downward_motion = (
                    vertical_velocity[i]
                    >= DOWNWARD_VELOCITY_FOR_IMPACT
                )

            if sudden_deceleration and downward_motion:
                impact_detected = True
                break

    # --------------------------------------------------
    # Rapid downward motion
    # --------------------------------------------------

    DROP_VELOCITY_THRESHOLD = 2.0

    rapid_downward_motion = (
        peak_downward_velocity
        >= DROP_VELOCITY_THRESHOLD
    )

    # --------------------------------------------------
    # Physics confirmation
    # --------------------------------------------------

    physics_confirmed = (
        rapid_downward_motion
        and impact_detected
    )

    # --------------------------------------------------
    # Physics severity
    # --------------------------------------------------

    velocity_score = min(
        peak_downward_velocity / 6.0,
        1.0
    )

    acceleration_score = min(
        peak_acceleration / 30.0,
        1.0
    )

    physics_severity = (
        0.5 * velocity_score
        + 0.5 * acceleration_score
    )

    return {
        "peak_velocity_m_s": round(
            peak_velocity,
            3
        ),

        "peak_downward_velocity_m_s": round(
            peak_downward_velocity,
            3
        ),

        "peak_acceleration_m_s2": round(
            peak_acceleration,
            3
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
            round(float(v), 3)
            for v in velocity
        ],

        "vertical_velocity": [
            round(float(v), 3)
            for v in vertical_velocity
        ],

        "acceleration": [
            round(float(a), 3)
            for a in acceleration
        ]
    }


def estimate_drop_height(trajectory):
    """
    Estimate vertical displacement of an object.

    The trajectory must already be calibrated into metres.

    This is an approximate vertical displacement,
    not full 3D height reconstruction.
    """

    if len(trajectory) < 2:
        raise ValueError(
            "At least 2 trajectory points are required."
        )

    y = np.array(
        [point["y"] for point in trajectory],
        dtype=float
    )

    # Increasing y represents downward movement.

    highest_point = np.min(y)
    lowest_point = np.max(y)

    drop_height = (
        lowest_point - highest_point
    )

    return round(
        float(drop_height),
        3
    )