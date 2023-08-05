import numpy as np
from numba import njit
import numba


@njit
def calcDisoriCubic(quatSym1, quatSym2, numEqt=24):
    """
    :param quatSym1: symmetrically equivalent of input quaternion, has default shape in (4, 24) of cubic crystal
    :param quatSym2: symmetrically equivalent of input quaternion, has default shape in (4, 24) of cubic crystal
    :param numEqt: number of symmetrically equivalents of one input quaternion, default value is 24 for cubic crystal
    :return:
    angle: disorientation, the minimum misorientation angle between two input quaternions
    """

    angle = 0
    for i in range(numEqt):
        for j in range(numEqt):
            tempA = quatSym1[:, i]
            tempB = quatSym2[:, j]
            ta = moriTimes(tempA, tempB)

            if i + j == 0:
                angle = ta
            else:
                if angle < ta:
                    pass
                else:
                    angle = ta
            j += 1
        i += 1

    for i in range(numEqt):
        for j in range(numEqt):
            tempB = quatSym1[:, i]
            tempA = quatSym2[:, j]
            ta = moriTimes(tempA, tempB)

            if angle < ta:
                pass
            else:
                angle = ta
            j += 1
        i += 1

    return angle


@njit
def symmetriesCubic(_q):
    """
    :param _q: input quaternion, inQuat has default shape in (4, )
    :return:
    quatSym: symmetrically equivalent of input quaternion
    """

    _q = _q.reshape(4, )

    q0 = _q[0]
    q1 = _q[1]
    q2 = _q[2]
    q3 = _q[3]

    quatSym = np.ones((4, 24), dtype=numba.float64)
    quatSym[:, 0] = np.array([q0, q1, q2, q3])
    quatSym[:, 1] = np.array([q3, q2, -q1, -q0])
    quatSym[:, 2] = np.array([-q2, q3, q0, -q1])
    quatSym[:, 3] = np.array([q1, -q0, q3, -q2])
    quatSym[:, 4] = np.array(
        [(q0 + q3 + q1 - q2) / 2, (q1 + q3 + q2 - q0) / 2, (q2 + q3 + q0 - q1) / 2, (q3 - q0 - q1 - q2) / 2])
    quatSym[:, 5] = np.array(
        [(q0 - q3 - q1 + q2) / 2, (q1 - q3 - q2 + q0) / 2, (q2 - q3 - q0 + q1) / 2, (q3 + q0 + q1 + q2) / 2])
    quatSym[:, 6] = np.array(
        [(q0 - q3 + q1 - q2) / 2, (q1 + q3 - q2 - q0) / 2, (q2 + q3 + q0 + q1) / 2, (q3 + q0 - q1 - q2) / 2])
    quatSym[:, 7] = np.array(
        [(q0 + q3 - q1 + q2) / 2, (q1 - q3 + q2 + q0) / 2, (q2 - q3 - q0 - q1) / 2, (q3 - q0 + q1 + q2) / 2])
    quatSym[:, 8] = np.array(
        [(q0 + q3 + q1 + q2) / 2, (q1 - q3 + q2 - q0) / 2, (q2 + q3 - q0 - q1) / 2, (q3 - q0 + q1 - q2) / 2])
    quatSym[:, 9] = np.array(
        [(q0 - q3 - q1 - q2) / 2, (q1 + q3 - q2 + q0) / 2, (q2 - q3 + q0 + q1) / 2, (q3 + q0 - q1 + q2) / 2])
    quatSym[:, 10] = np.array(
        [(q0 + q3 - q1 - q2) / 2, (q1 + q3 + q2 + q0) / 2, (q2 - q3 + q0 - q1) / 2, (q3 - q0 - q1 + q2) / 2])
    quatSym[:, 11] = np.array(
        [(q0 - q3 + q1 + q2) / 2, (q1 - q3 - q2 - q0) / 2, (q2 + q3 - q0 + q1) / 2, (q3 + q0 + q1 - q2) / 2])
    quatSym[:, 12] = np.array(
        [(q1 - q2) / np.sqrt(2), (q3 - q0) / np.sqrt(2), (q3 + q0) / np.sqrt(2), (-q1 - q2) / np.sqrt(2)])
    quatSym[:, 13] = np.array(
        [(q3 + q1) / np.sqrt(2), (q2 - q0) / np.sqrt(2), (q3 - q1) / np.sqrt(2), (-q0 - q2) / np.sqrt(2)])
    quatSym[:, 14] = np.array(
        [(q3 - q2) / np.sqrt(2), (q3 + q2) / np.sqrt(2), (q0 - q1) / np.sqrt(2), (-q0 - q1) / np.sqrt(2)])
    quatSym[:, 15] = np.array(
        [(-q1 - q2) / np.sqrt(2), (q3 + q0) / np.sqrt(2), (-q3 + q0) / np.sqrt(2), (-q1 + q2) / np.sqrt(2)])
    quatSym[:, 16] = np.array(
        [(q3 - q1) / np.sqrt(2), (q2 + q0) / np.sqrt(2), (-q3 - q1) / np.sqrt(2), (-q0 + q2) / np.sqrt(2)])
    quatSym[:, 17] = np.array(
        [(q3 + q2) / np.sqrt(2), (-q3 + q2) / np.sqrt(2), (-q0 - q1) / np.sqrt(2), (-q0 + q1) / np.sqrt(2)])
    quatSym[:, 18] = np.array(
        [(q0 + q3) / np.sqrt(2), (q1 + q2) / np.sqrt(2), (q2 - q1) / np.sqrt(2), (q3 - q0) / np.sqrt(2)])
    quatSym[:, 19] = np.array(
        [(q0 - q2) / np.sqrt(2), (q1 + q3) / np.sqrt(2), (q2 + q0) / np.sqrt(2), (q3 - q1) / np.sqrt(2)])
    quatSym[:, 20] = np.array(
        [(q0 + q1) / np.sqrt(2), (q1 - q0) / np.sqrt(2), (q2 + q3) / np.sqrt(2), (q3 - q2) / np.sqrt(2)])
    quatSym[:, 21] = np.array(
        [(q0 - q3) / np.sqrt(2), (q1 - q2) / np.sqrt(2), (q2 + q1) / np.sqrt(2), (q3 + q0) / np.sqrt(2)])
    quatSym[:, 22] = np.array(
        [(q0 + q2) / np.sqrt(2), (q1 - q3) / np.sqrt(2), (q2 - q0) / np.sqrt(2), (q3 + q1) / np.sqrt(2)])
    quatSym[:, 23] = np.array(
        [(q0 - q1) / np.sqrt(2), (q1 + q0) / np.sqrt(2), (q2 - q3) / np.sqrt(2), (q3 + q2) / np.sqrt(2)])

    return quatSym


