from scipy.spatial import distance

LEFT_EYE = [36, 37, 38, 39, 40, 41]
RIGHT_EYE = [42, 43, 44, 45, 46, 47]

def ear(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def is_blinking(shape):
    points = [(shape.part(i).x, shape.part(i).y) for i in range(68)]
    left = [points[i] for i in LEFT_EYE]
    right = [points[i] for i in RIGHT_EYE]

    avg_ear = (ear(left) + ear(right)) / 2.0
    return avg_ear < 0.21
