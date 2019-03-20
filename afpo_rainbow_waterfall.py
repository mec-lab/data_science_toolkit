from glob import glob
import matplotlib.pyplot as plt

RUN = 100  # only plot the ecological dynamics within this single run
GENS = 1000  # stop at this generation
FIT_COL = 5  # which column is fitness stored (first column is zero)?
AGE_COL = 7  # which column is age stored?
DPI = 300  # dots per inch
EXP_NAME = "ludobots"  # the dir name

run_directory = "/home/mecl/{0}/run_{1}/".format(EXP_NAME, RUN)  # dir holding one data file per generation
all_of_gen_files = glob(run_directory + "allIndividualsData/Gen_*.txt")  # each row is an individual (before selection)
sorted_all_of_gen_files = sorted(all_of_gen_files, reverse=False)

line_hist = []
gen_age_fit_dict = {}

for gen in range(GENS+1):

    gen_age_fit_dict[gen] = {0: 0.0}

    with open(sorted_all_of_gen_files[gen], 'r') as infile:

        next(infile)  # skip header

        for line in infile:
            this_fit = float(line.split()[FIT_COL])
            this_age = int(line.split()[AGE_COL])

            if this_age not in gen_age_fit_dict[gen] or this_fit > gen_age_fit_dict[gen][this_age]:  # ord by fit anyway
                gen_age_fit_dict[gen][this_age] = this_fit  # most fit at each age level

    if gen > 0:

        for age in gen_age_fit_dict[gen-1]:

            if age+1 not in gen_age_fit_dict[gen] or gen == 1000:  # extinction

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

plt.savefig("plots/PlotName.png", dpi=DPI)
