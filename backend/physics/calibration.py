import cv2
import numpy as np


def create_homography(image_points, world_points):
    """
    Create a homography matrix that maps image coordinates
    to real-world floor coordinates.

    image_points:
        Pixel coordinates from the camera image.

    world_points:
        Corresponding real-world coordinates in metres.

    Both must contain at least 4 corresponding points.
    """

    image_points = np.array(
        image_points,
        dtype=np.float32
    )

    world_points = np.array(
        world_points,
        dtype=np.float32
    )

    if len(image_points) < 4:
        raise ValueError(
            "At least 4 calibration points are required."
        )

    if len(image_points) != len(world_points):
        raise ValueError(
            "Image points and world points must have "
            "the same number of points."
        )

    homography, _ = cv2.findHomography(
        image_points,
        world_points
    )

    if homography is None:
        raise ValueError(
            "Could not calculate homography."
        )

    return homography


def pixel_to_world(x, y, homography):
    """
    Convert one image pixel coordinate into a
    real-world floor coordinate.
    """

    point = np.array(
        [[[x, y]]],
        dtype=np.float32
    )

    world_point = cv2.perspectiveTransform(
        point,
        homography
    )

    world_x = float(world_point[0][0][0])
    world_y = float(world_point[0][0][1])

    return world_x, world_y


def trajectory_to_world(trajectory, homography):
    """
    Convert a complete pixel trajectory into
    real-world floor coordinates.

    Input format:
        [
            {"t": 0.0, "x": 420, "y": 180},
            {"t": 0.1, "x": 423, "y": 195}
        ]

    Output format:
        [
            {"t": 0.0, "x": ..., "y": ...},
            {"t": 0.1, "x": ..., "y": ...}
        ]
    """

    world_trajectory = []

    for point in trajectory:

        world_x, world_y = pixel_to_world(
            point["x"],
            point["y"],
            homography
        )

        world_trajectory.append(
            {
                "t": point["t"],
                "x": round(world_x, 4),
                "y": round(world_y, 4)
            }
        )

    return world_trajectory