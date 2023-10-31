from zipfile import ZipFile
import os
import shutil
import subprocess
import platform

# Deciding on directory sep. Mac&Linux us '/' while Windows uses '\'
os_separator: str = "/" if platform.system() in ["Linux", "Darwin"] else "\\"


# current directory
curr_dir = os.path.abspath('.') + os_separator

# Haven't tested it with submissions of multiple java files but should handle

# Moss supports these languages

# C, C++, Java, C#, Python, Visual Basic, Javascript, FORTRAN, ML,
# Haskell, Lisp, Scheme, Pascal, Modula2, Ada,
# Perl, TCL, Matlab, VHDL, Verilog, Spice,
# MIPS assembly, a8086 assembly, a8086 assembly, HCL2.

test_exist = curr_dir+os_separator+'StudentCode'+os_separator+'namedFiles'
if os.path.exists(test_exist) and os.listdir(test_exist):
    y_n = str(input(
        "namedFiles already exists and contains files. Would you like to empty it?")).lower()[0]
    if y_n == 'y':
        shutil.rmtree(test_exist)

# Choosing a file extension
java_or_else = str(
    input('Use .java file extension? if not, enter the file extension to use (.cpp,.py,etc)'))
file_extension = '.java' if len(java_or_else) == 0 or java_or_else.lower()[
    0] == 'y' else java_or_else
print('Using {} as file extension and {} as directory seperator'.format(
    file_extension, os_separator))


# Have your pilot-downloaded zip file inside current dir/StudentCode/
# Scan dir
dir = '.'+os_separator+'StudentCode'
if not os.path.exists(dir):
    os.mkdir(dir)

unzipped_dir = dir+os_separator+'unzipped'

named_dir = dir+os_separator+'namedFiles'


def unzip():
    """
    unizps main zip file downloaded from Pilot into unzipped directory
    """
    try:
        shutil.rmtree(unzipped_dir)
    except:
        pass
    file_name = [file for file in os.listdir(dir) if file[-4:] == '.zip'][0]
    if not file_name:
        print('no zip files found')
        exit(0)
    with ZipFile(dir+os_separator+file_name, 'r') as zip:
        os.mkdir(unzipped_dir)
        zip.extractall(unzipped_dir)


def javaFileToDirectory():
    """
    Finds .java file submissions and turns them into the format lastName.java
    and moves them to namedFiles category
    """
    if not os.path.exists(dir+os_separator+'namedFiles'):
        os.mkdir(dir+os_separator+'namedFiles')
    for file_name in os.listdir(unzipped_dir):
        if file_name[-5:] == file_extension:
            new_name = file_name.split(' - ')[1].split()[1] + file_extension
            os.rename(unzipped_dir+os_separator+file_name,
                      curr_dir+dir+os_separator+'namedFiles'+os_separator+new_name)


def dealWithZip():
    """
    deals with leftover zip files that were submitted as zips in pilot
    creates temp lastName.dir folders that the .zip gets extracted to
    """
    i = 0
    for zipped_file in os.listdir(unzipped_dir):
        if zipped_file[-4:] != '.zip':
            continue
        with ZipFile(unzipped_dir+os_separator+zipped_file, 'r') as zf:
            temp_dir = unzipped_dir+os_separator + \
                (zipped_file.split(' - ')[1].split()[1])+'.dir'
            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)
            zf.extractall(temp_dir)
            i += 1


def find_Java(search_path):
    """
    searches for .java files and notes the directory title which is the last name so we can move it later
    to namedFiles
    gets abs paths of the .java files
    """
    results = []
    titles = []  # names of students
    title = ''
    # Wlaking top-down from the root
    for root, dir, files in os.walk(search_path):
        java_files = []
        # title = parent folder name. just so we save the name of the student that we are currently in
        title = root.split(
            os_separator)[-1] if root.split(os_separator)[-1][-4:] == '.dir' else title
        java_files = [os.path.join(root, file)
                      for file in files if file[-5:] == file_extension and file[0:2] != '._']  # '._' is a MacOS thing
        if java_files:
            titles.append(title)
            results.extend(java_files)
    return results, titles

# moves files in list


def moveFiles(lst, titles):
    """
    searches for .java files and notes the directory title which is the last name so we can move it later
    to namedFiles
    gets abs paths of the .java files
    """
    silly_number = str(1)
    for i in range(len(lst)):
        file_path = lst[i]
        new_path = named_dir+os_separator+titles[i]
        if os.path.exists(new_path):
            new_path = new_path.split(file_extension)[
                0]+silly_number+file_extension
            silly_number = str(int(silly_number)+1)
        os.rename(file_path, new_path)
    shutil.rmtree(unzipped_dir)


# unzip big pilot zip
unzip()
# make .java files into dirs
javaFileToDirectory()
# make .zip files into dirs of lastName.dir format
dealWithZip()

# get all .java file abs paths
zip_dirs, titles = find_Java(unzipped_dir)
titles = list(map(lambda x: x[0:len(x)-4]+file_extension, titles))
print('Found {} submissions.'.format(len(titles) + len(os.listdir(named_dir))))
# move .java files into namedFiles
moveFiles(
    zip_dirs, titles)

# # run moss!
subprocess.Popen(
    f'.{os_separator}moss .{os_separator}StudentCode{os_separator}namedFiles{os_separator}*.java', shell=True)

# WIP
# mossum = input('run mossum too?').lower()[0] == 'y'
# if mossum:
#     percentage = input('what\'s the lower limit %')
#     percentage = int(percentage[:-1]) if percentage[-1] == '%' else int(percentage)
#     link = input('provide link')
#     subprocess.Popen('mossum -p {} {}'.format(percentage,link), shell=True)
