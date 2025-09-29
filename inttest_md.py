import md
import os

md.run_md()

if not os.path.exists("cu.traj"):
    raise AssertionError("cu.traj was not created!")

if os.stat("cu.traj") == 0:
    raise AssertionError("cu.traj is empty file")