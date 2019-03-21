from glob import glob
import matplotlib.pyplot as plt

"""

What is AFPO?
In the optimization algorithm AFPO (Age-Fitness Pareto Optimization), randomly generated candidate designs (solutions) 
are injected into the population each generation with age zero. Every generation, modified copies are made of each 
design in the population, and the age of each design (both the originals and the mutated copies) are incremented by one. 
Next, selection reduces the population to some pre-specified size (deletes the worst designs) using the concept of 
Pareto dominance and the two objectives of fitness (maximized) and age (minimized). 


What is the Rainbow Waterfall plot?
Each generation, the most fit candidate design with age N is connected to the most fit design in the the previous 
generation with age N-1, for all N in the set of ages (of the designs) present in the current population.


What does the Rainbow Waterfall tell us?
It indicates whether optimization has prematurely converged or if, instead, fitness is continuing to improve. It
shows the dynamics of the two objectives of age and fitness and how they affect the discovery of novel and fit designs.


What stuff is required to run this script?
This script assumes stats are saved for every evaluated individual in generation X in a file called "Gen_X.txt".

"""

GENS = 1000  # stop at this generation
FIT_COL = 5  # which column is fitness stored (first column is zero)?
AGE_COL = 7  # which column is age stored?
RUN_DIR = "/home/mecl/ludobots/run_50/"  # dir holding the generational data files

# get all the data files and sort them from generation 1 to GENS
all_of_gen_files = glob(RUN_DIR + "Gen_*.txt")  # each row is an individual
sorted_all_of_gen_files = sorted(all_of_gen_files)

line_hist = []
gen_age_fit_dict = {}

for gen in range(GENS+1):

    gen_age_fit_dict[gen] = {0: 0.0}

    with open(sorted_all_of_gen_files[gen], 'r') as infile:

        next(infile)  # skip header

        for line in infile:
            this_fit = float(line.split()[FIT_COL])
            this_age = int(line.split()[AGE_COL])

            if this_age not in gen_age_fit_dict[gen] or this_fit > gen_age_fit_dict[gen][this_age]:
                gen_age_fit_dict[gen][this_age] = this_fit  # most fit at each age level

    if gen > 0:

        for age in gen_age_fit_dict[gen-1]:

            if age+1 not in gen_age_fit_dict[gen] or gen == GENS:  # extinction

                this_line = []
                n = 0
                while age-n > -1:
                    this_line += [gen_age_fit_dict[gen-1-n][age-n]]
                    n += 1

                pre_fill = [None]*(gen-age)
                line_hist += [pre_fill + list(this_line[::-1])]


fig, ax = plt.subplots(1, 1, figsize=(4, 3))

for line in line_hist:
    ax.plot(range(len(line)), line, linewidth=0.8)

plt.savefig("plots/PlotName.png", dpi=300)
