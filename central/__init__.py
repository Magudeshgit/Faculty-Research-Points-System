from pathlib import Path
import pickle
import time
starttime = time.time()
BASE_DIR = Path(__file__).resolve().parent.parent
print("Initializing Course Verifier ML Model")
file = open(f'{BASE_DIR}\\central\\ML\\courseverifier.pkl', 'rb')
model = pickle.load(file)
print(f"Course Verifier ML Model Successfully Loaded in {time.time() - starttime} second(s)")