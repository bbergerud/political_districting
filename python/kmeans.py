from data import *
from seeding import *
from metrics import *
import matplotlib.pyplot as plt

class kmeans(data, seeding, metrics):
	"""
	Class for performing weighted kmeans cluster
	to group blocks into regions of approximately
	equal population.

	Functions:
		_cluster
	"""

	def __init__(self, *args, **kwargs):
		pass

	def _cluster(self, N, method='area'):
		"""
		Function for running N updates on the clustering
		"""

		# ============================================================
		#	Verify that there is a dataframe for block, group
		# ============================================================
		try:
			self.block_
			self.group_
		except:
			print('Missing a block_ or group_ data frame')
			return(None)

		# ===================================================
		#	Check that lat and lon are in radians
		# ===================================================
		if self._deg:
			self._deg2rad()


		for i in range(N):
			self._assignGroup()
			self._updateGroup(method=method)
			self._updateWeights(i+1, N)


if __name__ == '__main__':

	K = 48
	km = kmeans()
	km._loadData(id='us')
	km._randomCentroid(K=K)

	for i in range(5):
		km._simulate(50)

		colors = cm.rainbow(np.linspace(0, 1, len(km.group_.index)))
		if not km._deg:
			km._deg2rad()

		for color, group in zip(colors, km.group_.index):
			loc = km.block_['group'] == group
			plt.scatter(km.block_['lon'][loc], km.block_['lat'][loc], c=color)

		for color, group in zip(colors, km.group_.index):
			plt.scatter(km.group_['lon'][group], km.group_['lat'][group], s=150, marker='*', c='white', edgecolors=color)
		plt.show() 
