"""
Euler angles are in Bunge convention, i.e. ZXZ rotation
"""
import sys
import numpy as np

P = -1
"""
Define permutation index to make conversion internally consistent
Reference DOI: 10.1088/0965-0393/23/8/083501
"""


class rotations(object):

    def __init__(self):
        pass

    @staticmethod
    def mat2quat(_rm):
        """
        Implementing Cayley's method
        Reference DOI: 10.1115/1.4041889
        """
        # ----- Check numpy data type -----
        if not type(_rm) is np.ndarray:
            _rm = np.array(_rm)
        # ---------------------------------
        _q = np.zeros(4)

        _q[0] = (1 / 4) * np.sqrt((_rm[0, 0] + _rm[1, 1] + _rm[2, 2] + 1) ** 2 +
                                  (_rm[2, 1] - _rm[1, 2]) ** 2 +
                                  (_rm[0, 2] - _rm[2, 0]) ** 2 +
                                  (_rm[1, 0] - _rm[0, 1]) ** 2)

        _q[1] = P * np.sign(_rm[2, 1] - _rm[1, 2]) * (1 / 4) * np.sqrt((_rm[2, 1] - _rm[1, 2]) ** 2 +
                                                                       (_rm[0, 0] - _rm[1, 1] - _rm[2, 2] + 1) ** 2 +
                                                                       (_rm[1, 0] + _rm[0, 1]) ** 2 +
                                                                       (_rm[2, 0] + _rm[0, 2]) ** 2)
        _q[2] = P * np.sign(_rm[0, 2] - _rm[2, 0]) * (1 / 4) * np.sqrt((_rm[0, 2] - _rm[2, 0]) ** 2 +
                                                                       (_rm[1, 0] + _rm[0, 1]) ** 2 +
                                                                       (_rm[1, 1] - _rm[0, 0] - _rm[2, 2] + 1) ** 2 +
                                                                       (_rm[2, 1] + _rm[1, 2]) ** 2)
        _q[3] = P * np.sign(_rm[1, 0] - _rm[0, 1]) * (1 / 4) * np.sqrt((_rm[1, 0] - _rm[0, 1]) ** 2 +
                                                                       (_rm[2, 0] + _rm[0, 2]) ** 2 +
                                                                       (_rm[2, 1] + _rm[1, 2]) ** 2 +
                                                                       (_rm[2, 2] - _rm[0, 0] - _rm[1, 1] + 1) ** 2)

        return _q

    @staticmethod
    def mat2quat_bi(_rm):
        """
        Implementing Bar-Itzhack algorithm
        If rotation matrix is not orthogonal, use this method
        Reference DOI: 10.2514/2.4654
        """

        # ----- Check numpy data type -----
        if not type(_rm) is np.ndarray:
            _rm = np.array(_rm)
        # ---------------------------------

        _k = np.zeros([4, 4])

        _k[0, 0] = 1 / 3 * (_rm[0, 0] - _rm[1, 1] - _rm[2, 2])
        _k[1, 0] = 1 / 3 * (_rm[1, 0] + _rm[0, 1])
        _k[2, 0] = 1 / 3 * (_rm[2, 0] + _rm[0, 2])
        _k[3, 0] = 1 / 3 * (_rm[1, 2] - _rm[2, 1])

        _k[0, 1] = 1 / 3 * (_rm[1, 0] + _rm[0, 1])
        _k[1, 1] = 1 / 3 * (_rm[1, 1] - _rm[0, 0] - _rm[2, 2])
        _k[2, 1] = 1 / 3 * (_rm[2, 1] + _rm[1, 2])
        _k[3, 1] = 1 / 3 * (_rm[2, 0] - _rm[0, 2])

        _k[0, 2] = 1 / 3 * (_rm[2, 0] + _rm[0, 2])
        _k[1, 2] = 1 / 3 * (_rm[2, 1] + _rm[1, 2])
        _k[2, 2] = 1 / 3 * (_rm[2, 2] - _rm[0, 0] - _rm[1, 1])
        _k[3, 2] = 1 / 3 * (_rm[0, 1] - _rm[1, 0])

        _k[0, 3] = 1 / 3 * (_rm[1, 2] - _rm[2, 1])
        _k[1, 3] = 1 / 3 * (_rm[2, 0] - _rm[0, 2])
        _k[2, 3] = 1 / 3 * (_rm[0, 1] - _rm[1, 0])
        _k[3, 3] = 1 / 3 * (_rm[0, 0] + _rm[1, 1] + _rm[2, 2])

        eigen = np.linalg.eig(_k)
        _q = eigen[1][:, eigen[0].argmax()]
        _q = np.array([_q[3], _q[0], _q[1], _q[2]])

        # Introducing permutation index
        _q[1] = -P * _q[1]
        _q[2] = -P * _q[2]
        _q[3] = -P * _q[3]

        if _q[0] < 0:
            _q = -1 * _q
        else:
            pass

        return _q

    @staticmethod
    def mat2quat_cyclic(_rm):

        # No need to use permutation index
        _anx = rotations.mat2anx(_rm)
        _q = rotations.anx2quat(_anx)

        return _q

    @staticmethod
    def quat2mat(_q):

        # ----- Check numpy data type -----
        if not type(_q) is np.ndarray:
            _q = np.array(_q)
        # ---------------------------------
        _rm = np.zeros([3, 3])

        # Introducing permutation index

        _rm[0, 0] = 1 - 2 * (_q[2] ** 2 + _q[3] ** 2)
        _rm[1, 0] = 2 * (P * (_q[0] * _q[3]) + _q[1] * _q[2])
        _rm[2, 0] = 2 * (_q[1] * _q[3] - P * (_q[0] * _q[2]))

        _rm[0, 1] = 2 * (_q[1] * _q[2] - P * (_q[0] * _q[3]))
        _rm[1, 1] = 1 - 2 * (_q[1] ** 2 + _q[3] ** 2)
        _rm[2, 1] = 2 * (P * (_q[0] * _q[1]) + _q[2] * _q[3])

        _rm[0, 2] = 2 * (P * (_q[0] * _q[2]) + _q[1] * _q[3])
        _rm[1, 2] = 2 * (_q[2] * _q[3] - P * (_q[0] * _q[1]))
        _rm[2, 2] = 1 - 2 * (_q[1] ** 2 + _q[2] ** 2)

        return _rm

    @staticmethod
    def euler2quat(_ea):
        # ----- Check numpy data type -----
        if not type(_ea) is np.ndarray:
            _ea = np.array(_ea)
        # ---------------------------------
        _ea = np.deg2rad(_ea)

        _phi1 = _ea[0]
        _cphi = _ea[1]
        _phi2 = _ea[2]

        _q = np.zeros([4, ])

        _q[0] = np.cos(_cphi / 2) * np.cos((_phi1 + _phi2) / 2)
        _q[1] = -P * np.sin(_cphi / 2) * np.cos((_phi1 - _phi2) / 2)
        _q[2] = -P * np.sin(_cphi / 2) * np.sin((_phi1 - _phi2) / 2)
        _q[3] = -P * np.cos(_cphi / 2) * np.sin((_phi1 + _phi2) / 2)

        if _q[0] < 0:
            _q = -1 * _q
        else:
            pass

        return _q

    @staticmethod
    def quat2euler(_q):
        # ----- Check numpy data type -----
        if not type(_q) is np.ndarray:
            _q = np.array(_q)
        # ---------------------------------

        _ea = np.zeros([3, ])

        # Setting conditions
        q03 = _q[0] ** 2 + _q[3] ** 2
        q12 = _q[1] ** 2 + _q[2] ** 2
        chi = np.sqrt(q03 * q12)

        if chi < 1.0e-8:
            if q12 < 1.0e-8:
                _ea[0] = np.arctan2(-2 * P * _q[0] * _q[3], _q[0] ** 2 - _q[3] ** 2)
                _ea[1] = 0
                _ea[2] = 0
            if q03 < 1.0e-8:
                _ea[0] = np.arctan2(2 * _q[1] * _q[2], _q[1] ** 2 - _q[2] ** 2)
                _ea[1] = np.pi
                _ea[2] = 0
        else:
            _ea[0] = np.arctan2(_q[1] * _q[3] - P * (_q[0] * _q[2]),
                                -P * (_q[0] * _q[1]) - _q[2] * _q[3])
            _ea[1] = np.arctan2(2 * chi, q03 - q12)
            _ea[2] = np.arctan2(_q[1] * _q[3] + P * (_q[0] * _q[2]),
                                _q[2] * _q[3] - P * (_q[0] * _q[1]))

        for i in range(3):
            if _ea[i] < 0:
                _ea[i] += 2 * np.pi

        _ea = np.rad2deg(_ea)

        return _ea

    @staticmethod
    def euler2mat(_ea):
        # ----- Check numpy data type -----
        if not type(_ea) is np.ndarray:
            _ea = np.array(_ea)
        # ---------------------------------

        _ea = np.deg2rad(_ea)

        phi1 = _ea[0]
        cphi = _ea[1]
        phi2 = _ea[2]
        _rm = np.array([[np.cos(phi1) * np.cos(phi2) - np.sin(phi1) * np.sin(phi2) * np.cos(cphi),
                         np.sin(phi1) * np.cos(phi2) + np.cos(phi1) * np.sin(phi2) * np.cos(cphi),
                         np.sin(phi2) * np.sin(cphi)],
                        [-np.cos(phi1) * np.sin(phi2) - np.sin(phi1) * np.cos(phi2) * np.cos(cphi),
                         -np.sin(phi1) * np.sin(phi2) + np.cos(phi1) * np.cos(phi2) * np.cos(cphi),
                         np.cos(phi2) * np.sin(cphi)],
                        [np.sin(phi1) * np.sin(cphi), -np.cos(phi1) * np.sin(cphi), np.cos(cphi)]])

        return _rm

    @staticmethod
    def mat2euler(_rm):
        # ----- Check numpy data type -----
        if not type(_rm) is np.ndarray:
            _rm = np.array(_rm)
        # ---------------------------------

        _ea = np.zeros([3, ])
        if np.abs(np.abs(_rm[2, 2]) - 1) > 1e-8:
            _ea[0] = np.arctan2(_rm[2, 0], -_rm[2, 1])
            _ea[1] = np.arccos(_rm[2, 2])
            _ea[2] = np.arctan2(_rm[0, 2], _rm[1, 2])
        else:
            _ea[0] = np.arctan2(_rm[0, 1], _rm[0, 0])
            _ea[1] = (np.pi / 2) * (1 - _rm[2, 2])
            _ea[2] = 0

        if _ea[0] < 0:
            _ea[0] += 2 * np.pi
        if _ea[2] < 0:
            _ea[2] += 2 * np.pi

        _ea = np.rad2deg(_ea)

        # using different approach
        # quat = rot.mat2quat(R)
        # euler = rot.quat2euler(quat)

        return _ea

    @staticmethod
    def mat2anx(_rm):
        # ----- Check numpy data type -----
        if not type(_rm) is np.ndarray:
            _rm = np.array(_rm)
        # ---------------------------------
        _anx = np.zeros([4, ])
        omega = np.arccos((_rm[0, 0] + _rm[1, 1] + _rm[2, 2] - 1) / 2)
        # n = np.zeros([3, ])
        eigen = np.linalg.eig(_rm)
        idx = 0
        for i in range(3):
            if eigen[0][i].imag == 0:
                idx = i

        if omega > 1e-8:
            n = np.abs(eigen[1][:, idx].real)
            n[0] = n[0] * np.sign(P * (_rm[2, 1] - _rm[1, 2]))
            n[1] = n[1] * np.sign(P * (_rm[0, 2] - _rm[2, 0]))
            n[2] = n[2] * np.sign(P * (_rm[1, 0] - _rm[0, 1]))
            # n[0] = R[2, 1] - R[1, 2]
            # n[1] = R[0, 2] - R[2, 0]
            # n[2] = R[1, 0] - R[0, 1]
            # n = n / (2 * np.sin(omega))
        else:
            n = np.array([0, 0, 1])

        omega = np.rad2deg(omega)

        _anx[0] = omega
        _anx[1:4] = n

        return _anx

    @staticmethod
    def anx2quat(_anx):
        # ----- Check numpy data type -----
        if not type(_anx) is np.ndarray:
            _anx = np.array(_anx)
        # ---------------------------------

        omega = np.deg2rad(_anx[0])
        n = _anx[1:4]

        _q = np.zeros([4, ])

        _q[0] = np.cos(omega / 2)
        _q[1:4] = np.sin(omega / 2) * n

        if _q[0] < 0:
            quat = -1 * _q
        else:
            pass

        return _q

    @staticmethod
    def quat2anx(_q):
        # ----- Check numpy data type -----
        if not type(_q) is np.ndarray:
            _q = np.array(_q)
        # ---------------------------------

        if _q[0] < 0:
            _q = -1 * _q
        else:
            pass

        q0 = _q[0]
        q1 = _q[1]
        q2 = _q[2]
        q3 = _q[3]

        if np.abs(q0 - 1) < 1e-3:
            omega = 0
            n = np.array([0, 0, 1])
        elif np.abs(q0) < 1e-8:
            omega = np.pi
            n = np.array([q1, q2, q3])
        else:
            omega = 2 * np.arccos(q0)
            s = np.sign(q0) / np.sqrt(q1 ** 2 + q2 ** 2 + q3 ** 2)
            n = s * np.array([q1, q2, q3])

        omega = np.rad2deg(omega)

        _anx = np.zeros([4, ])
        _anx[0] = omega
        _anx[1:4] = n
        return _anx

    @staticmethod
    def randQuats(n=1):
        """
        Creating random quaternions uniformly
        Reference DOI: 10.1016/B978-0-08-050755-2.50036-1

        Generated quaternions are stored as column vectors
        """
        _q = np.zeros((4, n))
        for i in range(n):
            u = np.random.random()
            v = np.random.random()
            w = np.random.random()
            _q[0, i] = np.sqrt(1 - u) * np.sin(2 * np.pi * v)
            _q[1, i] = np.sqrt(1 - u) * np.cos(2 * np.pi * v)
            _q[2, i] = np.sqrt(u) * np.sin(2 * np.pi * w)
            _q[3, i] = np.sqrt(u) * np.cos(2 * np.pi * w)
        return _q


