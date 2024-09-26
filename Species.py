"""
File: Species.py
Author: Grace Todd
Date: September 17, 2024
Description: A class used to hold information about a specific species.
			This includes everything from the physical characteristics
			described by the LLM to the tree parameters used by
			3-PG, the forest growth model.
"""

import csv

class Species:
	"""
	Holds information about a specific species.
	Takes in data collected by parameter estimator

	TODO break up the local variables into smaller, identifiable classes
	TODO adding masting cycle to this might have messed everything up
	"""
	def __init__(self, name, name_scientific, qualities, quantities, attributes=None):
		"""
		Attributes are a combination of LLM responses (qualitative) 
		and parameter estimation (quantitative)
		Input from parameter estimation function output, 
		quantitative values default to 0 if not found
		TODO extrapolate the most important species attributes here
		"""
		# TODO keep these two
		self.name:str = name
		self.name_scientific:str = name_scientific

		self.__dict__.update(qualities.__dict__) # Copy all qualities to species
		self.__dict__.update(quantities.__dict__) # Copy all quantities to species
		
		self.knowledge_base = []

		if attributes: # then it's a knowledge base item
			self.__dict__.update(attributes.__dict__)
		else: # attributes need to be estimated
			self.knowledge_base = load_knowledge_base(filepath='test_data/species_data_kb.csv') # TODO this is volatile
			self.estimate_attributes()

		# Data calculated from 3-PG
		self.b = 0

		# for synthetic data purposes -> estimating dimensions for a species
		self.height = None
		self.dbh = None
		self.lcl = None
		self.c_diam = None


	def get_basic_info(self):
		"""
		Prints the qualitative data about a tree species. Just for fun, but also for fact checking.
		"""
		print(f'\n================== {self.name} ({self.name_scientific}) ===================')
		print(f'{self.name} are a {self.deciduous_evergreen[0]} species, \
and are commonly found in {", ".join(self.habitat)} climates.')
		print(f'FOLIAGE: {self.name} tend to have a {", ".join(self.tree_form)} form, \
with {", ".join(self.leaf_color)}, {", ".join(self.leaf_shape)}-type leaves.')
		print(f'WOOD: The bark of {self.name} have a {" or ".join(self.bark_texture)} texture \
and tend to be {" and ".join(self.bark_color)} in color.')
		print(f'SEEDING: It takes the {self.name} {self.seeding_age} years to be able to produce \
seeds in a {" or ".join(self.habitat)} climate. \nAfter this age, seeds are produced approximately every \
{self.masting_cycle} years.\n')

	def estimate_attributes(self):
		"""
		References the knowledge base and uses the species' visual qualities to
		estimate formula variables for growth modeling.
		"""

		# ===== FIND SIMILARITIES =====
		def count_similarities(self, tree):
			return len(set(self) & set(tree))
		
		similarity_dict = {}
		# leaf_shape, leaf_color, tree_form, deciduous_evergreen, habitat, bark_texture, bark_color, tree_roots, canopy_density
		for tree in self.knowledge_base:
			points = 0  # Initialize points for current tree
			leaf_points = 0
			canopy_points = 0
			stem_points = 0
			habitat_points = 0


			# check leaf similarity
			leaf_points += count_similarities(self.leaf_color, tree.leaf_color)
			leaf_points += count_similarities(self.leaf_shape, tree.leaf_shape)

			# check canopy similarity
			canopy_points += count_similarities(self.tree_form, tree.tree_form)
			canopy_points += count_similarities(self.deciduous_evergreen, tree.deciduous_evergreen)
			canopy_points += count_similarities(self.canopy_density, tree.canopy_density)


			# check stem similarity
			stem_points += count_similarities(self.bark_texture, tree.bark_texture)
			stem_points += count_similarities(self.bark_color, tree.bark_color)
			stem_points += count_similarities(self.tree_roots, tree.tree_roots)

			# check habitat similarity
			habitat_points += count_similarities(self.habitat, tree.habitat)

			points += leaf_points + canopy_points + stem_points + habitat_points

			# Check if the tree has earned any points
			if points > 0:
				similarity_dict[tree] = [leaf_points, canopy_points, stem_points, habitat_points, points]
		# =============================

		# ========= DETERMINE BEST PARAMETERS FOR MOST SIMILAR TREES ==========
		def find_most_similar(attribute_index):
			max_points = -1
			tree_with_max_points = None

			for tree, points in similarity_dict.items():
				attribute = points[attribute_index]  # Assuming leaf_points is the first item in the list
				if attribute > max_points:
					max_points = attribute
					tree_with_max_points = tree

			return tree_with_max_points
		
		# [leaf_points, canopy_points, stem_points, habitat_points]
		l = find_most_similar(0) # similar leaves
		c = find_most_similar(1) # similar canopy
		s = find_most_similar(2) # similar stem
		h = find_most_similar(3) # similar habitat
		g = find_most_similar(4) # similar in general

		leaf_attr = self.Attributes.LeafAttributes(
			l.k, l.acx, l.sla_1, l.sla_0, l.t_sla_mid, l.yfx, l.yf0, l.tyf
		)

		canopy_attr = self.Attributes.CanopyAttributes(
			c.tc, c.mf, c.p2, c.p20, c.ms, c.wsx1000, c.nm
		)

		stem_attr = self.Attributes.StemAttributes(
			s.mr, s.ms, s.yr, s.nr_min, s.nr_max, s.m_0, s.ah, s.nhb, s.nhc, s.ahl,
			s.nhlb, s.nhlc, s.ak, s.nkb, s.nkh, s.av, s.nvb, s.nvh, s.nvbh, s.aws, s.nws
		)

		habitat_attr = self.Attributes.HabitatAttributes(
			h.t_min, h.t_opt, h.t_max, h.kd, h.n_theta, h.c_theta
		)

		general_attr = self.Attributes.GeneralAttributes(
			g.fcax_700, g.fn0, g.nfn, g.r_age, g.n_age, g.max_age, g.kf
		)

		attributes = self.Attributes(leaf_attr, canopy_attr, stem_attr, habitat_attr, general_attr)
		self.__dict__.update(attributes.__dict__)
		# =====================================================================

		pass


	class Attributes:
		"""
		This class holds all of the parameters used by 3-PG and estimated by the system.
		These parameters are more numerous and mroe difficult to work with, so they have
		been broken up into digestible chunks.
		"""
		def __init__(self, leaf, canopy, stem, habitat, general):
			self.__dict__.update(leaf.__dict__) # leaf attributes
			self.__dict__.update(canopy.__dict__) # canopy attributes
			self.__dict__.update(stem.__dict__) # stem attributes
			self.__dict__.update(habitat.__dict__) # habitat attributes
			self.__dict__.update(general.__dict__) # geenral attributes

		class LeafAttributes:
			"""
			This class holds data estimated by the knowledge base about attributes
			related to leaf similarity:
			k, acx, sla_1, sla_0, t_sla_mid,yfx, yf0, tyf
			"""
			def __init__(self, k, acx, sla_1, sla_0, t_sla_mid, yfx, yf0, tyf):
				self.k = float(k) # TODO structure it like this? And then have a comment explaining what it is
				self.acx = acx # Species-specific maximum potential, used for GPP calculation
				self.sla_1 = sla_1
				self.sla_0 = sla_0
				self.t_sla_mid = t_sla_mid
				self.yfx = yfx
				self.yf0 = yf0
				self.tyf = tyf
	

		class CanopyAttributes:
			"""
			This class holds data estimated by the knowledge base about attributes
			related to canopy similarity:
			tc, mf, p2, p20, ms, wsx1000, nm
			"""
			def __init__(self, tc, mf, p2, p20, ms, wsx1000, nm):
				self.tc = tc
				self.mf = mf
				self.p2 = p2
				self.p20 = p20
				self.ms = ms
				self.wsx1000 = wsx1000
				self.nm = nm

		class StemAttributes:
			"""
			This class holds data estimated by the knowledge base about attributes
			related to wood, bark, and root similarity:
			mr, ms, yr, nr_min, nr_max, m_0, ah,nhb, nhc, ahl, nhlb, nhlc, 
			ak, nkb, nkh, av, nvb, nvh, nvbh
			TODO this class is a bit big, maybe break it down?
			"""
			def __init__(self, mr, ms, yr, nr_min, nr_max, m_0, ah, nhb, nhc, ahl, 
				nhlb, nhlc, ak, nkb, nkh, av, nvb, nvh, nvbh, aws, nws):
				self.mr = mr
				self.ms = ms
				self.yr = yr
				self.nr_min = nr_min
				self.nr_max = nr_max
				self.m_0 = m_0
				self.ah = ah			# Constant in the stem-height relationship
				self.nhb = nhb
				self.nhc = nhc
				self.ahl = ahl
				self.nhlb = nhlb
				self.nhlc = nhlc
				self.ak = ak
				self.nkb = nkb
				self.nkh = nkh
				self.av = av
				self.nvb = nvb
				self.nvh = nvh
				self.nvbh = nvbh
				self.aws = aws
				self.nws = nws


		class HabitatAttributes:
			"""
			This class holds data estimated by the knowledge base about attributes
			related to habitat similarity:
			t_min, t_opt, t_max, kd, n_theta, c_theta
			"""
			def __init__(self, t_min, t_opt, t_max, kd, n_theta, c_theta):
				self.t_min = t_min
				self.t_opt = t_opt
				self.t_max = t_max
				self.kd = kd
				self.n_theta = n_theta
				self.c_theta = c_theta

		class GeneralAttributes:
			"""
			This class holds data estimated by te knowledge base about attributes
			related to general, overall similarity:
			fcax_700, fn0, nfn, r_age, n_age, max_age
			TODO be more concise with these docstrings
			"""
			def __init__(self, fcax_700, fn0, nfn, r_age, n_age, max_age, kf):
				self.fcax_700 = fcax_700
				self.fn0 = fn0
				self.nfn = nfn
				self.r_age = r_age
				self.n_age = n_age
				self.max_age = max_age
				self.kf = kf

	class VisualCharacteristics:
		"""
		The visual characteristics or qualities of the species
		as approximated by the LLM:
		leaf_shape, canopy_density, deciduous_evergreen,
		leaf_color, tree_form, habitat, bark_texture, bark_color, masting_cycle
		"""
		# TODO instead of feeding in all of these, read them in from csv by row
		def __init__(self, leaf_shape, leaf_color, tree_form, deciduous_evergreen, habitat, bark_texture, bark_color, tree_roots, canopy_density):
			# Obtained from LLM (all are lists of strings):
			self.leaf_shape = leaf_shape.split('/')
			self.leaf_color = leaf_color.split('/')

			self.tree_form = tree_form.split('/')
			self.tree_roots = tree_roots.split('/')

			self.canopy_density = canopy_density.split('/')
			self.deciduous_evergreen = deciduous_evergreen.split('/')
			self.habitat = habitat.split('/')

			self.bark_texture = bark_texture.split('/')
			self.bark_color = bark_color.split('/')
	
	class OtherCharacteristics:
		"""
		The reproductive characteristics as approximated by the LLM:
		masting_cycle, seeding_age
		"""
		def __init__(self, masting_cycle, seeding_age, foliage, stem, root):
			self.masting_cycle : int = int(masting_cycle)
			self.seeding_age : int = int(seeding_age)
			self.init_foliage_biomass : float = float(foliage)
			self.init_stem_biomass : float = float(stem)
			self.init_root_biomass : float = float(root)
			

