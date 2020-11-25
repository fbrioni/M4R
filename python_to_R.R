library(reticulate)

#approach 1:
np <- import("numpy") #this works and I can import numpy
bayesian_indep_test <- import("bayesian_indep_test") #however I can't import my module
# Error in py_module_import(module, convert = convert) : 
#ModuleNotFoundError: No module named 'bayesian_indep_test'

#approach 2:
source_python("bayesian_indep_test.py")
#Error in py_run_file_impl(file, local, convert) : 
#Unable to open file 'bayesian_indep_test.py' (does it exist?)

x <- rnorm(1000, 0, 1)
y <- x + rnorm(1000, 0, 2)

p <- independence_tester(x, y)

