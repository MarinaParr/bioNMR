import plot_hb
import hb_trace_parsing
#list_of_interesting_residues = ['GLU51', 'ASP52', 'GLY53', 'ARG54', 'GLU24', 'LYS63']
list_of_interesting_residues = ['GLU51']
#hb_trace_parsing.all_interactions("hb_trace.dat", 20)
all_inner, all_outer = hb_trace_parsing.all_interactions("hb_trace.dat", 20)
hb_trace_parsing.interesting_interactions(list_of_interesting_residues, all_inner, all_outer)
plot_hb.plotting()