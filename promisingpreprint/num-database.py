import pickle
import preprint

print("{} preprints".format(len(pickle.load(open("preprintdatabase.pickle", "rb")))))
