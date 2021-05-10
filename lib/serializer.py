import pickle


def serialize(objects, filename):
    with open(filename, 'wb') as f:
        pickle.dump(len(objects), f)
        for obj in objects:
            pickle.dump(obj, f)


def deserialize(filename):
    objects = []
    with open(filename, 'rb') as f:
        for _ in range(pickle.load(f)):
            objects.append(pickle.load(f))

    return objects
