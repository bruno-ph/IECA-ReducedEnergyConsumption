#!/usr/bin/python3

# Executor module. This module was written to facilitate the execution of large parameter intervals.
from subprocess import run

import pdb
from multiprocessing import Pool, cpu_count
import os
#detect how many processes will run at the same time
try:
        workers = 6#cpu_count()-1
except NotImplementedError:
        workers = 1

#initialize pool of processes
processes = []


                             

inst = [ ('c101C10.txt', 10), ('c101C5.txt', 5), ('c101_21.txt', 100), ('c102_21.txt', 100), ('c103C15.txt', 15), ('c103C5.txt', 5), ('c103_21.txt', 100), ('c104C10.txt', 10), ('c104_21.txt', 100), ('c105_21.txt', 100), ('c106C15.txt', 15), ('c106_21.txt', 100), ('c107_21.txt', 100), ('c108_21.txt', 100), ('c109_21.txt', 100), ('c201_21.txt', 100), ('c202C10.txt', 10), ('c202C15.txt', 15), ('c202_21.txt', 100), ('c203_21.txt', 100), ('c204_21.txt', 100), ('c205C10.txt', 10), ('c205_21.txt', 100), ('c206C5.txt', 5), ('c206_21.txt', 100), ('c207_21.txt', 100), ('c208C15.txt', 15), ('c208C5.txt', 5), ('c208_21.txt', 100), ('r101_21.txt', 100), ('r102C10.txt', 10), ('r102C15.txt', 15), ('r102_21.txt', 100), ('r103C10.txt', 10), ('r103_21.txt', 100), ('r104C5.txt', 5), ('r104_21.txt', 100), ('r105C15.txt', 15), ('r105C5.txt', 5), ('r105_21.txt', 100), ('r106_21.txt', 100), ('r107_21.txt', 100), ('r108_21.txt', 100), ('r109_21.txt', 100), ('r110_21.txt', 100), ('r111_21.txt', 100), ('r112_21.txt', 100), ('r201C10.txt', 10), ('r201_21.txt', 100), ('r202C15.txt', 15), ('r202C5.txt', 5), ('r202_21.txt', 100), ('r203C10.txt', 10), ('r203C5.txt', 5), ('r203_21.txt', 100), ('r204_21.txt', 100), ('r205_21.txt', 100), ('r206_21.txt', 100), ('r207_21.txt', 100), ('r208_21.txt', 100), ('r209C15.txt', 15), ('r209_21.txt', 100), ('r210_21.txt', 100), ('r211_21.txt', 100), ('rc101_21.txt', 100), ('rc102C10.txt', 10), ('rc102_21.txt', 100), ('rc103C15.txt', 15), ('rc103_21.txt', 100), ('rc104_21.txt', 100), ('rc105C5.txt', 5), ('rc105_21.txt', 100), ('rc106_21.txt', 100), ('rc107_21.txt', 100), ('rc108C10.txt', 10), ('rc108C15.txt', 15), ('rc108C5.txt', 5), ('rc108_21.txt', 100), ('rc201C10.txt', 10), ('rc201_21.txt', 100), ('rc202C15.txt', 15), ('rc202_21.txt', 100), ('rc203_21.txt', 100), ('rc204C15.txt', 15), ('rc204C5.txt', 5), ('rc204_21.txt', 100), ('rc205C10.txt', 10), ('rc205_21.txt', 100), ('rc206_21.txt', 100), ('rc207_21.txt', 100), ('rc208C5.txt', 5), ('rc208_21.txt', 100)]
alpha_beta = [('1','1'),('2','1')] #(1,2) skipped as it is the default

customer_multiplier = (0.5,0.7,1)


pyfile = "python3"
folder_name = "IECA-ReducedEnergyConsumption"
main_file = os.path.join("source","main.py")
repet = 1
for i in range(repet):
        for c in customer_multiplier:
            for ins in inst:
                #[instance, opt] = ins
                custam = int(ins[1]*c)
                input_file = os.path.join("evrptw_instances",f"{ins[0]}")
                output_file = os.path.join("results",f"{'a1b2_c'+str(custam)+'_'+ins[0]}.json")
                processes.append([f"{pyfile}", f"{main_file}",f"-file {input_file}",f"-pop {custam}",f"-outfile {output_file}"])

for i in range(repet):
        for ab in alpha_beta:
            for ins in inst:
                #[instance, opt] = ins
                custam = int(ins[1])
                input_file = os.path.join("evrptw_instances",f"{ins[0]}.txt")
                output_file = os.path.join("results",f"a{ab[0]}b{ab[1]}_c{str(custam)+'_'+ins[0]}.json")
                processes.append([f"{pyfile}",f"{main_file}",f"-file {input_file}",f"-alpha {ab[0]}",f"-beta {ab[1]}",f"-outfile {output_file}"])

print ("Total processes:{}".format(len(processes)),processes)

#code to call the processes
pool = Pool(processes=workers)
result = pool.map(run,processes)
print(result)

#nohup no console
