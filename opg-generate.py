import os
import shutil
import logging
import filecmp
import zipfile
import xml.etree.cElementTree as ET
import xml.dom.minidom

from gamedata.gtav import *


SCRIPT_BASE_DIR = os.path.split(os.path.realpath(__file__))[0]

logging.basicConfig(filename=OPG_WORKING_DIRECTORY+'.2.log', filemode='w', format='%(message)s', level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler())




def add_static_binaries(xmlroot):
    save_cwd = os.getcwd()
    os.chdir(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG'))

    static_files = []
    for rootfolder in os.listdir('content'):
        if rootfolder.endswith('.rpf') or rootfolder in GTA_V_STOCK_FOLDERS:
            continue

        if os.path.isfile(os.path.join('content', rootfolder)):
            static_files.append(rootfolder)
        else:
            static_files.extend([ os.path.relpath(os.path.join(root, name), 'content')
                                for root, dirs, files in os.walk(os.path.join('content', rootfolder))
                                for name in files])
    os.chdir(save_cwd)

    for f in static_files:
        ET.SubElement(xmlroot, 'add', source=f).text = f


def flat_mixed_file_folder_list(mixed_list, act):
    flated = []
    target = 'mods'
    if act == 'del':
        target = 'base'
    for f in mixed_list:
        if os.path.isfile(os.path.join(target, f)):
            flated.append(f)
        else:
            flated.extend([ os.path.relpath(os.path.join(root, name), target)
                            for root, dirs, files in os.walk(os.path.join(target, f))
                            for name in files])
    return flated




def get_rpf_level(path, act):
    retval = []
    if not '.rpf' in os.path.dirname(path):
        return retval
    rel_rpf_path = ''
    for name in path.split(os.sep):
        rel_rpf_path = os.path.join(rel_rpf_path, name)
        if name.endswith('.rpf'):
            retval.append(rel_rpf_path)
            rel_rpf_path = ''
    target = 'mods'
    if act == 'del':
        target = 'base'
    if path.endswith('.rpf') and os.path.isfile(os.path.join(target, path)):
        retval = retval[:-1]
    return retval


def note_difflist_to_xml(xml_basenode, mixed_list, act):
    for f in flat_mixed_file_folder_list(mixed_list, act):
        archive_node = xml_basenode
        prefix_path = ''
        for archive_path in get_rpf_level(f, act):
            try_to_get_existed_archive_node = archive_node.find('archive[@path="%s"]' % archive_path)
            prefix_path = os.path.join(prefix_path, archive_path)
            if try_to_get_existed_archive_node:
                archive_node = try_to_get_existed_archive_node
            else:
                archive_node = ET.SubElement(archive_node, 'archive', path=archive_path, createIfNotExist='True', type="RPF7")
        sf = os.path.relpath(f, prefix_path)
        if act == 'add':
            ET.SubElement(archive_node, 'add', source=sf).text = sf
            logging.info('          ADD: ' + f)
            os.makedirs(os.path.dirname(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG', 'content', f)), exist_ok=True)
            shutil.copyfile(os.path.join('mods', f), os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG', 'content', f))
        if act == 'del':
            ET.SubElement(archive_node, 'delete').text = sf
            logging.info('          DEL: ' + f)
        if act == 'mod':
            ET.SubElement(archive_node, 'add', source=sf).text = sf
            logging.info('          MOD: ' + f)
            os.makedirs(os.path.dirname(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG', 'content', f)), exist_ok=True)
            shutil.copyfile(os.path.join('mods', f), os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG', 'content', f))


def recursive_diff(dc, xmlroot):

    cur_dir = os.path.relpath(dc.left, 'mods')

    if cur_dir.endswith('.rpf'):
        logging.info('Scanning: ' + cur_dir)
        # save when finished each rpf
        save_current_xml_to_file(content)
    else:
        logging.debug('Scanning: ' + cur_dir)

    note_difflist_to_xml(xmlroot, [os.path.join(cur_dir, f) for f in dc.left_only],  'add')
    note_difflist_to_xml(xmlroot, [os.path.join(cur_dir, f) for f in dc.right_only], 'del')
    note_difflist_to_xml(xmlroot, [os.path.join(cur_dir, f) for f in dc.diff_files], 'mod') # overwrite

    failed_msg = ''
    for f in dc.funny_files:
        failed_msg = failed_msg + f + ', ' 
    if failed_msg:
        logging.warn('Failed to compare in ' + cur_dir + ': ' + failed_msg)

    for sd in dc.subdirs.values():
        recursive_diff(sd, xmlroot)


def save_current_xml_to_file(xmlcontent):
    minidomxml = xml.dom.minidom.parseString(ET.tostring(xmlcontent))
    pretty_xml_as_string = minidomxml.toprettyxml()
    xmlfile = open(os.path.join(SCRIPT_BASE_DIR, 'assembly-content.xml'), 'w')
    xmlfile.write(pretty_xml_as_string)
    xmlfile.close()


#content = ET.Element("content")
#
#
#logging.info('Adding Static Files to XML...')
#add_static_binaries(content)
#save_current_xml_to_file(content)
#logging.info('Static Files Added.\r\n\r\n')
#
#
#logging.info('Running diff against the two rpf directories\r\n\r\n')
#os.chdir(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'rpf'))
#MODS_RPF_DIR = 'mods'
#ORIG_RPF_DIR = 'base'
#rpf_diff = filecmp.dircmp(MODS_RPF_DIR, ORIG_RPF_DIR)
#
#
#
#logging.info('Scanning: .')
#recursive_diff(rpf_diff, content)
#save_current_xml_to_file(content)



### Almost finished
print('Almost done! Please check the generated files in "Grand Theft V/' + OPG_WORKING_DIRECTORY + '/PKG/')
print('Once you make sure that everything looks good, hit ENTER to finish the final packaging.')
input('PRESS ENTER TO CONTINUE...')

### Packing up
shutils.copyfile(os.path.join(SCRIPT_BASE_DIR, 'icon.png'), os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG', 'icon.png'))

full_asm_xml = xml.dom.minidom.parse(os.path.join(SCRIPT_BASE_DIR, 'assembly-template.xml'))
content_xml  = xml.dom.minidom.parse(os.path.join(SCRIPT_BASE_DIR, 'assembly-content.xml'))
full_asm_xml.documentElement.appendChild(content_xml.documentElement)

final_pretty_xml_as_string = full_asm_xml.toxml()
final_xmlfile = open(os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG', 'assembly.xml'), 'w')
final_xmlfile.write(fiinal_pretty_xml_as_string)
final_xmlfile.close()

def zip_folders(root, folders, zip_filename):
    zip_file = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(os.path.join(root ,folder)):
            for filename in filenames:
                zip_file.write(
                    os.path.join(dirpath, filename),
                    os.path.relpath(os.path.join(dirpath, filename), root))
    zip_file.close()


print('Zipping...')
oiv_pkg_name =  full_asm_xml.documentElement.getElementsByTagName('metadata')[0].getElementsByTagName('name')[0].childNodes[0].nodeValue
zip_folders(root=os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, 'PKG'),
            folders=['content', 'icon.png', 'assembly.xml'],
            zip_filename=os.path.join(GTA_V_PATH, OPG_WORKING_DIRECTORY, oiv_pkg_name + '.oiv'))
