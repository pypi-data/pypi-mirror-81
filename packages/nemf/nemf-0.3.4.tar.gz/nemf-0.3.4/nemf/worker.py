import numpy as np
import pandas as pd
import yaml
import sys
import os

# ode solver
from scipy.integrate import solve_ivp 
# to avoid overwriting of class objects
from copy import deepcopy
# for debugging output
from termcolor import colored, cprint


# Data reading

def parse_from_excel(df):
	""" parses data from a pandas.dataframe into the correct data format 

	Takes a dataframe and returns its content as a numpy.array and its headers 
	as a list. The first column of the data frame is expected to be the 
	observation time in some timestamp format with the header 'Datetime'. It is 
	transformed into the universal posix standard.

	Parameters
	----------

	df : pandas.dataframe
		pandas data frame with column headers and the first column being 
		timestemps with the name 'Datetime'

	Returns
	-------

	da : numpy.array
		Array containing reference data.
	column_names : list of strings
		List containing the names of the columns used as compartment names.

	"""

	# headers
	
	headers = check_datetime(list(df.columns))
	
	# time column
	if np.issubdtype(df['Datetime'],np.integer):
		pass
	else:
		# turns timestamp into posix
		for ii,item in enumerate(df['Datetime']):
			df['Datetime'][ii] = item.timestamp()
		
	da = np.array(df)
	return da, headers

def check_datetime(headers):
	if headers[0] != 'Datetime':
		print("Warning! First Column is not 'Datetime'."
			  + "Is the first (datetime) column of the reference data "
			  + "formated correctly?" )
	return headers


def import_ref_from_excel(path):
	""" Uses pandas to import data from excel file and return it as a np.array

	Parameters
	----------

	path : string
		path pointing to the file

	Returns
	-------

	da : numpy.array
		Array containing reference data.
	column_names : list of strings
		List containing the names of the columns used as compartment names.

	"""

	df = pd.read_excel(path)
	da, names = parse_from_excel(df)
	return da, names


def import_ref_from_csv(path,**kwargs):

	if 'delimiter' in list(kwargs):
		if 'skip_header' in list(kwargs):
			n_header = kwargs.pop('skip_header')
			data = np.genfromtxt(path,
				skip_header=1+n_header,**kwargs,)
			names = np.genfromtxt(path,
				names=True,
				delimiter=',',
				skip_header=n_header,**kwargs).dtype.names
		else:	
			data = np.genfromtxt(path,
				skip_header=1,**kwargs,)
			names = np.genfromtxt(path,
				names=True,
				delimiter=',',**kwargs).dtype.names
	else:
		if 'skip_header' in list(kwargs):
			n_header = kwargs.pop('skip_header')
			data = np.genfromtxt(path,
				skip_header=1+n_header,
				delimiter=',',**kwargs)
			names = np.genfromtxt(path,
				names=True,
				skip_header=n_header,
				delimiter=',',**kwargs).dtype.names
		else:	
			data = np.genfromtxt(path,
				skip_header=1,
				delimiter=',',**kwargs)
			names = np.genfromtxt(path,
				names=True,
				delimiter=',',**kwargs).dtype.names
	
	names = check_datetime(names)
	
	return data, names


def import_reference_data(path,**kwargs):
	""" Main function to import reference data of different formats.


	Parameters
	----------

	path : string
		path pointing to the file
	args : list of arguments
		arguments passed to the respective import function depending on its 
		file type

	Returns
	-------

	da : numpy.array
		Array containing reference data.
	column_names : list of strings
		List containing the names of the columns used as compartment names.

	"""
	file_suffix = path.split('.')[-1]
	excel_suffixes = ['xls','xlsx']
	if file_suffix in excel_suffixes:
		# excel import
		da, names = import_ref_from_excel(path,**kwargs)
	else:
		# numpy import
		da, names = import_ref_from_csv(path,**kwargs)
		
	return da, names


