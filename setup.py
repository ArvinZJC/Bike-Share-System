try:
    import matplotlib
    import numpy
    import pandas
    import PIL
except ImportError:
    print('Oops! Any necessary third-party package is missing.')
    print('Setup would help you to install any missing package.')
    print('NOTE: if the setup fails to do that, you may need to install the packages manually by running the command `pip3 install -r requirements.txt` under the directory same as that of the setup.\n')
    import subprocess
    import sys
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])

from bss import bss_run

bss_run.main()