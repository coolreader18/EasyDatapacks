import os
import shutil

from .namespace import *
from .function import CompilationError

MCMETA = '''{
    "pack" : {
        "pack_format" : 3,
        "description" : "data pack generated by EasyDatapacks"
    }
}
'''

LOADTICK = '''{
    "values" : [
    %s
    ]
}'''


def compile(destination, files, verbose=False, nofiles=False):
    """files is a list of text files containing your code.
    destination points to the folder where you want your datapack to end up"""

    packname = destination.split('/')[-1].split('\\')[-1]

    namespace = Namespace(packname, files)
    namespace.compile(verbose)

    if nofiles:
        return False

    # generate the file layout
    os.chdir("..")

    def create_folder(*path):
        try:
            os.mkdir(os.path.join(*path))
        except FileExistsError:
            pass

    create_folder(destination)
    create_folder(destination, 'data')
    with open(os.path.join(destination, 'pack.mcmeta'), 'w') as f:
        f.write(MCMETA)
    create_folder(destination, 'data', 'minecraft')
    create_folder(destination, 'data', 'minecraft', 'tags')
    create_folder(destination, 'data', 'minecraft', 'tags', 'functions')

    # load
    with open(os.path.join(destination, 'data', 'minecraft', 'tags', 'functions', 'load.json'), 'w') as f:
        for func in namespace.functions:
            if func == 'main.load':
                f.write(LOADTICK % ('"' + packname + ':load"'))
                break
        else:
            f.write(LOADTICK % "")

    # tick
    with open(os.path.join(destination, 'data', 'minecraft', 'tags', 'functions', 'tick.json'), 'w') as f:
        for func in namespace.functions:
            if func == 'main.tick':
                f.write(LOADTICK % ('"' + packname + ':tick"'))
                break
        else:
            f.write(LOADTICK % "")

    # actual datapack
    create_folder(destination, 'data', packname)

    try:
        shutil.rmtree(os.path.join(destination, 'data', packname, 'functions'))
    except:
        pass
        
    create_folder(destination, 'data', packname, 'functions')
    for func in namespace.functions:
        with open(os.path.join(destination, 'data', packname, 'functions', func[5:] + '.mcfunction'), 'w') as f:
            f.write('\n'.join(namespace.functions[func].commands))

    return True
