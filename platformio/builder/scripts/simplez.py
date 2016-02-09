"""
    Build script for simplez soft-processor on an FPGAs
    simplez-builder.py
"""
import os
from os.path import join
from SCons.Script import (AlwaysBuild, Builder, DefaultEnvironment,
                          Glob)

HOME = os.environ.get('HOME')
LOCALBIN = join(HOME, '.local', 'bin')
print("LOCALBIN: {}".format(LOCALBIN))

env = DefaultEnvironment()
env.Replace(ENV={'PATH': os.environ['PATH']})

# -- Get the local folder in which the simplez tools should be installed
piopackages_dir = env.subst('$PIOPACKAGES_DIR')
bin_dir = join(piopackages_dir, 'toolchain-simplez', 'bin')

# -- Add the $HOME/.local/bin to the path
# -- There are locate the tools when installed with pip3
env.PrependENVPath('PATH', LOCALBIN)

# -- Add this path to the PATH env variable. First the building tools will be
# -- searched in the local PATH. If they are not founde, the global ones will
# -- be executed (if installed)
env.PrependENVPath('PATH', bin_dir)

# -- Get a list of all the asm files in the src folfer, in ASCII, with
# -- the full path
# -- All these programs will be assembled
asm_nodes = Glob(join(env['PROJECTSRC_DIR'], '*.asm'))

# -- Builder (.asm --> .list)
assembler = Builder(action='sasm $SOURCE -o $TARGET',
                    suffix='.list',
                    src_suffix='.asm')

env.Append(BUILDERS={'Assemble': assembler})

progs = env.Assemble(asm_nodes)

try:
    prog = progs[0]
except IndexError:
    prog = None
    print("Warning: NO .asm files!!!")

upload = env.Alias('upload', prog, 'sboot $SOURCE')
AlwaysBuild(upload)