def load_knowledge_base(filepath):
	# reads in the knowledge base csv file
	# each row of information is assigned to a the appropriate class object
	# TODO should the knowledge base be a species attribute? Like we have the list of trees in Forest, 
	# maybe we could have the list of species... or would that be too recursive and cause problems?

	"""
	name,name_scientific,
	leaf_shape,canopy_density,deciduous_evergreen,leaf_color,tree_form,tree_roots,habitat,bark_texture,bark_color,
	t_min,t_opt,t_max,kf,fcax_700,kd,n_theta,c_theta,p2,p20,acx,sla_1,sla_0,t_sla_mid,fn0,nfn,tc,max_age,r_age,
	n_age,mf,mr,ms,yfx,yf0,tyf,yr,nr_max,nr_min,m_0,wsx1000,nm,k,aws,nws,ah,nhb,nhc,ahl,nhlb,nhlc,ak,nkb,nkh,av,nvb,nvh,nvbh,
	masting_cycle,seeding_age
	"""

	knowledge_base = []

	with open(filepath, 'r', encoding='utf-8') as file:
		reader = csv.DictReader(file)  # Use DictReader to read the CSV as a dictionary
		for row in reader:
			# Exclude lines starting with a comment character (e.g., #)
			if not row or row.get('name', '').startswith("#"):
				continue
			
			# Get the name and scientific name
			name = row.get('name')
			scientific_name = row.get('name_scientific')

			# Get the visual characteristics
			leaf_shape = row.get('leaf_shape')
			leaf_color = row.get('leaf_color')
			tree_form = row.get('tree_form')
			deciduous_evergreen = row.get('deciduous_evergreen')
			habitat = row.get('habitat')
			bark_texture = row.get('bark_texture')
			bark_color = row.get('bark_color')
			tree_roots = row.get('tree_roots')
			canopy_density = row.get('canopy_density')

			visual_characteristics = Species.VisualCharacteristics(
				leaf_shape, leaf_color, tree_form, deciduous_evergreen, habitat, bark_texture, bark_color,
				tree_roots, canopy_density
				)

			# Get the seeding characteristics
			seeding_age = row.get('seeding_age')
			masting_cycle = row.get('masting_cycle')
			foliage = row.get('foliage_biomass')
			stem = row.get('stem_biomass')
			root = row.get('root_biomass')
			seeding = Species.OtherCharacteristics(int(masting_cycle), int(seeding_age), float(foliage), float(stem), float(root))

			# Get the attributes
			# Leaf attributes
			k = row.get('k')
			acx = row.get('acx')
			sla_1 = row.get('sla_1')
			sla_0 = row.get('sla_0')
			t_sla_mid = row.get('t_sla_mid')
			yfx = row.get('yfx')
			yf0 = row.get('yf0')
			tyf = row.get('tyf')

			leaf_attr = Species.Attributes.LeafAttributes(
				float(k), float(acx), float(sla_1), float(sla_0), float(t_sla_mid), float(yfx), float(yf0), float(tyf)
				)

			# canopy attributes
			tc = row.get('tc')
			mf = row.get('mf')
			p2 = row.get('p2')
			p20 = row.get('p20')
			ms = row.get('ms') 
			wsx1000 = row.get('wsx1000')
			nm = row.get('nm')

			canopy_attr = Species.Attributes.CanopyAttributes(
				float(tc), float(mf), float(p2), float(p20), float(ms), float(wsx1000), float(nm)
				)

			# stem attributes
			mr = row.get('mr')
			ms = row.get('ms')
			yr = row.get('yr')
			nr_min = row.get('nr_min')
			nr_max = row.get('nr_max')
			m_0 = row.get('m_0')
			ah = row.get('ah')
			nhb = row.get('nhb')
			nhc = row.get('nhc')
			ahl = row.get('ahl')
			nhlb = row.get('nhlb')
			nhlc = row.get('nhlc')
			ak = row.get('ak')
			nkb = row.get('nkb')
			nkh = row.get('nkh')
			av = row.get('av')
			nvb = row.get('nvb')
			nvh = row.get('nvh')
			nvbh = row.get('nvbh')
			aws = row.get('aws')
			nws = row.get('nws')

			stem_attr = Species.Attributes.StemAttributes(float(mr), float(ms), float(yr), float(nr_min), float(nr_max), float(m_0), float(ah),
												 float(nhb), float(nhc), float(ahl), float(nhlb), float(nhlc), float(ak), float(nkb), float(nkh),
												 float(av), float(nvb), float(nvh), float(nvbh), float(aws), float(nws))

			# habitat attributes
			t_min = row.get('t_min')
			t_opt = row.get('t_opt')
			t_max = row.get('t_max')
			kd = row.get('kd')
			n_theta = row.get('n_theta')
			c_theta = row.get('c_theta')

			hab_attr = Species.Attributes.HabitatAttributes(float(t_min), float(t_opt), float(t_max), float(kd), float(n_theta), float(c_theta))

			# general attributes
			fcax_700 = row.get('fcax_700')
			fn0 = row.get('fn0')
			nfn = row.get('nfn')
			r_age = row.get('r_age')
			n_age = row.get('n_age')
			max_age = row.get('max_age')
			kf = row.get('kf')

			gen_attr = Species.Attributes.GeneralAttributes(float(fcax_700), float(fn0), float(nfn), float(r_age), float(n_age), float(max_age), float(kf))

			attributes = Species.Attributes(leaf_attr, canopy_attr, stem_attr, hab_attr, gen_attr)
			species = Species(name, scientific_name, visual_characteristics, seeding, attributes)

			knowledge_base.append(species)
	return knowledge_base


if __name__ == '__main__':
	# example usage

	#qualities and quantities would be read in from the LLM
	qualities = Species.VisualCharacteristics('needle', 'green', 'pyramidal', 'evergreen', 'temperate', 'furrows', 'gray', 'shallow', 'medium')
	quantities = Species.OtherCharacteristics('5', '20')

	new_species = Species('Ponderosa Pine', 'Pinus ponderosa', qualities, quantities)

	kb = load_knowledge_base('test_data/species_data_kb.csv')
	for species in kb:
		species.get_basic_info()