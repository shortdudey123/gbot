# based on info from http://stackoverflow.com/questions/1057431/loading-all-modules-in-a-folder-in-python
# more info in my own question: http://stackoverflow.com/questions/24718759/how-do-i-dynamically-reload-a-module-in-a-custom-package
import os
import sys
import imp


# based off of https://github.com/myano/jenni/blob/master/modules/reload.py#L40
def reload_modules(moduleName):
    name = '{0}.{1}'.format(os.path.dirname(__file__).split('/')[-1:][0], moduleName)
    if name in sys.modules.keys():
        filePath = sys.modules[name].__file__
        if filePath.endswith('.pyc') or filePath.endswith('.pyo'):
            filePath = filePath[:-1]
        module = imp.load_source(name, filePath)
        sys.modules[name] = module
    else:
        pass

for module in os.listdir(os.path.dirname(__file__)):
    if module[0:8] != '__init__' and module[-3:] == '.py':
        name = '{0}.{1}'.format(os.path.dirname(__file__).split('/')[-1:][0], module[:-3])
        __import__(module[:-3], locals(), globals())
