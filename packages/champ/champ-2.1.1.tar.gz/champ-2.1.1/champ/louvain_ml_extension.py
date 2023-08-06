#Py 2/3 Compatibility
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division # use // to specify int div.
from future.utils import iteritems,iterkeys
from future.utils import lmap

import gzip
import sys, os
import re
import tempfile
from contextlib import contextmanager
from multiprocessing import Pool,cpu_count
from time import time
import itertools
from .champ_functions import get_intersection
from .champ_functions import create_coefarray_from_partitions
from .louvain_ext import *
import matplotlib.lines as mlines
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from matplotlib import rc
import igraph as ig
import louvain
import numpy as np
import h5py
import sklearn.metrics as skm
from time import time
import logging
logging.basicConfig(format=':%(asctime)s:%(levelname)s:%(message)s', level=logging.DEBUG)

class MultiLayerPartitionEnsemble():

	'''Group of partitions of a multilayer graph stored in membership vector format

	The attribute for each partition is stored in an array and can be indexed

	:cvar graph: The graph associated with this PartitionEnsemble.  Each ensemble \
	can only have a single graph and the nodes on the graph must be orded the same as \
	each of the membership vectors.
	:type graph: igraph.Graph

	:cvar partitions:  of membership vectors for each partition.  If h5py is set this is a dummy \
	variable that allows access to the file, but never actually hold the array of parititons.
	:type partitions:  np.array
	:cvar int_edges:  Number of edges internal to the communities
	:type int_edges:  list

	:cvar exp_edges:  Number of expected edges (based on configuration model)
	:type exp_edges:  list

	:cvar resoltions:  If partitions were idenitfied with Louvain, what resolution \
	were they identified at (otherwise None)
	:type resolutions: list

	:cvar orig_mods:  Modularity of partition at the resolution it was identified at \
	if Louvain was used (otherwise None).
	:type orig_mods: list

	:cvar numparts: number of partitions
	:type numparts: int
	:cvar ind2doms: Maps index of dominant partitions to boundary points of their dominant \
	domains
	:type ind2doms: dict
	:cvar ncoms: List with number of communities for each partition
	:type numcoms: list
	:cvar min_com_size: How many nodes must be in a community for it to count towards the number \
	of communities.  This eliminates very small or unstable communities.  Default is 5
	:type min_com_size: int
	:cvar unique_partition_indices: The indices of the paritions that represent unique coefficients.  This will be a \
	subset of all the partitions.
	:cvar hdf5_file: Current hdf5_file.  If not None, this serves as the default location for loading and writing \
	partitions to, as well as the default location for saving.
	:type hdf5_file: str
	:type unique_partition_indices: np.array
	:cvar twin_partitions:  We define twin partitions as those that have the same coefficients, but are actually \
	different partitions.  This and the unique_partition_indices are only calculated on demand which can take some time.
	:type twin_partitions: list of np.arrays
	'''


	def __init__(self,intra_graph=None,inter_graph=None,layer_vec=None,
				 listofparts=None,name='unnamed_graph',maxpt=None,min_com_size=5):

		self._hdf5_file=None
		self.int_edges = np.array([])
		self.int_inter_edges = np.array([])
		self.exp_edges = np.array([])
		self.resolutions = np.array([])
		self.couplings = np.array([])
		self.numcoms=np.array([])
		self.orig_mods = np.array([])
		self.numparts=0
		self.intra_graph = intra_graph
		self.inter_graph = inter_graph
		self.layer_vec = layer_vec

		self.min_com_size=min_com_size
		self.maxpt=maxpt
		#some private variable
		self._partitions=np.array([])
		self._uniq_coeff_indices=None
		self._uniq_partition_indices=None
		self._twin_partitions=None
		self._sim_mat=None

		if listofparts!=None:
			self.add_partitions(listofparts,maxpt=self.maxpt)
		self.name=name


	def get_adjacency(self,intra=True):
		'''
		Calc adjacency representation if it exists
		:param intra: return intralayer adjacency.  If false returns interlayer adj.
		:return: self.adjacency

		'''
		if intra:
			if 'intra_adj'  not in self.__dict__:
				if 'weight' in self.intra_graph.edge_attributes():
					self.intra_adj=self.intra_graph.get_adjacency(type="GET_ADJACENCY_BOTH",
														attribute='weight')
				else:
					self.intra_adj = self.intra_graph.get_adjacency(type="GET_ADJACENCY_BOTH")
			return self.intra_adj
		else:
			if 'inter_adj'  not in self.__dict__:
				if 'weight' in self.inter_graph.edge_attributes():
					self.intra_adj=self.inter_graph.get_adjacency(type="GET_ADJACENCY_BOTH",
														attribute='weight')
				else:
					self.intra_adj = self.inter_graph.get_adjacency(type="GET_ADJACENCY_BOTH")
			return self.inter_adj

	def calc_internal_edges(self,memvec,intra=True):
		'''
		Uses igraph Vertex Clustering representation to calculate internal edges.  see \
		:meth:`louvain_ext.get_expected_edges`

		:param memvec: membership vector for which to calculate the internal edges.
		:param intra: boolean indicating whether to calculate intralayer edges that are \
		internal (True) or interlayer edges that are internal to communities (False).
		:type memvec: list

		:return:

		'''
		# if "weight" in self.graph.edge_attributes():
		#	 adj=self.graph.get_adjacency(attribute='weight')
		if intra:
			partobj = ig.VertexClustering(graph=self.intra_graph, membership=memvec)
			weight = "weight" if "weight" in self.intra_graph.edge_attributes() else None
		else:
			partobj = ig.VertexClustering(graph=self.inter_graph, membership=memvec)
			weight = "weight" if "weight" in self.intra_graph.edge_attributes() else None

		return get_sum_internal_edges(partobj=partobj,weight=weight)

	def calc_expected_edges(self, memvec):
		'''
		Uses igraph Vertex Clustering representation to calculate expected edges for \
		each layer within the graph.
		:meth:`louvain_ext.get_expected_edges`

		:param memvec: membership vector for which to calculate the expected edges
		:type memvec: list
		:return: expected edges under null
		:rtype: float

		'''

		#create temporary VC object
		partobj=ig.VertexClustering(graph=self.intra_graph,membership=memvec)
		weight = "weight" if "weight" in self.intra_graph.edge_attributes() else None
		Phat=get_expected_edges_ml(partobj,self.layer_vec,weight=weight)
		return Phat


	def __getitem__(self, item):
		'''
		List of paritions in the PartitionEnsemble object can be indexed directly

		:param item: index of partition for direct access
		:type item: int
		:return: self.partitions[item]
		:rtype:  membership vector of community for partition
		'''
		return self.partitions[item]

	class _PartitionOnFile():

		def __init__(self,file=None):
			self._hdf5_file=file

		def __getitem__(self, item):
			with h5py.File(self._hdf5_file, 'r') as openfile:
				try:
					return  openfile['_partitions'].__getitem__(item)
				except TypeError:
					#h5py has some controls on what can be used as a slice object.
					return  openfile['_partitions'].__getitem__(list(item))


		def __len__(self):
			with h5py.File(self._hdf5_file, 'r') as openfile:
				return  openfile['_partitions'].shape[0]

		def __str__(self):
			return "%d partitions saved on %s" %(len(self),self._hdf5_file)

	@property
	def partitions(self):
		'''Type/value of partitions is defined at time of access. If the PartitionEnsemble\
		has an associated hdf5 file (PartitionEnsemble.hdf5_file), then partitions will be \
		read and added to on the file, and not as an object in memory.'''

		if not self._hdf5_file is None:

			return PartitionEnsemble._PartitionOnFile(file=self._hdf5_file)

		else:
			return self._partitions

	@property
	def hdf5_file(self):
		'''Default location for saving/loading PartitionEnsemble if hdf5 format is used.  When this is set\
		it will automatically resave the PartitionEnsemble into the file specified.'''
		return self._hdf5_file

	@hdf5_file.setter
	def hdf5_file(self,value):
		'''Set new value for hdf5_file and automatically save to this file.'''
		self._hdf5_file=value
		self.save()


	def _check_lengths(self):
		'''
		check all state variables for equal length.  Will use length of partitions stored \
		in the hdf5 file if this is set for the PartitionEnsemble.  Otherwise just uses \
		internal lists.

		:return: boolean indicating states varaible lengths are equal

		'''
		if not self._hdf5_file is None:
			with h5py.File(self._hdf5_file) as openfile:
				if openfile['_partitions'].shape[0] == len(self.int_edges) and \
					openfile['_partitions'].shape[0] == len(self.resolutions) and \
					openfile['_partitions'].shape[0] == len(self.exp_edges) and \
					openfile['_partitions'].shape[0] == len(self.couplings):
					return True
				else:
					return False

		if self.partitions.shape[0]==len(self.int_edges) and \
				self.partitions.shape[0] == len(self.int_inter_edges) and \
				self.partitions.shape[0]==len(self.resolutions) and \
				self.partitions.shape[0]==len(self.exp_edges):
			return True
		else:
			return False


	def _combine_partitions_hdf5_files(self,otherfile):
		if self._hdf5_file is None or otherfile is None:
			raise IOError("PartitionEnsemble does not have hdf5 file currently defined")

		with h5py.File(self._hdf5_file,'a') as myfile:
			with h5py.File(otherfile,'r') as file_2_add:

				for attribute in ['_partitions', 'resolutions','couplings', 'orig_mods', "int_edges","int_inter_edges", 'exp_edges']:
					cshape=myfile[attribute].shape
					oshape=file_2_add[attribute].shape
					newshape=(cshape[0]+oshape[0],cshape[1]+oshape[1])
					myfile[attribute].resize(newshape[0],newshape[1])
					myfile[attribute][cshape[0]:newshape[0],cshape[1]:newshape[1]]=file_2_add[attribute]

	def _append_partitions_hdf5_file(self,partitions):
		'''

		:param partitions: list of partitions (in dictionary) to add to the PartitionEnsemble.

		:type partitions: dict

		'''
		with h5py.File(self._hdf5_file,'a') as openfile:
			#Resize all of the arrays in the file
			orig_shape=openfile['_partitions'].shape
			for attribute in ['_partitions','resolutions','couplings','orig_mods',"int_edges","int_inter_edges",'exp_edges']:
				cshape=openfile[attribute].shape
				if len(cshape)==1:
					openfile[attribute].resize( (cshape[0]+len(partitions),) )
				else:
					openfile[attribute].resize((cshape[0] + len(partitions), cshape[1]))

			for i,part in enumerate(partitions):

				cind=orig_shape[0]+i

				#We store these on the file
				openfile['_partitions'][cind]=np.array(part['partition'])

				#We leave the new partitions only in the file.  Everything else is updated \
				# in both the PartitionEnsemble and the file

				if 'resolution' in part:
					self.resolutions=np.append(self.resolutions,part['resolution'])
					openfile['resolutions'][cind]=part['resolution']
				else:
					self.resolutions=np.append(self.resolutions,None)
					openfile['resolutions'][cind]=None

				if 'coupling' in part:
					self.resolutions = np.append(self.resolutions, part['coupling'])
					openfile['couplings'][cind] = part['coupling']
				else:
					self.resolutions = np.append(self.resolutions, None)
					openfile['resolutions'][cind] = None

				#internal intra edges
				if 'int_edges' in part:
					self.int_edges=np.append(self.int_edges,part['int_edges'])
					openfile['int_edges'][cind]=part['int_edges']
				else:
					cint_edges = self.calc_internal_edges(part['partition'],intra=True)
					self.int_edges=np.append(self.int_edges,cint_edges)
					openfile['int_edges'][cind]=cint_edges

				#internal inter edges
				if 'int_inter_edges' in part:
					self.int_edges=np.append(self.int_edges,part['int_inter_edges'])
					openfile['int_inter_edges'][cind]=part['int_inter_edges']
				else:
					cinter_edges = self.calc_internal_edges(part['partition'],intra=False)
					self.int_inter_edges=np.append(self.int_inter_edges,cinter_edges)
					openfile['int_inter_edges'][cind]=cinter_edges

				if 'exp_edges' in part:
					self.exp_edges=np.append(self.exp_edges,part['exp_edges'])
					openfile['exp_edges'][cind]=part['exp_edges']
				else:
					cexp_edges = self.calc_expected_edges(part['partition'])
					self.exp_edges=np.append(self.exp_edges,cexp_edges)
					openfile['exp_edges'][cind]=cexp_edges

				if "orig_mod" in part:
					self.orig_mods=np.append(self.orig_mods,part['orig_mod'])
					openfile['orig_mods'][cind]=part['orig_mod']
				elif not self.resolutions[-1] is None:
					# calculated original modularity from orig resolution
					corigmod=self.int_edges[-1] - self.resolutions[-1] * self.exp_edges
					self.orig_mods=np.append(self.orig_mods,corigmod)
					openfile['orig_mods'][cind]=corigmod
				else:
					openfile['orig_mods'][cind]=None
					self.orig_mods=np.append(self.orig_mods,None)

			self.numparts=openfile['_partitions'].shape[0]
		assert self._check_lengths()


	def add_partitions(self,partitions,maxpt=None):
		'''
		Add additional partitions to the PartitionEnsemble object. Also adds the number of \
		communities for each.  In the case where PartitionEnsemble was openned from a file, we \
		just appended these and the other values onto each of the files.  Partitions are not kept \
		in object, however the other partitions values are.

		:param partitions: list of partitions to add to the PartitionEnsemble
		:type partitions: dict,list

		'''

		#wrap in list.
		if not hasattr(partitions,'__iter__'):
			partitions=[partitions]

		if self._hdf5_file is not None:
			# essential same as below, but everything is written to file and partitions \
			#aren't kept in object memory
			self._append_partitions_hdf5_file(partitions)



		else:
			for part in partitions:

				#make sure this private variable is set
				if len(self._partitions)==0:
					self._partitions=np.array([part['partition']])
				else:
					self._partitions=np.append(self._partitions,[part['partition']],axis=0)

				if 'resolution' in part:
					self.resolutions=np.append(self.resolutions,part['resolution'])
				else:
					self.resolutions=np.append(self.resolutions,None)

				if 'int_edges' in part:
					self.int_edges=np.append(self.int_edges,part['int_edges'])
				else:
					cint_edges=self.calc_internal_edges(part['partition'])
					self.int_edges=np.append(self.int_edges,cint_edges)

				if 'exp_edges' in part:
					self.exp_edges=np.append(self.exp_edges,part['exp_edges'])
				else:
					cexp_edges=self.calc_expected_edges(part['partition'])
					self.exp_edges=np.append(self.exp_edges,cexp_edges)

				if "orig_mod" in part:
					self.orig_mods=np.append(self.orig_mods,part['orig_mod'])
				elif not self.resolutions[-1] is None:
					#calculated original modularity from orig resolution
					self.orig_mods=np.append(self.orig_mods,self.int_edges[-1]-self.resolutions[-1]*self.exp_edges)
				else:
					self.orig_mods=np.append(self.orig_mods,None)



				self.numcoms=np.append(self.numcoms,get_number_of_communities(part['partition'],
															  min_com_size=self.min_com_size))

				assert self._check_lengths()
				self.numparts=len(self.partitions)
			#update the pruned set
		self.apply_CHAMP(maxpt=self.maxpt)
		self.sim_mat #set the sim_mat

	def get_champ_gammas(self):
		'''
		Return the first coordinate for each range in the dominante domain, sorted by increasing gamma
		:return: sorted list
		'''
		allgams = sorted(set([pt[0] for pts in self.ind2doms.values() for pt in pts]))
		return allgams

	def get_broadedst_domains(self, n=4):
		'''
		Return the starting $\gamma$ for the top n domains by the length of the domain \
		(i.e. $\gamma_{i+1}-\gamma_{i}$)

		:param n: number of top starting values to return
		:return: list of n $\gamma$ values
		'''
		prune_gammas=self.get_champ_gammas()
		gam_ind = zip(np.diff(prune_gammas), range(len(prune_gammas) - 1))
		gam_ind.sort(key=lambda x: x[0], reverse=True)
		return [(prune_gammas[gam_ind[i][1]], gam_ind[i][0]) for i in range(n)]

	def get_partition_dictionary(self, ind=None):
		'''
		Get dictionary representation of partitions with the following keys:

			'partition','resolution','orig_mod','int_edges','exp_edges'

		:param ind: optional indices of partitions to return.  if not supplied all partitions will be returned.
		:type ind: int, list
		:return: list of dictionaries

		'''

		if ind is not None:
			if not hasattr(ind,"__iter__"):
				ind=[ind]
		else: #return all of the partitions
			ind=range(len(self.partitions))

		outdicts=[]

		for i in ind:
			cdict={"partition":self.partitions[i],
				   "int_edges":self.int_edges[i],
				   "exp_edges":self.exp_edges[i],
				   "resolution":self.resolutions[i],
				   "orig_mod":self.orig_mods[i]}
			outdicts.append(cdict)

		return outdicts

	def merge_ensemble(self,otherEnsemble,new=True):
		'''
		Combine to PartitionEnsembles.  Checks for concordance in the number of vertices. \
		Assumes that internal ordering on the graph nodes for each is the same.

		:param otherEnsemble: otherEnsemble to merge
		:param new: create a new PartitionEnsemble object? Otherwise partitions will be loaded into \
		the one of the original partition ensemble objects (the one with more partitions in the first place).
		:type new: bool
		:return:  PartitionEnsemble reference with merged set of partitions

		'''

		if not self.graph.vcount()==otherEnsemble.graph.vcount():
			raise ValueError("PartitionEnsemble graph vertex counts do not match")

		if new:
			bothpartitions=self.get_partition_dictionary()+otherEnsemble.get_partition_dictionary()
			return PartitionEnsemble(self.graph,listofparts=bothpartitions)

		else:
			if self.numparts<otherEnsemble.numparts:
				#reverse order of merging
				return otherEnsemble.merge_ensemble(self,new=False)
			else:
				if not self._hdf5_file is None and not otherEnsemble.hdf5_file is None:
					#merge the second hdf5_file onto the other and then reopen it to
					#reload everything.
					self._combine_partitions_hdf5_files(otherEnsemble.hdf5_file)
					self.open(self._hdf5_file)
					return self
				else:
					self.add_partitions(otherEnsemble.get_partition_dictionary())
					return self

	def get_coefficient_array(self):
		'''
		Create array of coefficents for each partition.

		:return: np.array with coefficents for each of the partions

		'''

		outlist=np.array([[self.int_edges[0],
				self.exp_edges[0]]])

		for i in range(1,self.numparts):
			outlist=np.append(
				outlist,[[
				self.int_edges[i],
				self.exp_edges[i]
			]],axis=0)

		return outlist

	@property
	def unique_coeff_indices(self):
		if self._uniq_coeff_indices is None:
			self._uniq_coeff_indices=self.get_unique_coeff_indices()
			return self._uniq_coeff_indices

	@property
	def unique_partition_indices(self):
		if self._uniq_partition_indices is None:
			self._twin_partitions,self._uniq_partition_indices=self._get_unique_twins_and_partition_indices()
		return self._uniq_partition_indices

	@property
	def twin_partitions(self):
		'''
		We define twin partitions as those that have the same coefficients but are different partitions.\
		To find these we look for the diffence in the partitions with the same coefficients.

		:return: List of groups of the indices of partitions that have the same coefficient but \
		are non-identical.
		:rtype: list of list (possibly empty if no twins)
		'''

		if self._twin_partitions is None:
			self._twin_partitions,self._uniq_partition_indices=self._get_unique_twins_and_partition_indices()
		return self._twin_partitions

	@property
	def sim_mat(self):
		if self._sim_mat is None:
			sim_mat = np.zeros((len(self.ind2doms), len(self.ind2doms)))
			for i in range(len(self.ind2doms)):
				for j in range(i,len(self.ind2doms)):
					partition1 = self.partitions[i]
					partition2 = self.partitions[j]

					sim_mat[i][j] = skm.adjusted_mutual_info_score(partition1,
															   partition2,average_method='max')
					sim_mat[j][i] = sim_mat[j][i]
			self._sim_mat=sim_mat
		return self._sim_mat


	def get_unique_coeff_indices(self):
		''' Get the indices for the partitions with unique coefficient \
		 :math:`\\hat{A}=\\sum_{ij}A_{ij}` \
		 :math:`\\hat{P}=\\sum_{ij}P_{ij}`

		 Note that for each replicated partition we return the index of one (the earliest in the list) \
		 the replicated

		:return: the indices of unique coeficients
		:rtype: np.array
		'''
		_,indices=np.unique(self.get_coefficient_array(),return_index=True,axis=0)
		return indices

	def _reindex_part_array(self,part_array):
		'''we renumber partitions labels to ensure that each goes from number 0,1,2,...
		in order to compare.

		:param part_array:
		:type part_array:
		:return: relabeled array
		:rtype:
		'''
		out_array=np.zeros(part_array.shape)
		for i in range(part_array.shape[0]):
			clabdict={}
			for j in range(part_array.shape[1]):
				#Use len of cdict as value
				clabdict[part_array[i][j]]=clabdict.get(part_array[i][j],len(clabdict))

			for j in range(part_array.shape[1]):
				out_array[i][j]=clabdict[part_array[i][j]]

		return out_array


	def _get_unique_twins_and_partition_indices(self, reindex=True):
		'''
		Returns the (possibly empty) list of twin partitions and the list of unique partitions.

		:param reindex: if True, will reindex partitions that it is comparing to ensure they are unique under \
		permutation.
		:return: list of twin partition (can be empty), list of indicies of unique partitions.
		:rtype: list,np.array
		'''
		uniq,index,reverse,counts=np.unique(self.get_coefficient_array(),
											return_index=True,return_counts=True,
											return_inverse=True,axis=0)

		ind2keep=index[np.where(counts==1)[0]]
		twin_inds=[]

		for ind in np.where(counts>1)[0]:
			#we have to load the partitions and compare them to each other
			revinds=np.where(reverse==ind)[0]
			parts2comp=self.partitions[np.where(reverse==ind)[0]]
			if reindex:
				reindexed_parts2comp=self._reindex_part_array(parts2comp)
			else:
				reindexed_parts2comp=parts2comp

			#here curpart inds is which of of this current group of partitions are unique
			_,curpart_inds=np.unique(reindexed_parts2comp,axis=0,return_index=True)
			#len of curpart_inds determines how many of the current ind group get added to
			#the ind2keep.  should always be at least one.
			if len(curpart_inds)>1: #matching partitions with different coeffs
				twin_inds.append(revinds[curpart_inds])
			ind2keep=np.append(ind2keep,revinds[curpart_inds])

		np.sort(ind2keep)
		return  twin_inds,ind2keep

	def get_unique_partition_indices(self,reindex=True):
		'''
	   This returns the indices for the partitions who are unique.  This could be larger than the
	   indices for the unique coeficient since multiple partitions can give rise to the same coefficient. \
	   In practice this has been very rare.  This function can take sometime for larger network with many \
	   partitions since it reindex the partitions labels to ensure they aren't permutations of each other.

	   :param reindex: if True, will reindex partitions that it is comparing to ensure they are unique under \
	   permutation.
	   :return: list of twin partition (can be empty), list of indicies of unique partitions.
	   :rtype: list,np.array
	   '''
		_,uniq_inds=self._get_unique_twins_and_partition_indices(reindex=reindex)
		return uniq_inds



	def apply_CHAMP(self,maxpt=None):
		'''
		Apply CHAMP to the partition ensemble.

		:param maxpt: maximum domain threshhold for included partition.  I.e \
		partitions with a domain greater than maxpt will not be included in pruned \
		set
		:type maxpt: int

		'''

		self.ind2doms=get_intersection(self.get_coefficient_array(),max_pt=maxpt)

	def get_CHAMP_indices(self):

		'''
		Get the indices of the partitions that form the pruned set after application of \
		CHAMP

		:return: list of indices of partitions that are included in the prune set \
		sorted by their domains of dominance
		:rtype: list

		'''

		inds=zip(self.ind2doms.keys(),[val[0][0] for val in self.ind2doms.values()])
		#asscending sort by last value of domain
		inds.sort(key=lambda x: x[1])

		#retreive index
		return [ind[0] for ind in inds]

	def get_CHAMP_partitions(self):

		'''Return the subset of partitions that form the outer envelop.
		:return: List of partitions in membership vector form of the paritions
		:rtype: list

		'''
		inds=self.get_CHAMP_indices()
		return [self.partitions[i] for i in inds]

	def _write_graph_to_hd5f_file(self,file,compress=4):
		'''
		Write the internal graph to hd5f file saving the edge lists, the edge properties, and the \
		vertex properties all as subgroups.  We only save the edges, and the vertex and node attributes

		:param file: openned h5py.File
		:type file: h5py.File
		:return: reference to the File
		'''

		# write over previous if exists.
		if 'graph' in file.keys():
			del file['graph']

		grph=file.create_group("graph")

		grph.create_dataset('directed',data=int(self.graph.is_directed()))
		#save edge list as graph.ecount x 2 numpy array
		grph.create_dataset("edge_list",
							data=np.array([e.tuple for e in self.graph.es]),compression="gzip",compression_opts=compress)

		edge_atts=grph.create_group('edge_attributes')
		for attrib in self.graph.edge_attributes():

			edge_atts.create_dataset(attrib,
									 data=np.array(self.graph.es[attrib]),compression="gzip",compression_opts=compress)

		node_atts=grph.create_group("node_attributes")
		for attrib in self.graph.vertex_attributes():
			node_atts.create_dataset(attrib,
									 data=np.array(self.graph.vs[attrib]),compression="gzip",compression_opts=compress)
		return file

	def _read_graph_from_hd5f_file(self,file):
		'''
		Load self.graph from hd5f file.  Sets self.graph as new igraph created from edge list \
		and attributes stored in the file.

		:param file: Opened hd5f file that contains the edge list, edge attributes, and \
		node attributes stored in the hierarchy as PartitionEnsemble._write_graph_to_hd5f_file.

		:type file: h5py.File

		'''

		grph=file['graph']
		directed=bool(grph['directed'].value)
		self.graph=ig.Graph().TupleList(grph['edge_list'],directed=directed)
		for attrib in grph['edge_attributes'].keys():
			self.graph.es[attrib]=grph['edge_attributes'][attrib][:]
		for attrib in grph['node_attributes'].keys():
			self.graph.vs[attrib] = grph['node_attributes'][attrib][:]


	def save(self,filename=None,dir=".",hdf5=None,compress=9):
		'''
		Use pickle or h5py to store representation of PartitionEnsemble in compressed file.  When called \
		if object has an assocated hdf5_file, this is the default file written to.  Otherwise objected \
		is stored using pickle.

		:param filename: name of file to write to.  Default is created from name of ParititonEnsemble\: \
			"%s_PartEnsemble_%d" %(self.name,self.numparts)
		:param hdf5: save the PartitionEnsemble object as a hdf5 file.  This is \
		very useful for larger partition sets, especially when you only need to work \
		with the optimal subset.  If object has hdf5_file attribute saved \
		this becomes the default
		:type hdf5: bool
		:param compress: Level of compression for partitions in hdf5 file.  With less compression, files take \
		longer to write but take up more space.  9 is default.
		:type compress: int [0,9]
		:param dir: directory to save graph in.  relative or absolute path.  default is working dir.
		:type dir: str
		'''

		if hdf5 is None:
			if self._hdf5_file is None:
				hdf5 is False
			else:
				hdf5 is True



		if filename is None:
			if hdf5:
				if self._hdf5_file is None:
					filename="%s_PartEnsemble_%d.hdf5" %(self.name,self.numparts)
				else:
					filename=self._hdf5_file
			else:
				filename="%s_PartEnsemble_%d.gz" %(self.name,self.numparts)

		if hdf5:
			with h5py.File(os.path.join(dir,filename),'w') as outfile:

				for k,val in iteritems(self.__dict__):
					#store dictionary type object as its own group
					if k=='graph':
						self._write_graph_to_hd5f_file(outfile,compress=compress)

					elif isinstance(val,dict):
						indgrp=outfile.create_group(k)
						for ind,dom in iteritems(val):
							indgrp.create_dataset(str(ind),data=dom,compression="gzip",compression_opts=compress)

					elif isinstance(val,str):
						outfile.create_dataset(k,data=val)

					elif hasattr(val,"__len__"):
						data=np.array(val)

						#1D array don't have a second shape index (ie np.array.shape[1] can throw \
						#IndexError
						cshape=list(data.shape)
						cshape[0]=None
						cshape=tuple(cshape)

						cdset = outfile.create_dataset(k, data=data, maxshape=cshape,
													   compression="gzip",compression_opts=compress)

					elif not val is None:
							#Single value attributes
							cdset = outfile.create_dataset(k,data=val)


			self._hdf5_file=filename

		else:
			with gzip.open(os.path.join(dir,filename),'wb') as fh:
				pickle.dump(self,fh)

		return filename

	def save_graph(self,filename=None,dir="."):
		'''
		Save a copy of the graph with each of the optimal partitions stored as vertex attributes \
		in graphml compressed format.  Each partition is attribute names part_gamma where gamma is \
		the beginning of the partitions domain of dominance

		:param filename: name of file to write out to.  Default is self.name.graphml.gz or \
		:type filename: str
		:param dir: directory to save graph in.  relative or absolute path.  default is working dir.
		:type dir: str
		'''

		#TODO add other graph formats for saving.
		if filename is None:
			filename=self.name+".graphml.gz"
		outgraph=self.graph.copy()
		#Add the CHAMP partitions to the outgraph
		for ind in self.get_CHAMP_indices():
			part_name="part_%.3f" %(self.ind2doms[ind][0][0])
			outgraph.vs[part_name]=self.partitions[ind]

		outgraph.write_graphmlz(os.path.join(dir,filename))



	def open(self,filename):
		'''
		Loads pickled PartitionEnsemble from file.

		:param file:  filename of pickled PartitionEnsemble Object

		:return: writes over current instance and returns the reference

		'''

		#try openning it as an hd5file
		try:
			with h5py.File(filename,'r') as infile:
				self._read_graph_from_hd5f_file(infile)
				for key in infile.keys():
					if key!='graph' and key!='_partitions':
						#get domain indices recreate ind2dom dict
						if key=='ind2doms':
							self.ind2doms={}
							for ind in infile[key]:
								self.ind2doms[int(ind)]=infile[key][ind][:]
						else:
							try:
								self.__dict__[key]=infile[key][:]
							except ValueError:
								self.__dict__[key]=infile[key].value

			#store this for accessing partitions

			self._hdf5_file=filename
			return self

		except IOError:

			with gzip.open(filename,'rb') as fh:
				opened=pickle.load(fh)

			openedparts=opened.get_partition_dictionary()

			#construct and return
			self.__init__(opened.graph,listofparts=openedparts)
			return self


	def _sub_tex(self,str):
		new_str = re.sub("\$", "", str)
		new_str = re.sub("\\\\ge", ">=", new_str)
		new_str = re.sub("\\\\", "", new_str)
		return new_str

	def _remove_tex_legend(self,legend):
		for text in legend.get_texts():
			text.set_text(self._sub_tex(text.get_text()))
		return legend

	def _remove_tex_axes(self, axes):
		axes.set_title(self._sub_tex(axes.get_title()))
		axes.set_xlabel(self._sub_tex(axes.get_xlabel()))
		axes.set_ylabel(self._sub_tex(axes.get_ylabel()))
		return axes

	def plot_modularity_mapping(self,ax=None,downsample=2000,champ_only=False,legend=True,
								no_tex=False):
		'''

		Plot a scatter of the original modularity vs gamma with the modularity envelope super imposed. \
		Along with communities vs :math:`\\gamma` on a twin axis.  If no orig_mod values are stored in the \
		ensemble, just the modularity envelope is plotted.  Depending on the backend used to render plot \
		the latex in the labels can cause error.  If you are getting RunTime errors when showing or saving \
		the plot, try setting no_tex=True

		:param ax: axes to draw the figure on.
		:type ax: matplotlib.Axes
		:param champ_only: Only plot the modularity envelop represented by the CHAMP identified subset.
		:type champ_only: bool
		:param downsample: for large number of runs, we down sample the scatter for the number of communities \
		and the original partition set.  Default is 2000 randomly selected partitions.
		:type downsample: int
		:param legend: Add legend to the figure.  Default is true
		:type legend: bool
		:param no_tex: Use latex in the legends.  Default is true.  If error is thrown on plotting try setting \
		this to false.
		:type no_tex: bool
		:return: axes drawn upon
		:rtype: matplotlib.Axes


		'''

		if ax == None:
			f = plt.figure()
			ax = f.add_subplot(111)

		if not no_tex:
			rc('text',usetex=True)
		else:
			rc('text',usetex=False)



		# check for downsampling and subset indices
		if downsample and downsample<=len(self.partitions):
			rand_ind=np.random.choice(range(len(self.partitions)),size=downsample)
		else:
			rand_ind=range(len(self.partitions))

		allgams = [self.resolutions[ind] for ind in rand_ind]
		allcoms = [self.numcoms[ind] for ind in rand_ind]

		if not champ_only and not self.orig_mods[0] is None :


			allmods=[self.orig_mods[ind] for ind in rand_ind]

			ax.set_ylim([np.min(allmods) - 100, np.max(allmods) + 100])
			mk1 = ax.scatter(allgams, allmods,
							 color='red', marker='.', alpha=.6, s=10,
							 label="modularity", zorder=2)

		#take the x-coord of first point in each domain

		#Get lists for the champ subset
		champ_inds=self.get_CHAMP_indices()

		# take the x-coord of first point in each domain
		gammas=[ self.ind2doms[ind][0][0] for ind in champ_inds  ]
		# take the y-coord of first point in each domain
		mods = [self.ind2doms[ind][0][1] for ind in champ_inds]

		champ_coms = [self.numcoms[ind] for ind in champ_inds]



		mk5 = ax.plot(gammas, mods, ls='--', color='green', lw=3, zorder=3)
		mk5 = mlines.Line2D([], [], color='green', ls='--', lw=3)

		mk2 = ax.scatter(gammas, mods, marker="v", color='blue', s=60, zorder=4)
		#	 ax.scatter(gamma_ins,orig_mods,marker='x',color='red')
		ax.set_ylabel("modularity")



		a2 = ax.twinx()
		a2.grid('off')
		#	 a2.scatter(allgammas,allcoms,marker="^",color="#fe9600",alpha=1,label=r'\# communities ($\ge 5$ nodes)',zorder=1)

		sct2 = a2.scatter(allgams, allcoms, marker="^", color="#91AEC1",
						  alpha=1, label=r'\# communities ($\ge %d$ nodes)'%(self.min_com_size),
						  zorder=1)
		#	 sct2.set_path_effects([path_effects.SimplePatchShadow(alpha=.5),path_effects.Normal()])

		# fake for legend with larger marker size
		mk3 = a2.scatter([], [], marker="^", color="#91AEC1", alpha=1,
						 label=r'\# communities ($\ge %d$)'%(self.min_com_size),
						 zorder=1,
						 s=20)



		stp = a2.step(gammas, champ_coms, color="#004F2D", where='post',
					  path_effects=[path_effects.SimpleLineShadow(alpha=.5), path_effects.Normal()])
		#	 stp.set_path_effects([patheffects.Stroke(linewidth=1, foreground='black'),
		#					 patheffects.Normal()])

		# for legend
		mk4 = mlines.Line2D([], [], color='#004F2D', lw=2,
							path_effects=[path_effects.SimpleLineShadow(alpha=.5), path_effects.Normal()])


		a2.set_ylabel(r"\# communities ($\ge 5$ nodes)")

		ax.set_zorder(a2.get_zorder() + 1)  # put ax in front of ax2
		ax.patch.set_visible(False)  # hide the 'canvas'

		ax.set_xlim(xmin=0, xmax=max(allgams))
		if legend:
			l = ax.legend([mk1, mk3, mk2, mk4, mk5],
						  ['modularity', r'\# communities ($\ge %d $ nodes)' %(self.min_com_size), "transitions,$\gamma$",
						   r"\# communities ($\ge %d$ nodes) optimal" %(self.min_com_size), "convex hull of $Q(\gamma)$"],
						  bbox_to_anchor=[0.5, .87], loc='center',
						  frameon=True, fontsize=14)
			l.get_frame().set_fill(False)
			l.get_frame().set_ec("k")
			l.get_frame().set_linewidth(1)
			if no_tex:
				l=self._remove_tex_legend(l)

		if no_tex: #clean up the tex the axes
			a2=self._remove_tex_axes(a2)
			ax=self._remove_tex_axes(ax)

		return ax


