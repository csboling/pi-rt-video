import numpy as np


def translation_matrix(translation):
    return np.hstack([
        np.vstack([
            np.eye(3),
            np.array(translation).reshape(1, 3),
        ]),
        np.array([[0, 0, 0, 1]]).T,
    ])

   
