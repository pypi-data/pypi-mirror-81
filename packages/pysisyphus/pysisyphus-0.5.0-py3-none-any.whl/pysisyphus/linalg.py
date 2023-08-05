import numpy as np


def gram_schmidt(vecs, thresh=1e-8):
    def proj(v1, v2): return v1.dot(v2)/v1.dot(v1)
    ortho = [vecs[0], ]
    for v1 in vecs[1:]:
        tmp = v1.copy()
        for v2 in ortho:
            tmp -= proj(v2, v1)*v2
        norm = np.linalg.norm(tmp)
        # Don't append linear dependent vectors, as their norm will be
        # near zero. Renormalizing them to unity would lead to numerical
        # garbage and to erronous results later on, when we orthgonalize
        # against this 'arbitrary' vector.
        if norm <= thresh:
            continue
        ortho.append(tmp / norm)
    return np.array(ortho)


def perp_comp(vec, along):
    """Return the perpendicular component of vec along along."""
    return vec - vec.dot(along)*along


def make_unit_vec(vec1, vec2):
    """Return unit vector pointing from vec2 to vec1."""
    diff = vec1 - vec2
    return diff / np.linalg.norm(diff)