#### MULTI-LAYER Louvain static methods

#MUTLILAYER GRAPH CREATION

def _create_interslice(interlayer_edges, layer_vec, directed=False):
	"""


	"""
	weights=[]
	layers = np.unique(layer_vec)
	layer_edges = set()
	for e in interlayer_edges:
		ei,ej=e[0],e[1]
		lay_i = layer_vec[ei]
		lay_j = layer_vec[ej]
		if len(e)>2:
			weights.append(e[2])
		assert lay_i != lay_j #these shoudl be interlayer edges
		if lay_i < lay_j:
			layer_edges.add((lay_i, lay_j))
		else:
			layer_edges.add((lay_j, lay_i))


	slice_couplings = ig.Graph(n=len(layers), edges=list(layer_edges), directed=directed)
	if len(weights) == 0:
		weights=1
	slice_couplings.es['weight']=weights
	return slice_couplings

def _create_all_layers_single_igraph(intralayer_edges, layer_vec, directed=False):
	"""
	"""
	#create a single igraph
	layers, cnts = np.unique(layer_vec, return_counts=True)
	layer_elists = []
	layer_weights=[ ]
	# we divide up the edges by layer
	for e in intralayer_edges:
		ei,ej=e[0],e[1]
		if not directed: #switch order to preserve uniqness
			if ei>ej:
				ei,ej=e[1],e[0]

		layer_elists.append((ei, ej))
		if len(e)>2:
			layer_weights.append(e[2])

	layer_graphs = []
	cgraph = ig.Graph(n=len(layer_vec), edges=layer_elists, directed=directed)
	if len(layer_weights) > 0:  # attempt to set the intralayer weights
		cgraph.es['weight'] = layer_weights
	else:
		cgraph.es['weight']=1
	cgraph.vs['nid']=range(cgraph.vcount())
	cgraph.vs['layer_vec']=layer_vec
	return cgraph
	# layer_graphs.append(cgraph)
	# return layer_graphs

