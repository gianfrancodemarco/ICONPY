import pickle


def serialize_objects(objects, filename):
    with open(filename, 'wb') as f:
        pickle.dump(len(objects), f)
        for obj in objects:
            pickle.dump(obj, f)


def serialize(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)


def deserialize(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def deserialize_objects(filename):
    objects = []
    with open(filename, 'rb') as f:
        for _ in range(pickle.load(f)):
            objects.append(pickle.load(f))

    return objects
