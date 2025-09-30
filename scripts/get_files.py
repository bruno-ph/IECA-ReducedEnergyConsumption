from os import listdir,getcwd
from os.path import isfile, join
##RUN FROM PROJECT ROOT FOLDER
current_dir = getcwd()
instance_folder = join(current_dir,"evrptw_instances")
print(instance_folder)

files = [f for f in listdir(instance_folder) if f!="readme.txt"]
if files:
    objective_file = join(current_dir,"scripts","files.txt")
    file = open(objective_file, "w")
    for filename in files:

        file.write(f"{filename}\n")
    file.close()