def _create_all_layer_igraphs_multi(intralayer_edges, layer_vec, directed=False):
	"""
	"""

	layers, cnts = np.unique(layer_vec, return_counts=True)
	layer_elists = [[] for _ in range(len(layers))]
	layer_weights=[[] for _ in range(len(layers))]
	# we divide up the edges by layer
	for e in intralayer_edges:
		ei,ej=e[0],e[1]
		if not directed: #switch order to preserve uniqness
			if ei>ej:
				ei,ej=e[1],e[0]

		# these should all be intralayer edges
		lay_i, lay_j = layer_vec[ei], layer_vec[ej]
		assert lay_i == lay_j

		coffset=np.sum(cnts[:lay_i])#indexing for edges must start with 0 for igraph

		layer_elists[lay_i].append((ei-coffset, ej-coffset))
		if len(e)>2:
			layer_weights[lay_i].append(e[2])

	layer_graphs = []
	tot = 0
	for i, layer_elist in enumerate(layer_elists):
		if not directed:
			layer_elist=list(set(layer_elist)) #prune out non-unique
		#you have adjust the elist to start with 0 for first node
		cnts[i]
		cgraph = ig.Graph(n=cnts[i], edges=layer_elist, directed=directed)
		assert cgraph.vcount()==cnts[i],'edges indicated more nodes within graph than the layer_vec'
		cgraph.vs['nid'] = range(tot , tot +cnts[i])  # each node in each layer gets a unique id
		if len(layer_weights[i])>0: #attempt to set the intralayer weights
			cgraph.es['weight']=layer_weights[i]
		tot += cnts[i]
		layer_graphs.append(cgraph)

	return layer_graphs