@njit
def moriTimes(inQuat1, inQuat2):
    """

    :param inQuat1: as q1
    :param inQuat2: as q2
    :return:
    angle: the misorientation angle between q1 and q2
    quatProductMori: this variable has been modified to calculate q2 * q1^-1
    """
    a1 = inQuat2[0]
    b1 = inQuat2[1]
    c1 = inQuat2[2]
    d1 = inQuat2[3]
    a2 = inQuat1[0]
    b2 = -inQuat1[1]
    c2 = -inQuat1[2]
    d2 = -inQuat1[3]

    quatProdcutMori = np.ones((1, 4), dtype=numba.float64)

    quatProdcutMori[0, 0] = a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2
    quatProdcutMori[0, 1] = b1 * a2 + a1 * b2 - d1 * c2 + c1 * d2
    quatProdcutMori[0, 2] = c1 * a2 + d1 * b2 + a1 * c2 - b1 * d2
    quatProdcutMori[0, 3] = d1 * a2 - c1 * b2 + b1 * c2 + a1 * d2

    quatProdcutMori = quatProdcutMori.reshape(4, )

    if quatProdcutMori[0] < 0:
        quatProdcutMori = -1 * quatProdcutMori
    else:
        pass

    q0 = quatProdcutMori[0]

    if np.abs(q0 - 1) < 1e-3:
        angle = 0
    elif np.abs(q0) < 1e-8:
        angle = np.pi
    else:
        angle = 2 * np.arccos(q0)

    angle = angle * 180 / np.pi

    return angle
