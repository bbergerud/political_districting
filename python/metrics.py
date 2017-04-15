import numpy as np
import pandas as pd

class metrics:
	"""
	Functions:
		_angDist
		_assignGroup
		_updateGroup
		_updateWeights
	"""

	def _assignGroup(self):
		"""
		Function for computing the distance of each block
		unit to the center of the grouping.

		To call:
			_assignGroup()

		Parameters:
			[None]

		Postcondition
			Each block unit is assigned to the group whose weighted
			distance is the lowest value. The assigned group is
			stored in the 'group' column of the self.block_ data frame.

			If lat, lon were in degrees, these have been converted
			to radians.
		"""

		# ============================================================
		#	Check to see if lat, lon are in degrees. If so
		#	convert to radians.
		# ============================================================
		if self._deg:
			self._deg2rad()

		# ============================================================
		#	Create an array to hold the distances.
		#	There is one row for each block unit and one column
		#	for each group (cluster / district)
		# ============================================================
		dist = np.zeros((self.block_.shape[0], self.group_.shape[0]))


		# ============================================================
		#	Iterate through each group and compute the distance
		#	of each block unit from that group's centroid,
		#	multiplied by a weight.
		# ============================================================
		for group in self.group_.index:
			dist[:, group] = self.group_['alpha'][group] * \
							self._angDist(	lat1=self.block_['lat'], lon1=self.block_['lon'],
											lat2=self.group_['lat'][group], lon2=self.group_['lon'][group]	)

		# ============================================================
		#	Assign the block unit to the closest group 
		# ============================================================
		self.block_['group'] = np.argmin(dist, axis=1)
		# self.dist_ = dist


	def _angDist(self, lat1, lon1, lat2, lon2):
		"""
		Function for computing the great circle distance
		between coordinates on a sphere, minus the prefactors.
		***Assumes angles are in radians***

		To call:
			_angDist(lat1, lon1, lat2, lon2)

		Parameters:
			lat*		latitude of coordinate *
			lon*		longitude of coordinate *

		Postcondition:
			The great circle distance is returned, minus
			the prefactors.
		"""

		# ===================================================
		#	Find the difference in lat and lon, dividing
		#	by 2 for the great circle calculation
		# ===================================================
		delta_lat = 0.5 * (lat2 - lat1)
		delta_lon = 0.5 * (lon2 - lon1)

		# ===================================================
		#	Compute the angular distance on the great
		#	circle, minus the prefactors.
		# ===================================================		
		d = np.arcsin( 
			np.sqrt( 
				np.sin(delta_lat)**2 + \
				np.cos(lat1) * np.cos(lat2) * np.sin(delta_lon)**2 
			) 
		)

		return(d**2)



	def _updateGroup(self, method='area'):
		"""
		Function for computing the center of the group,
		the population in each group, as well as the
		area of each group.

		To call:
			_groupParams(method='area')

		Parameters:
			method		'area' or 'pop' centroid

		Postcondition:
			The updated statistics of the groups are
			stored in the data frame self.group_
		"""

		# ===================================================	
		#	Create lists to hold the population and center
		# ===================================================	
		groupPop  = []
		groupCen  = []
		groupArea = []


		# ===================================================	
		#	Iterate through each group
		# ===================================================	
		for group in self.group_.index:

			# ===============================================		
			#	Find the blocks that area within the group
			# ===============================================		
			loc = self.block_['group'] == group

			# ===============================================		
			#	Get the group population
			# ===============================================
			groupPop.append(
				np.sum(self.block_['pop'][loc])
			)

			# ===============================================
			#	Find the center of the group
			#		[Note this is not strictly correct as
			#		longitude becomes narrower away from
			#		the equator]
			# ===============================================
			lat = np.mean(self.block_['lat'][loc] * self.block_[method][loc]) / \
					np.mean(self.block_[method][loc]
			)
			lon = np.mean(self.block_['lon'][loc] * self.block_[method][loc]) / \
					np.mean(self.block_[method][loc])

			groupCen.append((lat, lon))

			# ===============================================
			#	Find the total area
			# ===============================================
			groupArea.append(
				np.sum(self.block_['area'][loc])
			)

		# ===================================================	
		#	Update the groups 
		#	[loc is a temporary patch in case one district
		#	loses its entire population due to the weights,
		#	and thus has no centroid]
		# ===================================================
		loc = np.isnan(groupPop) == False
	

		try:
			self.group_['pop'][loc] = groupPop[loc]
			self.group_[['lat', 'lon']][loc] = groupCen[loc]
			self.group_['area'][loc] = groupArea[loc]
		except:
			self.group_['pop'] = groupPop
			self.group_[['lat', 'lon']] = groupCen
			self.group_['area'] = groupArea



	def _updateWeights(self, itr, itrMax):
		"""
		Function for updating the weights for computing
		the weighted distance of each block from the
		group centroids.

		*** The weighting system is subject to change ***

		To call:
			_updateWeights(itr, itrMax)

		Variables:
			itr			current iteration number
			itrMax		max number of iterations

		Postcondition:
			The new weights are computed and stored in the 'alpha'
			column of the self.group_ data frame.
		"""

		# ===================================================	
		#	Compute the iteration ratio, as well as the
		#	population ratio relative to the ideal mean
		# ===================================================	
		itrRatio = itr / float(itrMax)
		popRatio = self.group_['pop'] / self.group_['pop'].mean()

		# ===================================================	
		#	Compute the new weights alpha and normalize
		# ===================================================	
		alpha = np.sqrt(itrRatio) + popRatio * np.sqrt(1 - itrRatio)
		alpha /= alpha.max()

		# ===================================================	
		#	Store the results
		# ===================================================	
		alpha = self.group_['alpha'] * np.sqrt(alpha)
		self.group_['alpha'] = alpha / alpha.max()