def _label_nodes_by_identity(intralayer_graphs, interlayer_edges, layer_vec):
	"""Go through each of the nodes and determine which ones are shared across multiple slices.\
	We create an attribute on each of the graphs to indicate the shared identity \
	of that node.  This is done through tracking the predecessors of the node vi the interlayer\
	connections

	"""

	namedict = {}
	backedges = {}

	# For each node we hash if it has any neighbors in the layers behind it.

	for e in interlayer_edges:
		ei,ej=e[0],e[1]
		if ei < ej:
			backedges[ej] = backedges.get(ej, []) + [ei]
		else:
			backedges[ei] = backedges.get(ei, []) + [ej]

	offset = 0  # duplicate names used
	for i, lay in enumerate(layer_vec):

		if i not in backedges:  # node doesn't have a predecessor
			namedict[i] = i - offset
		else:
			pred = backedges[i][0] #get one of the predecessors
			namedict[i] = namedict[pred]  # get the id of the predecessor
			offset += 1

	for graph in intralayer_graphs:
		graph.vs['shared_id'] = map(lambda x: namedict[x], graph.vs['nid'])
		assert len(set(graph.vs['shared_id']))==len(graph.vs['shared_id']), "IDs within a slice must all be unique"


def create_multilayer_igraph_from_edgelist(intralayer_edges, interlayer_edges, layer_vec, directed=False):
	"""
	   We create an igraph representation used by the louvain package to represents multi-slice graphs.  \
	   For this method only two graphs are created :
	   intralayer_graph : all edges withis this graph are treated equally though the null model is adjusted \
	   based on each slice's degree distribution
	   interlayer_graph:  sinlge graph that contains only interlayer connections between all nodes

	:param intralayer_edges: edges representing intralayer connections.  Note each node should be assigned a unique\
	index.
	:param interlayer_edges: connection across layers.
	:param layer_vec: indication of which layer each node is in.  This important in computing the modulary modularity\
	null model.
	:param directed: If the network is directed or not
	:return: intralayer_graph,interlayer_graph
	"""
	t=time()
	interlayer_graph = _create_all_layers_single_igraph(interlayer_edges, layer_vec=layer_vec, directed=directed)
	# interlayer_graph=interlayer_graph[0]
	logging.debug("create interlayer : {:.4f}".format(time()-t))
	t=time()
	intralayer_graph = _create_all_layers_single_igraph(intralayer_edges, layer_vec, directed=directed)
	logging.debug("create intrallayer : {:.4f}".format(time()-t))
	t=time()
	return intralayer_graph,interlayer_graph