"""
Implementing algorithms to solve Wabha's problem:
a.k.a. Calculate rotation matrix R between two pairs of vectors (v1, u1), (v2, u2)
R @ v1 = v2; R @ u1 = u2
v1, u1 cannot be parallel and zero vectors
"""


def check_angle(v1, v2):
    """
    v1 is your firsr vector
    v2 is your second vector
    Inputs are column vectors
    """

    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    norm3 = np.linalg.norm(np.cross(v1, v2))
    try:
        if norm1 == 0:
            raise ValueError('First vector is zero')
        if norm2 == 0:
            raise ValueError('Second vector is zero')
        if norm3 == 0:
            raise ValueError('First and second vector are parallel')
        else:
            pass
            # print('Checking done!')
    except ValueError as e:
        print('ValueError:', e)
        sys.exit(1)

    # return None
    # angle = np.arccos((v1 @ v2) / (norm1 * norm2))
    # return angle


def normalized_vec3d(vec):
    vec_hat = vec / np.linalg.norm(vec, axis=0)
    return vec_hat


# ---------------------------------------------------------------------------------
# TRIAD ALGORITHM
def triad(vs1, vs2):
    """
    vs1 and vs2 are column vectors

    """
    # print('Checking angles between first vector pair...')
    check_angle(vs1[:, 0], vs2[:, 0])
    # print('Checking angles between second vector pair...')
    check_angle(vs1[:, 1], vs2[:, 1])

    a = normalized_vec3d(vs1)
    v = np.cross(a[:, 0], a[:, 1])
    v = v.reshape(3, 1)
    a = np.hstack((a, v))
    b = np.linalg.inv(a)

    a = normalized_vec3d(vs2)
    v = np.cross(a[:, 0], a[:, 1])
    v = v.reshape(3, 1)
    a = np.hstack((a, v))

    _rm = np.zeros((3, 3))
    for j in range(3):
        for i in range(3):
            for k in range(3):
                _rm[i, j] = _rm[i, j] + a[i, k] * b[k, j]
    return _rm


