GTA_V_PATH = 'D:\Games\SteamLibrary\steamapps\common\Grand Theft Auto V'


OPG_WORKING_DIRECTORY = 'OPG-Temp'

GTA_V_SKIP = [
    '_CommonRedist',
    'Installers',
    'ReadMe',
    'mods',
    'installscript.vdf',
    'steam_api64.dll',
    'desktop.ini',
    OPG_WORKING_DIRECTORY
]


GTA_V_STOCK_FILES = [
    'bink2w64.dll',
    'commandline.txt',
    'd3dcompiler_46.dll',
    'd3dcsx_46.dll',
    'GFSDK_ShadowLib.win64.dll',
    'GFSDK_TXAA.win64.dll',
    'GFSDK_TXAA_AlphaResolve.win64.dll',
    'GTA5.exe',
    'GTAVLauncher.exe',
    'GTAVLanguageSelect.exe'
]


GTA_V_STOCK_FOLDERS = [
    'update',
    'x64',
]

import os
# check game path
while not os.path.exists(GTA_V_PATH):
    print('GTA V PATH not exists, please set new path.')
    GTA_V_PATH = raw_input('GTA V PATH:')

# make working directory under game folder
os.makedirs(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG', 'content'), exist_ok=True)
os.makedirs(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'rpf', 'base'), exist_ok=True)
os.makedirs(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'rpf', 'mods'), exist_ok=True)
