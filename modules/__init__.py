# based on info from http://stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python
import os
for module in os.listdir(os.path.dirname(__file__)):
    if module[0:8] != '__init__' and module[-3:] == '.py':
        if module in dir(os.path.dirname(__file__)):
            reload(module)
		else:
            __import__(module[:-3], locals(), globals())
del module
del os