# ---------------------------------------------------------------------------------
# KABASCH ALGORITHM
def kabsch(P, Q):
    """
    Using the Kabsch algorithm with two sets of paired point P and Q, centered
    around the centroid. Each vector set is represented as an NxD
    matrix, where D is the the dimension of the space.
    The algorithm works in two steps:
    - the computation of a covariance matrix C
    - computation of the optimal rotation matrix U
    For more info see http://en.wikipedia.org/wiki/Kabsch_algorithm
    Parameters
    ----------
    P, Q are column vectors
    P : array
        (D,N) matrix, where D is dimension and N is points.
    Q : array
        (D,N) matrix, where D is dimension and N is points.
    Returns
    -------
    rot : matrix
        Rotation matrix (D,D)
    """
    print('Checking angles between first vector pair...')
    check_angle(P[:, 0], Q[:, 0])
    print('Checking angles between second vector pair...')
    check_angle(P[:, 1], Q[:, 1])

    # Computation of the covariance matrix
    # C = np.dot(np.transpose(Q), P) # Change covariance matrix if row vectors are received
    # C = np.dot(Q, np.transpose(P)) # To calculate rot @ Q = P
    C = np.dot(Q, np.transpose(P))  # To calculate rot @ P = Q

    # Computation of the optimal rotation matrix
    # This can be done using singular value decomposition (SVD)
    # Getting the sign of the det(V)*(W) to decide
    # whether we need to correct our rotation matrix to ensure a
    # right-handed coordinate system.
    # And finally calculating the optimal rotation matrix 'rot'
    # see http://en.wikipedia.org/wiki/Kabsch_algorithm
    V, S, W = np.linalg.svd(C)
    d = (np.linalg.det(V) * np.linalg.det(W)) < 0.0

    if d:
        S[-1] = -S[-1]
        V[:, -1] = -V[:, -1]

    # Create Rotation matrix 'rot'
    _rm = np.dot(V, W)

    return _rm