def read_coeff_yaml(path):
	"Reads a yaml file and returns its as a dictionary"
	
	fo = open(path,'r')
	stream = fo.read()
	data_dict = yaml.safe_load(stream)
	
	return data_dict


def import_constraints(path):
	""" Import constraints from a python file 
	
	The file at the end of path needs to contain a variable named
	constraints that contains the constraints.
	
	Parameters
	----------
	
	path : string
		path to file.py containing the constraints definition
		
	Returns
	-------

	constraints : list or scipy constraints type 
		containts all contraints that shall be used in the model
	"""

	path = os.path.abspath(path)
	sys.path.insert(0,path)
	file_name = os.path.basename(path)
	# strip extension
	file_name = file_name[:-3]
	module = __import__(file_name)
	constraints = module.constraints

	return constraints



# Parsers

def initialize_ode_system(path_config):
	""" Initializes the dictionary containing the 'state' and 'interactions'

	Parameters
	----------
	path_config : string
		Path to the yaml file containing the ode model configuration.
		The configuration contains the compartments, initial values
		and optimization constrains - as well as - interactions paths, 
		interaction directions (sign),interaction functions,
		initial parameter values and optimization constrains.

	Returns
	-------
	ode_system_configuration : dict
		Contains the state and interaction configuration
		in a similar structure as provided by the yaml files.
		
	"""

	system_config = read_coeff_yaml(path_config)

	return system_config


# Gradient Decent

## Cost function related Methods
def cost_function(prediction,y):
	""" normalized squared distance between model prediction and
		desired model behavior 
		
		Parameters
		----------
		prediction : numpy.array
			1D-array contains the output of the fit model which
			ran the time integration
		y : numpy.array
			1D-array,same length as prediction containing the desired
			model output.
			
		Returns
		-------
		cost : float
			contains the value of the cost function for the given prediction
			and desired state"""


	cost = (1/len(y))*np.sum( (prediction - y)**2 )
	return cost


## Gradient Decent related Helper Functions

def update_param(initial_param, fit_param, fit_idx):

	# states
	fit_states = fit_param[:len(fit_idx[0])]
	states_t0 = deepcopy(initial_param[0])
	for [idx,item] in zip(fit_idx[0],fit_states):
		states_t0[idx] = item
	
	# args
	fit_args = fit_param[len(fit_idx[0]):]
	args = deepcopy(initial_param[1])
	
	for [idx,item] in zip(fit_idx[1],fit_args):
		args[idx[0]][idx[1]][idx[2]] = item
	
	return [states_t0,args]


