class Species:
    """
    Holds information about a specific species.
    Takes in data collected by parameter estimator

    TODO break up the local variables into smaller, identifiable classes
    TODO adding masting cycle to this might have messed everything up
    """
    def __init__(self, name, name_scientific,leaf_shape, canopy_density, deciduous_evergreen,
                 leaf_color, tree_form, tree_roots, habitat, bark_texture, bark_color, masting_cycle, t_min=0,
                 t_opt=0, t_max=0, kf=0, fcax_700=0, kd=0, n_theta=0, c_theta=0,p2=0, p20=0, acx=0,
                 sla_1=0, sla_0=0, t_sla_mid=0, fn0=0, nfn=0, tc=0, max_age=0, r_age=0, n_age=0,
                 mf=0, mr=0, ms=0, yfx=0, yf0=0, tyf=0, yr=0, nr_max=0, nr_min=0, m_0=0, wsx1000=0,
                 nm=0, k=0, aws=0, nws=0, ah=0, nhb=0, nhc=0, ahl=0, nhlb=0, nhlc=0, ak=0, nkb=0,
                 nkh=0, av=0, nvb=0, nvh=0, nvbh=0,):
        """
        Attributes are a combination of LLM responses (qualitative) 
        and parameter estimation (quantitative)
        Input from parameter estimation function output, 
        quantitative values default to 0 if not found
        """
        self.name:str = name
        self.name_scientific:str = name_scientific

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

        self.masting_cycle = masting_cycle

        # Estimated from knowledge base:
        self.t_min = float(t_min) # Minimum temperature for growth
        self.t_opt = float(t_opt)
        self.t_max = float(t_max)
        self.kf = float(kf)
        self.fcax_700 = float(fcax_700)
        self.kd = float(kd)
        self.n_theta = float(n_theta)
        self.c_theta = float(c_theta)
        self.p2 = float(p2)
        self.p20 = float(p20)
        self.acx = float(acx)
        self.sla_1 = float(sla_1)
        self.sla_0 = float(sla_0)
        self.t_sla_mid = float(t_sla_mid)
        self.fn0 = float(fn0)
        self.nfn = float(nfn)
        self.tc = float(tc)
        self.max_age = float(max_age)
        self.r_age = float(r_age)
        self.n_age = float(n_age)
        self.mf = float(mf)
        self.mr = float(mr)
        self.ms = float(ms)
        self.yfx = float(yfx)
        self.yf0 = float(yf0)
        self.tyf = float(tyf)
        self.yr = float(yr)
        self.nr_max = float(nr_max)
        self.nr_min = float(nr_min)
        self.m_0 = float(m_0)
        self.wsx1000 = float(wsx1000)
        self.nm = float(nm)
        self.k = float(k)
        self.aws = float(aws)
        self.nws = float(nws)
        self.ah = float(ah)
        self.nhb = float(nhb)
        self.nhc = float(nhc)
        self.ahl = float(ahl)
        self.nhlb = float(nhlb)
        self.nhlc = float(nhlc)
        self.ak = float(ak)
        self.nkb = float(nkb)
        self.nkh = float(nkh)
        self.av = float(av)
        self.nvb = float(nvb)
        self.nvh = float(nvh)
        self.nvbh = float(nvbh)

        # Data calculated from 3-PG
        self.b = 0


    def get_basic_info(self):
        """
        Prints the qualitative data about a tree species. Just for fun, but also for fact checking.
        """
        print(f'\n========== {self.name} ({self.name_scientific}) ===========')
        print(f'{self.name} are a {self.deciduous_evergreen[0]} species, \
and are commonly found in {", ".join(self.habitat)} climates.')
        print(f'FOLIAGE: {self.name} tend to have a {", ".join(self.tree_form)} form, \
with {", ".join(self.leaf_color)}, {", ".join(self.leaf_shape)}-type leaves.')
        print(f'WOOD: The bark of {self.name} have a {" or ".join(self.bark_texture)} texture \
and tend to be {" and ".join(self.bark_color)} in color.\n')