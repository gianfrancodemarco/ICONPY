import pickle
import src


class RenameUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        renamed_module = module
        if module == "lib.wikidata.wikimovie":
            renamed_module = "src.lib.wikidata.WikiMovie"

        return super(RenameUnpickler, self).find_class(renamed_module, name)


def renamed_load(file_obj):
    return RenameUnpickler(file_obj).load()


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
        return renamed_load(f)


def deserialize_objects(filename):
    objects = []
    with open(filename, 'rb') as f:
        for _ in range(pickle.load(f)):
            objects.append(pickle.load(f))

    return objects