# ---------------------------------------------------------------------------------
# DUAL QUATERNION ALGORITHM
def quaternion_transform(r):
    """
    Get optimal rotation
    """
    Wt_r = makeW(*r).T
    Q_r = makeQ(*r)
    rot = Wt_r.dot(Q_r)[:3, :3]
    return rot


def makeW(r1, r2, r3, r4=0):
    """
    matrix involved in quaternion rotation
    """
    W = np.asarray([
        [r4, r3, -r2, r1],
        [-r3, r4, r1, r2],
        [r2, -r1, r4, r3],
        [-r1, -r2, -r3, r4]])
    return W


def makeQ(r1, r2, r3, r4=0):
    """
    matrix involved in quaternion rotation
    """
    Q = np.asarray([
        [r4, -r3, r2, r1],
        [r3, r4, -r1, r2],
        [-r2, r1, r4, r3],
        [-r1, -r2, -r3, r4]])
    return Q


def quaternion_rotate(Y, X):
    """
    Calculate the rotation

    Parameters
    ----------
    X : array
        (N,D) matrix, where N is points and D is dimension.
    Y: array
        (N,D) matrix, where N is points and D is dimension.

    Returns
    -------
    rot : matrix
        Rotation matrix (D,D)
    """
    X = X.T
    Y = Y.T

    print('Checking angles between first vector pair...')
    check_angle(X[:, 0], Y[:, 0])
    print('Checking angles between second vector pair...')
    check_angle(X[:, 1], Y[:, 1])

    N = X.shape[0]
    W = np.asarray([makeW(*Y[k]) for k in range(N)])
    Q = np.asarray([makeQ(*X[k]) for k in range(N)])
    Qt_dot_W = np.asarray([np.dot(Q[k].T, W[k]) for k in range(N)])
    # NOTE UNUSED W_minus_Q = np.asarray([W[k] - Q[k] for k in range(N)])
    A = np.sum(Qt_dot_W, axis=0)
    eigen = np.linalg.eigh(A)
    r = eigen[1][:, eigen[0].argmax()]

    _rm = quaternion_transform(r)
    return _rm


