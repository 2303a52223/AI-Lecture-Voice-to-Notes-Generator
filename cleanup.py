import os
path = "pages"
for f in os.listdir(path):
    if "Copy" in f:
        fpath = os.path.join(path, f)
        try:
            os.remove(fpath)
            print(f"Deleted: {fpath}")
        except Exception as e:
            print(f"Error deleting {fpath}: {e}")
