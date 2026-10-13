import numpy as np


def project_point(point, W, H, fx, fy, ox, oy, n, f):
    if W <= 0 or H <= 0 or not 0 < n < f:
        raise ValueError("Require W, H > 0 and 0 < n < f.")

    P = np.array([
        [2 * fx / W, 0, 1 - 2 * ox / W, 0],
        [0, 2 * fy / H, 1 - 2 * oy / H, 0],
        [0, 0, -(f + n) / (f - n), -2 * f * n / (f - n)],
        [0, 0, -1, 0]
    ])

    point = np.asarray(point, dtype=float)
    if point.shape == (3,):
        point = np.append(point, 1.0)
    elif point.shape != (4,):
        raise ValueError("Provide 3 or 4 point coordinates.")

    clip = P @ point

    if clip[3] == 0:
        raise ValueError("Perspective division is undefined at z = 0.")

    ndc = clip[:3] / clip[3]

    u = 0.5 * (ndc[0] + 1) * W
    v = 0.5 * (ndc[1] + 1) * H

    return P, clip, ndc, (u, v)


if __name__ == "__main__":
    P, clip, ndc, pixels = project_point(
        point=(0.3, -0.15, -6.0, 1),
        W=800, H=600,
        fx=800, fy=800,
        ox=400, oy=400,
        n=0.2, f=20
    )

    print("Projection matrix:\n", P)
    print("Clip coordinates:", clip)
    print("NDC:", ndc)
    print("Pixel coordinates:", pixels)