# ---------------------------------------------------------------------------------
class quat(object):

    def __init__(self, _q):
        self.q = _q
        self.q0 = _q[0]
        self.q1 = _q[1]
        self.q2 = _q[2]
        self.q3 = _q[3]

    def __add__(self, other):
        return self + other

    def __mul__(self, other):
        [a1, b1, c1, d1] = self.q
        [a2, b2, c2, d2] = other.q
        _q = np.zeros([4, ])
        _q[0] = a1 * a2 - b1 * b2 - c1 * c2 - d1 * d2
        _q[1] = b1 * a2 + a1 * b2 - d1 * c2 + c1 * d2
        _q[2] = c1 * a2 + d1 * b2 + a1 * c2 - b1 * d2
        _q[3] = d1 * a2 - c1 * b2 + b1 * c2 + a1 * d2
        return _q

    @staticmethod
    def dot(q1, q2):
        d = np.zeros([4, ])
        d[0] = q1[0] * q2[0]
        d[1] = q1[1] * q2[1]
        d[2] = q1[2] * q2[2]
        d[3] = q1[3] * q2[3]
        return d

    @staticmethod
    def outer(g1, g2):
        if not type(g1 or g2) is np.ndarray:
            g1, g2 = np.array(g1), np.array(g2)
        d = g1 * np.transpose(g2)
        return d

    @staticmethod
    def conj(_q):
        if not type(_q) is np.ndarray:
            _q = np.array(_q)

        _qconj = np.zeros([4, ])
        _qconj[0] = _q[0]
        _qconj[1] = -1 * _q[1]
        _qconj[2] = -1 * _q[2]
        _qconj[3] = -1 * _q[3]

        return _qconj

    @staticmethod
    def to_quat(_v):
        """
        Make vector or vector sets to quaternions
        q = a + bi + cj + dk
        INPUT: v(3, N), N is number of vectors.
        """
        _v = np.insert(_v, 0, 0, axis=0)
        return _v

    @staticmethod
    def lhs(_q):
        if not type(_q) is np.ndarray:
            _q = np.array(_q)

        [_a, _b, _c, _d] = _q

        lhsm = np.zeros([4, 4])
        lhsm[:, 0] = [_a, _b, _c, _d]
        lhsm[:, 1] = [-_b, _a, _d, -_c]
        lhsm[:, 2] = [-_c, -_d, _a, _b]
        lhsm[:, 3] = [-_d, _c, -_b, _a]

        return lhsm

    @staticmethod
    def rhs(_q):
        if not type(_q) is np.ndarray:
            _q = np.array(_q)

        [_a, _b, _c, _d] = _q

        rhsm = np.zeros([4, 4])
        rhsm[:, 0] = [_a, _b, _c, _d]
        rhsm[:, 1] = [-_b, _a, -_d, _c]
        rhsm[:, 2] = [-_c, _d, _a, -_b]
        rhsm[:, 3] = [-_d, -_c, _b, _a]

        return rhsm

    @staticmethod
    def rotv(_q, _v):
        """
        This is less efficient to function ROTV, can be used to cross-verify
        :param v: v can be a 3d vector or quaternion
        :return: v as column vector
        """
        if not type(_q) is np.ndarray:
            _q = np.array(_q)

        rota = rotations.quat2mat(_q)
        _v = rota @ _v

        return _v

    @staticmethod
    def rotv2(_q, _v):
        """
        This is less efficient to function ROTV, can be used to cross-verify
        :param v: v can be a 3d vector or quaternion
        :return: v as column vector
        """
        if not type(_q) is np.ndarray:
            _q = np.array(_q)

        if P == -1:
            _q = quat.conj(_q)
        else:
            pass

        _v = _v.reshape([3, -1])
        _v = quat.to_quat(_v)
        # This is active rotation
        _v = quat.rhs(quat.conj(_q)) @ quat.lhs(_q) @ _v
        _v = _v[1: 4]
        # rota = quaternion.rhs(quaternion.conj(quat)) @ quaternion.lhs(quat)
        # rota = rota[1:4, 1:4]
        # v = rota @ v

        return _v

    @staticmethod
    def rotq(_q1, _q2):
        return quat.rhs(quat.conj(_q1)) @ quat.lhs(_q1) @ _q2

    @staticmethod
    def fnorm(_q):
        return np.linalg.norm(_q, axis=0)