def call_slices_to_layers_from_edge_list(intralayer_edges, interlayer_edges, layer_vec, directed=False):
	"""
	   We create an igraph representation used by the louvain package to represents multi-slice graphs.  This returns \
	   three values:
		layers : list of igraphs each one representing a single slice in the network (all nodes across all layers \
		are present but only the edges in that slice)
		interslice_layer: igraph representing interlayer connectiosn
		G_full : igraph with connections for both inter and intra slice connections across all nodes ( differentiated) \
		by igraph.es attribute.

	:param intralayer_edges:
	:param interlayer_edges:
	:param layer_vec:
	:param directed:
	:return: layers
	"""
	t=time()
	interlayer_graph = _create_interslice(interlayer_edges,layer_vec=layer_vec, directed=directed)
	# interlayer_graph=interlayer_graph[0]
	logging.debug("create interlayer : {:.4f}".format(time()-t))
	t=time()
	intralayer_graphs = _create_all_layer_igraphs_multi(intralayer_edges, layer_vec, directed=directed)
	logging.debug("create intrallayer : {:.4f}".format(time()-t))
	t=time()

	_label_nodes_by_identity(intralayer_graphs, interlayer_edges, layer_vec)
	logging.debug("label nodes : {:.4f}".format(time()-t))
	t=time()
	interlayer_graph.vs['slice'] = intralayer_graphs
	layers, interslice_layer, G_full = louvain.slices_to_layers(interlayer_graph, vertex_id_attr='shared_id')
	logging.debug("louvain call : {:.4f}".format(time()-t))
	t=time()
	return layers, interslice_layer, G_full

