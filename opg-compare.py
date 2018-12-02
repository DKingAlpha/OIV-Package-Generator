import os
import shutil
import logging
from gamedata.gtav import *


# Log to files for further reference.
logging.basicConfig(filename=OPG_WORKING_DIRECTORY+'.1.log', filemode='w', format='%(message)s', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())



# First, copy misc files(hooks, asi, scripts, fx, etc) except rpf archives
# This only need to run once unless they changed again, so you can mask the copy process later to save some time.
logging.info('Copying files possibly related to modding:')
logging.info('='*32)
for f in os.listdir(GTA_V_PATH):
    if f in GTA_V_SKIP:
        continue
    if f.endswith('.log'):
        continue
    if f.endswith('.rpf'):
        continue
    if os.path.isfile(os.path.join(GTA_V_PATH, f)):
        if f not in GTA_V_STOCK_FILES:
            logging.info(f)
            ### you may comment the next line to skip copy process
            #shutil.copyfile(os.path.join(GTA_V_PATH, f), os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG', 'content' ,f))
    else:
        if f not in GTA_V_STOCK_FOLDERS:
            logging.info(f)
            ### you may comment the next line to skip copy process
            #shutil.copytree(os.path.join(GTA_V_PATH, f), os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG', 'content' ,f))
logging.info('='*32+ '\r\n\r\n')



### Here we begin to handle RPF archives

RPF_FILES = []
for rootfolder in os.listdir(GTA_V_PATH):
    if rootfolder!='mods' and rootfolder in GTA_V_SKIP:
        continue
    if os.path.isfile(os.path.join(GTA_V_PATH, rootfolder)):
        if rootfolder.endswith('.rpf'):
            RPF_FILES.append(rootfolder)
    else:
        RPF_FILES.extend([ os.path.relpath(os.path.join(root, name), GTA_V_PATH)
                            for root, dirs, files in os.walk(os.path.join(GTA_V_PATH, rootfolder))
                            for name in files
                            if name.endswith('.rpf')])

MODS_RPF_FILES  = [os.path.relpath(f, 'mods').lower() for f in RPF_FILES if f.startswith('mods')]
STOCK_RPF_FILES = [f.lower() for f in RPF_FILES if not f.startswith('mods')]


logging.info('Please wait. Handling RPF archives...')
need_to_be_copied = []
for mrpf in MODS_RPF_FILES:
    if mrpf not in STOCK_RPF_FILES:
        mrpf_parent = os.path.dirname(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'rpf', 'mods', mrpf))
        os.makedirs(mrpf_parent, exist_ok=True)
        #shutil.copyfile(os.path.join(GTA_V_PATH, 'mods', mrpf), os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'rpf', 'mods', mrpf) )
        logging.info('    Directly Coping: ' + os.path.join('mods', mrpf))
    else:
        os.makedirs(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'rpf', 'base', mrpf), exist_ok=True)
        os.makedirs(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'rpf', 'mods', mrpf), exist_ok=True)
        need_to_be_copied.append(mrpf)
        logging.info('    Creating Placeholder: ' + os.path.join(mrpf))


logging.info('\r\n\r\n')
logging.info('RPF files supposed to be extracted manually:')
logging.info('='*32)
for ntbc in need_to_be_copied:
    logging.info(ntbc)
logging.info('='*32 + '\r\n\r\n')


logging.info('All new files added and needed rpf files listed in OPG working directory')
logging.info('1. Now, open OpenIV, select GTA V for Windows.  (You can run multiple OpenIV instances too save a little more time)')
logging.info('2. Navigate to "Grand Theft V/' + OPG_WORKING_DIRECTORY + '/rpf/mods", and in OpenIV export the listed MODDED rpf files into the empty directory')
logging.info('3. At last, as the reference, export the ORIGINAL rpf files in "Grand Theft V/' + OPG_WORKING_DIRECTORY + '/rpf/base"')
logging.info('4. Check every directories to make sure all files are in the right place.')
logging.info('5. Run opg-generate.py')
logging.info('(These can not be automatically done so far. RPF7 decryption for GTA V is tough for me)')