class symOperator(object):

    def __init__(self, **kwargs):
        self.crystalType = kwargs.get('crystalType', 'cubic')
        if self.crystalType == 'cubic':
            self.symOpCubic = np.zeros([4, 24])
        else:
            self.symOpHex = np.zeros([4, 12])

    @property
    def cubic(self):
        self.symOpCubic[:, 0] = np.array([1, 0, 0, 0])
        self.symOpCubic[:, 1] = np.array([0, 1, 0, 0])
        self.symOpCubic[:, 2] = np.array([0, 0, 1, 0])
        self.symOpCubic[:, 3] = np.array([0, 0, 0, 1])
        self.symOpCubic[:, 4] = np.array([0.5, 0.5, 0.5, 0.5])
        self.symOpCubic[:, 5] = np.array([0.5, -0.5, -0.5, -0.5])
        self.symOpCubic[:, 6] = np.array([0.5, 0.5, -0.5, 0.5])
        self.symOpCubic[:, 7] = np.array([0.5, -0.5, 0.5, -0.5])
        self.symOpCubic[:, 8] = np.array([0.5, -0.5, 0.5, 0.5])
        self.symOpCubic[:, 9] = np.array([0.5, 0.5, -0.5, -0.5])
        self.symOpCubic[:, 10] = np.array([0.5, -0.5, -0.5, 0.5])
        self.symOpCubic[:, 11] = np.array([0.5, 0.5, 0.5, -0.5])
        self.symOpCubic[:, 12] = np.array([1 / np.sqrt(2), 1 / np.sqrt(2), 0, 0])
        self.symOpCubic[:, 13] = np.array([1 / np.sqrt(2), 0, 1 / np.sqrt(2), 0])
        self.symOpCubic[:, 14] = np.array([1 / np.sqrt(2), 0, 0, 1 / np.sqrt(2)])
        self.symOpCubic[:, 15] = np.array([1 / np.sqrt(2), -1 / np.sqrt(2), 0, 0])
        self.symOpCubic[:, 16] = np.array([1 / np.sqrt(2), 0, -1 / np.sqrt(2), 0])
        self.symOpCubic[:, 17] = np.array([1 / np.sqrt(2), 0, 0, -1 / np.sqrt(2)])
        self.symOpCubic[:, 18] = np.array([0, 1 / np.sqrt(2), 1 / np.sqrt(2), 0])
        self.symOpCubic[:, 19] = np.array([0, -1 / np.sqrt(2), 1 / np.sqrt(2), 0])
        self.symOpCubic[:, 20] = np.array([0, 0, 1 / np.sqrt(2), 1 / np.sqrt(2)])
        self.symOpCubic[:, 21] = np.array([0, 0, -1 / np.sqrt(2), 1 / np.sqrt(2)])
        self.symOpCubic[:, 22] = np.array([0, 1 / np.sqrt(2), 0, 1 / np.sqrt(2)])
        self.symOpCubic[:, 23] = np.array([0, -1 / np.sqrt(2), 0, 1 / np.sqrt(2)])

        return self.symOpCubic