def adjacency_to_edges(A):
	nnz_inds = np.nonzero(A)
	nnzvals = np.array(A[nnz_inds])
	if len(nnzvals.shape)>1:
		nnzvals=nnzvals[0] #handle scipy sparse types
	return zip(nnz_inds[0], nnz_inds[1], nnzvals)


def create_multilayer_igraph_from_adjacency(A,C,layer_vec,directed=False):
	"""
	Create the multilayer igraph representation necessary to call igraph-louvain \
	in the multilayer context.  Edge list are formed and champ_fucntions.create_multilayer_igraph_from_edgelist \
	is called.  Each edge list includes the weight of the edge \
	as indicated in the appropriate adjacency matrix.

	:param A:
	:param C:
	:param layer_vec:
	:return:
	"""

	nnz_inds = np.nonzero(A)
	nnzvals = np.array(A[nnz_inds])
	if len(nnzvals.shape)>1:
		nnzvals=nnzvals[0] #handle scipy sparse types

	intra_edgelist = adjacency_to_edges(A)
	inter_edgelist = adjacency_to_edges(C)


	return create_multilayer_igraph_from_edgelist(intralayer_edges=intra_edgelist,
												  interlayer_edges=inter_edgelist,
												  layer_vec=layer_vec,directed=directed)

