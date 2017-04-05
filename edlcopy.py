from __future__ import print_function
import sys
import os
import getopt
import shutil
# import ntpath
# import decimal


def main(argv):
   input_edl = ''
   src_root_dir = ''
   dest_root_dir = ''
   file_names = []
   file_queue = []
   files_not_found = []
   accumulated_size = None

   try:
       opts, args = getopt.getopt(argv, "hi:s:o:" , ["ifile=","sourcedir=","outputdir="])
   except getopt.GetoptError:
       print ('edlcopy.py -i <inputfile> -s <sourcedirectory> -o <outputdirectory>')
       sys.exit(2)

   for opt , arg in opts:
       if opt == '-h':
           print ('edlcopy.py -i <inputfile> -s <sourcedirectory> -o <outputdirectory>')
           sys.exit()
       elif opt in ("-i","--ifile"):
           input_edl = os.path.normpath(arg)
       elif opt in ("-s","--sourcedir"):
           src_root_dir = os.path.normpath(arg)
       elif opt in ("-o","--outputdir"):
           dest_root_dir = os.path.normpath(arg)

   shot_names = get_shots_from_edl(input_edl)

   for shot_name in shot_names:
       shot_file = find_file_in_dir(src_root_dir,shot_name)
       isinstance(shot_file,list)
       if not shot_file:
           files_not_found.append(shot_name)
       else:
           file_queue.append(shot_file)

   print ("found the following files:")
   for task in file_queue:
       print (task[0])

   print ("did not find the following files:")
   for file_unfound in files_not_found:
       print (file_unfound)

   accumulated_size = copytask_accumulated_size(file_queue)
   print(accumulated_size)

   for file in file_queue:
       copy_file(file[0],src_root_dir,dest_root_dir)
   
"""Extracts all the shots/files used inside the Edl (AVID only a.t.m.)"""
def get_shots_from_edl(edl_file):
    found_shots = []
    with open (edl_file, 'r') as f:
        for line in f:
            if "FROM CLIP NAME" in line:
                shot = line.split(":",1)[1].lstrip(' ').splitlines()[0]
                found_shots.append(shot)
    return found_shots


"""Find a file in a given directory,
   returns metadata[][] containing Filepath and Filesize """
def find_file_in_dir(source_dir,filename):
    metadata = []
    for root, dirs ,files in os.walk(source_dir):
            for file in files:
                if filename in file:
                    file_path = os.path.join(root,file)
                    metadata.append(file_path)
                    metadata.append(os.path.getsize(file_path))
    return metadata


"""Get the SUM of filesizes from all tasks in the queue"""
def copytask_accumulated_size(files_in_queue):
    
    accumulated_size = 0.0
    
    for copytask in files_in_queue:
       accumulated_size = accumulated_size + float(copytask[1])

    """Convert accumulated_size to MegaBytes in return value"""
    return (accumulated_size/1000)/1000
        

def copy_file(src_file, src_root_dir, dest_root_dir):

    src_dir_path = os.path.dirname(src_file)
    src_file_name = os.path.basename(src_file)

    subtree = src_dir_path.replace(src_root_dir, "")
    dest_file_path = dest_root_dir + subtree
    dest_file = os.path.join(dest_file_path,src_file_name)


    if not os.path.exists(dest_file_path):
        os.makedirs(dest_file_path)

    """Check if file doesn't already exist on location"""
    if not os.path.exists(dest_file):
        print("Start copy " + src_file_name + "...")
        shutil.copy(src_file,dest_file_path)
        print("done")
    else:
        print("File already exists on destination")





    
        
if __name__ == "__main__":
   main(sys.argv[1:])