def calcRM(_v1, _v2):
    """ Find the rotation matrix that aligns vec1 to vec2
    https://stackoverflow.com/questions/45142959/calculate-rotation-matrix-to-align-two-vectors-in-3d-space
    :param _v1: A 3d "source" vector
    :param _v2: A 3d "destination" vector
    :return mat: A transform matrix (3x3) which when applied to vec1, aligns it with vec2.
    """
    _a, _b = (_v1 / np.linalg.norm(_v1)).reshape(3), (_v2 / np.linalg.norm(_v2)).reshape(3)
    v = np.cross(_a, _b)
    c = np.dot(_a, _b)
    s = np.linalg.norm(v)
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    _rm = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s ** 2))
    return _rm


def randOM(dim=3):
    """
    Creating random orthogonal matrix, i.e. random rotation matrix
    https://stackoverflow.com/questions/38426349/how-to-create-random-orthonormal-matrix-in-python-numpy
    """
    random_state = np.random
    H = np.eye(dim)
    D = np.ones((dim,))
    for n in range(1, dim):
        x = random_state.normal(size=(dim - n + 1,))
        D[n - 1] = np.sign(x[0])
        x[0] -= D[n - 1] * np.sqrt((x * x).sum())
        # Householder transformation
        Hx = (np.eye(dim - n + 1) - 2. * np.outer(x, x) / (x * x).sum())
        mat = np.eye(dim)
        mat[n - 1:, n - 1:] = Hx
        H = np.dot(H, mat)
        # Fix the last sign such that the determinant is 1
    D[-1] = (-1) ** (1 - (dim % 2)) * D.prod()
    # Equivalent to np.dot(np.diag(D), H) but faster, apparently
    H = (D * H.T).T
    return H