# def _save_ml_graph(intralayer_edges,interlayer_edges,layer_vec,filename=None):
#	 if filename is None:
#		 file=tempfile.NamedTemporaryFile()
#	 filename=file.name
#
#	 outdict={"interlayer_edges":interlayer_edges,
#			  'intralayer_edges':intralayer_edges,
#			  'layer_vec':layer_vec}
#
#	 with gzip.open(filename,'w') as fh:
#		 pickle.dump(outdict,fh)
#	 return file #returns the filehandle


def _save_ml_graph(slice_layers,interslice_layer):
	"""
	We save the layers of the graph as graphml.gz files here
	:param slice_layers:
	:param interslice_layer:
	:param layer_vec:
	:return:
	"""
	filehandles=[]
	filenames=[]
	#interslice couplings will be last
	for layer in slice_layers+[interslice_layer]: #save each graph in it's own file handle
		fh=tempfile.NamedTemporaryFile(mode='wb',suffix='.graphml.gz')
		layer.write_graphmlz(fh.name)
		filehandles.append(fh)
		filenames.append(fh.name)
	return filehandles,filenames


def _get_sum_internal_edges_from_partobj_list(part_obj_list,weight='weight'):
	A=0
	for part_obj in part_obj_list:
		A+=get_sum_internal_edges(part_obj,weight=weight)
	return A

