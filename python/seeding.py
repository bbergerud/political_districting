import numpy as np
import sys

class seeding:
	"""
	Class for providing the initial seeding of the districts.

	Functions:
		_randomCentroid

	Hidden Functions:
		__dfTest
	"""

	def __init__(self, *args, **kwargs):
		pass


	def __dfTest(self):
		# ===================================================
		#	Verify a census dataset has been loaded
		# ===================================================
		try:
			self.block_
		except:
			sys.exit(1)


	'''
	def _randomAssign(self, K, method='area', seed=4545):
		"""
		Randomly assigned each block to one of K districts.
		Finds the district centers by taking the geometric
		(method='geo') mean or the population (method='pop')
		mean. Note that the population mean tends to have
		worse convergence as it doesn't change much by
		adding in outlying, low-populated rural regions.

		To call:
			randomAssign(K, method='area')
	
		Parameters:
			K		number of divisions (districts)
			method	have the center weighted by geometry
					(ALAND) or population.
		"""

		# ===================================================
		#	Verify that there is a data frame
		# ===================================================
		self.__dfTest()

		# ===================================================
		#	Set the random seed
		# ===================================================
		np.random.seed(seed)

		# ===================================================
		#	Randomly assign each block to one of the K
		#	districts
		# ===================================================
		self.blocks["group"] = np.random.randint(0, K, size=self.blocks_.shape[0])

		# ===================================================
		#	Compute the district populations
		# ===================================================
		# self.group["pop"] = self.__computeDistrictPopulation()

		# ===================================================
		#	Find the district centers
		# ===================================================
		# self.__computeDistrictCenter(method=method)
	'''


	def _randomCentroid(self, K, seed=4545):
		"""
		Randomly assigns a centroid to each of the K districts.

		To call:
			_randomCentroid(K, seed)

		Parameters:
			K		number of groups / clusters
			seed	random number seed

		Postcondition:
			K groups/clusters are created with their positions
			chosen by randomly selecting the coordinates of
			one of the block units. The group information is
			stored in the data frame self.group_
		"""

		# ===================================================
		#	Verify that there is a data frame
		# ===================================================
		self.__dfTest()

		# ===================================================
		#	Set the random seed
		# ===================================================
		np.random.seed(seed)

		# ===================================================
		#	Randomly assign each block to one of the K
		#	districts
		# ===================================================
		loc = np.random.choice(self.block_.index, replace=False, size=K)
		self.group_ = self.block_.loc[loc][['lat', 'lon']].reset_index(drop=True)

		# ===================================================
		#	Create the weights for clustering
		# ===================================================
		self.group_['alpha'] = 1



