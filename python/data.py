import pandas as pd
import numpy as np
import sys, us

class data:
	"""
	Class for loading the dataset.

	Functions:
		_loadData
		_deg2rad
		_rad2deg
	"""
	def __init__(self, *args, **kwargs):
		pass

	def _loadData(self, fn='../census/usa.txt', id='IA', L48=False, DC=True):
		"""
		Function that loads the dataset into a pandas dataframe
		and selects a subset that follow the id (state initials).

		Use 'usa' / 'us' if wanting to use the whole dataset, or
		a list of ids ['IA', 'MN'] to combine multiple states. If
		wanting to exclude AK and HW, then set L48 to True. If
		also wanting to exclude DC, then set DC to False.

		To call:
			_loadData(fn, id, L48=False, DC=True)

		Parameters:
			fn		filename of dataset
			id		state(s) identifier
			L48		(boolean) use only lower 48 states (+DC)
			DC		(boolean) include DC

		Postcondition:
			GEOID_1, INTPTLAT, INTPTLON, ALAND, B01001e1, STATEFP
			have been extracted from the csv file. STATEPF is 
			converted to the appropriate abbreviation. These variables
			are then renamed as [id, lat, lon, area, pop, state] and
			stored in a pandas dataframe self.block_, which contains
			only the block units whose 'state' column matches the
			chosen id(s).
		"""

		# =========================================================
		#	Attempt to load in the dataset
		# =========================================================
		try:
			block = pd.read_csv(fn)
		except:
			print('Failed to load datafile: {:s}. Aborting'.format(fn))
			sys.exit(1)

		# =========================================================
		#	Keep only the necessary columns
		# =========================================================

		block = block[['GEOID_1', 'INTPTLAT', 'INTPTLON', 'ALAND', 'B01001e1', 'STATEFP']]
		block.columns = ['id', 'lat', 'lon', 'area', 'pop', 'state']

		# =========================================================
		#	Converts FIPS number to state ABBR
		# =========================================================		
		for state in set(block.state):
			if state < 10:
				s = '0' + str(state)
			else:
				s = str(state)

			s = us.states.lookup(s)
			block['state'][block['state'] == state] = s.abbr

		# =========================================================		
		#	If id = 'usa' | 'us', then remove the territories
		#	and check the other input conditions.
		# =========================================================	
		if id in ['usa', 'us', 'USA', 'US']:
			
			# =====================================================
			#	Get the territory abbeviations for removing
			#	from the data frame
			# =====================================================
			territories = us.states.TERRITORIES
			territories = [t.abbr for t in territories]

			# =====================================================
			#	Test to see if Alaska, Hawaii, and DC should
			#	be removed
			# =====================================================
			if L48: territories.extend(['AK', 'HI'])
			if not DC: territories.append('DC')

			# =====================================================
			#	Remove the specified areas
			# =====================================================
			block = block[~block.state.isin(territories)].reset_index(drop=True)
	
		else:
			
			# =========================================================		
			#	If id is a string, insert into a list for subsetting
			# =========================================================
			if isinstance(id, str):
				id = [id]

			block = block[block.state.isin(id)].reset_index(drop=True)


		# =========================================================
		#	Store the data frame
		# =========================================================
		self.block_ = block
		self._deg = True			# For tracking the units of lat/lon


	def _deg2rad(self):
		"""
		Function for converting the latitude and longitude to radians.

		To call:
			_deg2rad()

		Parameters:
			[None]

		Postcondition:
			If lat/lon are currently in degrees, then there are 
			converted to radians.
		"""
		# =========================================================
		#	Number of radians in a degree
		# =========================================================
		deg2rad = np.pi / 180.

		# =========================================================
		#	Convert from deg to radians
		# =========================================================
		if self._deg:

			self.block_[['lat', 'lon']] *= deg2rad

			try: self.group_[['lat', 'lon']] *= deg2rad
			except: print('Warning: no group object; _deg2rad [if]')

			self._deg = False


	def _rad2deg(self):
		"""
		Function for converting the latitude and longitude to degrees.

		To call:
			_rad2deg()

		Parameters:
			[None]

		Postcondition:
			If lat/lon are currently in radians, then there are 
			converted to degrees.
		"""
		# =========================================================
		#	Number of degrees in a radian
		# =========================================================
		rad2deg = 180. / np.pi

		# =========================================================
		#	Convert from radians to deg
		# =========================================================
		if not self._deg:

			self.block_[['lat', 'lon']] *= rad2deg
			try: self.group_[['lat', 'lon']] *= rad2deg
			except: print('Warning: no group object; _deg2rad [else]')

			self._deg = True


if __name__ == '__main__':

	cn = data()
	cn._loadData(id=['IA'])
	print(cn.block_.head())