def construct_objective(model,method='Radau',time_series_events=None,
						debug=False):
	
	differential_equation = model.de_constructor()
	fit_indices = model.fetch_to_optimize_args()[0][0]
	initial_param = model.fetch_param()
	ref_data, idx_refed_compart = model.prep_ref_data()
	t_eval = ref_data[:,0]

	# steady-state solution
	if t_eval[0] == np.inf:
		if debug: cprint('steady_state objective','magenta')		
		t_min = 0
		t_max = model.configuration['time_evo_max']
		t_span = [t_min,t_max]
		if debug: 
			cprint(f't_span: ','magenta')
			print(t_span)
			cprint(f't_eval: ','magenta')
			print(t_eval)
		y = ref_data[:,1:]

		def objective(fit_param):
			
			updated_param = update_param(initial_param,fit_param,fit_indices)
			y0 = updated_param[0]
			args = [updated_param[1]]
			if debug:
				cprint(f'initial_param: ','magenta')	
				print(initial_param)
				cprint(f'updated_param: ','magenta')
				print(updated_param)
			ode_sol = solve_ivp(differential_equation,t_span,y0,
								method=method,args=args,dense_output=True,
								events=time_series_events)
		   

			x = ode_sol.sol(t_span[1]).T
			x = np.reshape(x,(1,len(x)))
			x = x[:,idx_refed_compart]
			res = np.linalg.norm(x-y)**2
			if debug:
				cprint(f'solution(time integration): ','magenta')
				print(x)
				cprint(f'solution(reference data): ','magenta')
				print(y)
				cprint(f'objective function: ','magenta')
				print(res)
			return res

	# non-steady-state solution
	else:
		if debug: cprint('non_steady_state objective','magenta')		

		t_min = t_eval[0]
		t_max = t_eval[-1]
		t_span = [t_min,t_max]
		if debug: 
			cprint(f't_span: ','magenta')
			print(t_span)
			cprint(f't_eval: ','magenta')
			print(t_eval)
		y = ref_data[:,1:]
		
		def objective(fit_param):
			
			updated_param = update_param(initial_param,fit_param,fit_indices)
			y0 = updated_param[0]
			args = [updated_param[1]]
			if debug:
				cprint(f'fit_param: ','magenta')
				print(fit_param)
				cprint(f'fit_indices: ','magenta')
				print(fit_indices)
				cprint(f'initial_param: ','magenta')
				print(initial_param)
				cprint(f'updated_param: ','magenta')
				print(updated_param)
	
			ode_sol = solve_ivp(differential_equation,t_span,y0,
								method=method,args=args,dense_output=True, 
								t_eval=t_eval)
		   
			x = ode_sol.sol(t_eval).T
			x = x[:,idx_refed_compart]
			res = np.linalg.norm(x-y)**2
			if debug:
				cprint(f'solution(time integration): ','magenta')
				print(x)
				cprint(f'solution(reference data): ','magenta')
				print(y)
				cprint(f'objective function: ','magenta')
				print(res)
				
			return res
		
	return objective


def perturb(x,pert_scale=1e-4):
	"Adds a small perturbation to input (1D-)array"
	
	delta_x = (np.random.rand(len(x)) - 0.5)*pert_scale
	
	return x+delta_x


def read_coeff_constrains(path):
	""" reads the constrains of the ODE coefficients from file """
	constrains = np.genfromtxt(path)
	lower = constrains[:,::2]
	upper = constrains[:,1::2]

	free_coeff = np.where( ((lower != 0) + (upper != 0)) *
			  ((lower != -1) + (upper != -1)) *
			  ((lower != 1) + (upper != 1)) )

	lower = lower[free_coeff]
	upper = upper[free_coeff]

	lower = np.reshape(lower, (len(lower),))
	upper = np.reshape(upper, (len(upper),))

	constrains = np.stack((lower,upper),axis=1)
	
	return constrains,free_coeff


def monte_carlo_sample_generator(constrains):
	""" Creates randomly distributed samples inside the constraints

	Constructs a set of homogenously distributed random values 
	in the value range provided by 'constrains'.
	Returns an array of the length of 'constrains' 
	Caution: Samples the FULL float search space if an inf value is provided! 
		
	Parameters
	----------
	constrains : numpy.array
		2D-array containing the upper and lower limit of every free input
		parameter in the shape (len(free_param),2).
		
	Returns
	-------
	sample_set : numpy.array 
		1D-array containing a random vector in the range of constrains """

	""" returns min/max possible value if a +/- infinite value is pressent """
	constrains[constrains==np.inf] = np.finfo(float).max
	constrains[constrains==-np.inf] = np.finfo(float).min

	constrains_width = constrains[:,1] - constrains[:,0]
	sample_set = constrains_width*np.random.rand(len(constrains))+constrains[:,0]

	return sample_set


# checks to test if element in dict is defined

def assert_if_exists(unit,container,item='',reference='',
								name="Model configuration "):
	assert (unit in container), \
		name + reference + " {} lacks definition of {}".format(item,unit)

def assert_if_non_empty(unit,container,item='',reference='',
								name="Model configuration "):
	assert (container[unit] != None), \
		name + reference + " {} {} is empty".format(item,unit)

def assert_if_exists_non_empty(unit,container,item='',reference='',
								name="Model configuration "):
	assert_if_exists(unit,container,item,reference=reference,name=name)
	assert_if_non_empty(unit,container,item,reference=reference,name=name)