def get_expected_edges_ml(part_obj,layer_vec,weight='weight'):
	"""
	Multilayer calculation of expected edges.  Breaks up partition object \
	by layer and calculated expected edges for each layer-subgraph seperately\
	thus getting the relative weights correct
	:param part_obj: ig.VertexPartition with the appropriate graph and membership vector.
	:param layer_vec: array with length equaling number of nodes specifying which layer each node is in.
	:param weight: weight attribute on network
	:return:
	"""
	P_tot=0
	layers=np.unique(layer_vec)
	for layer in layers:
		cind=np.where(layer_vec==layer)[0]
		subgraph=part_obj.graph.subgraph(cind)
		submem=part_obj.membership[cind]
		cpartobj=ig.VertexClustering(graph=subgraph,membership=submem)
		P_tot += get_expected_edges(cpartobj,weight=weight)
	return P_tot

def _get_sum_expected_edges_from_partobj_list(part_obj_list,weight='weight'):
	P=0
	for part_obj in part_obj_list:
		P+=get_expected_edges_ml(part_obj,weight=weight)
	return P


def _get_modularity_from_partobj_list(part_obj_list):
	finmod=0
	for part_obj in part_obj_list:
		finmod+=part_obj.quality()
	return finmod

def run_louvain_multilayer(intralayer_graph,interlayer_graph, layer_vec, weight='weight',
						   resolution=1.0, omega=1.0,nruns=1):
	# logging.debug('loading igraphs')
	# t=time()
	# layers=[]
	# mu=0 #total degrees (intra + inter)
	# for i,filename in enumerate(multilayer_files): #assume last is interslice
	#	 if i==len(multilayer_files)-1:
	#		 interslice_layer=ig.load(filename)
	#		 interslice_layer.es['weight']=omega #set coupling strength
	#		 mu+=np.sum(interslice_layer.es['weight'])
	#	 else:
	#		 layers.append(ig.load(filename))
	#		 try:
	#			 mu += np.sum(layers[-1].es[weight])
	#		 except:
	#			 mu += np.sum(layers[-1].ecount()) #not weighted
	# logging.debug('time: {:.4f}'.format(time() - t))
	logging.debug('Shuffling node ids')
	t=time()
	mu=np.sum(intralayer_graph.es[weight])+interlayer_graph.ecount()

	layers=[intralayer_graph] #for now only have one layer representing all intralayer connections

	outparts=[]
	for run in range(nruns):
		rand_perm = list(np.random.permutation(interlayer_graph.vcount()))
		rperm = rev_perm(rand_perm)
		interslice_layer_rand = interlayer_graph.permute_vertices(rand_perm)
		offset=0
		#create permutation vectors for each of these igraphs
		rlayers=[]
		for layer in layers:
			rlayers.append(layer.permute_vertices(rand_perm))
		logging.debug('time: {:.4f}'.format(time()-t))

		t=time()

		#create the partition objects
		layer_partition_objs=[]

		logging.debug('creating partition objects')
		t=time()
		for i,layer in enumerate(rlayers): #these are the shuffled igraph slice objects
			try:
				res=resolution[i]
			except:
				res=resolution

			cpart=louvain.RBConfigurationVertexPartitionWeightedLayers(layer,layer_vec=layer_vec,
														 weights=weight,
														 resolution_parameter=resolution)
			layer_partition_objs.append(cpart)

		coupling_partition=louvain.RBConfigurationVertexPartition(interslice_layer_rand,
																  weights='weight',resolution_parameter=0)
		all_layer_partobjs=layer_partition_objs+[coupling_partition]
		optimiser=louvain.Optimiser()
		logging.debug('time: {:.4f}'.format(time()-t))
		logging.debug('running optimiser')
		t=time()
		improvement=optimiser.optimise_partition_multiplex(all_layer_partobjs)

		#the membership for each of the partitions is tied together.
		finalpartition=get_orig_ordered_mem_vec(rperm,all_layer_partobjs[0].membership)
		#use only the intralayer part objs
		A=_get_sum_internal_edges_from_partobj_list(layer_partition_objs,weight=weight)
		P=_get_sum_expected_edges_from_partobj_list(layer_partition_objs,weight=weight)
		C=get_sum_internal_edges(coupling_partition,weight=weight)
		outparts.append({'partition': np.array(finalpartition),
						 'resolution': resolution,
						 'coupling':omega,
						 'orig_mod': (.5/mu)*_get_modularity_from_partobj_list(all_layer_partobjs),
						 'int_edges': A,
						 'exp_edges': P,
						'int_inter_edges':C})

	logging.debug('time: {:.4f}'.format(time()-t))
	return outparts


def _parallel_run_louvain_multimodularity(files_layervec_gamma_omega):
	logging.debug('running parallel')
	# graph_file_names,layer_vec,gamma,omega=files_layervec_gamma_omega
	np.random.seed() #reset seed in forked process
	# louvain.set_rng_seed(int(np.random.get_state()[1][0]))
	louvain.set_rng_seed(np.random.randint(2147483647)) #max value for unsigned long

	intralayer_graph,interlayer_graph,layer_vec,gamma,omega=files_layervec_gamma_omega

	partition=run_louvain_multilayer(intralayer_graph,interlayer_graph, layer_vec=layer_vec, resolution=gamma, omega=omega)



	return partition

def parallel_multilayer_louvain(intralayer_edges,interlayer_edges,layer_vec,
								gamma_range,ngamma,omega_range,nomega,maxpt=None,numprocesses=2):

	""""""
	logging.debug('creating graphs from edges')
	t=time()
	intralayer_graph,interlayer_graph=create_multilayer_igraph_from_edgelist(intralayer_edges=intralayer_edges,
																			 interlayer_edges=interlayer_edges,
																			 layer_vec=layer_vec)



	logging.debug('time {:.4f}'.format(time() - t))
	# logging.debug('graph to file')
	# t = time()
	# fhandles, fnames = _save_ml_graph(slice_layers=[intralayer_graph],
	#								   interslice_layer=interlayer_graph)
	# logging.debug('time {:.4f}'.format(time() - t))
	gammas=np.linspace(gamma_range[0],gamma_range[1],num=ngamma)
	omegas=np.linspace(omega_range[0],omega_range[1],num=nomega)

	args = itertools.product([intralayer_graph],[interlayer_graph], [layer_vec],
							 gammas,omegas)

	with terminating(Pool(numprocesses)) as pool:
		parts_list_of_list=pool.map(_parallel_run_louvain_multimodularity,args)


	all_part_dicts=[pt for partrun in parts_list_of_list for pt in partrun]
	tempf.close()
	outensemble=MultiLayerPartitionEnsemble(graph,listofparts=all_part_dicts,maxpt=maxpt)

	return outensemble

def parallel_multilayer_louvain_from_adj(intralayer_adj, interlayer_adj,layer_vec,
										 gamma_range, omega_range):

	"""Call parallel multilayer louvain with adjacency matrices """
	intralayer_edges=adjacency_to_edges(intralayer_adj)
	interlayer_edges=adjacency_to_edges(interlayer_adj)

	return parallel_multilayer_louvain(intralayer_edges=intralayer_edges,interlayer_edges=interlayer_edges,
									   layer_vec=layer_vec,
									   gamma_range=gamma_range,omega_range=omega_range)