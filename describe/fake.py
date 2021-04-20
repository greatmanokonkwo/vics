import os
os.sys.path.append("..")
from engine import SceneDescribeSystem
from read.engine import ReadingSystem

read = ReadingSystem()
describe = SceneDescribeSystem()
read.run()
describe.run()
read.run()

