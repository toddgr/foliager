"""
File name: test_threepg.py
Author: Grace Todd
Date: February 28, 2024
Description: This file tests out the 3-PG implementation in threepg.py using Douglas Fir species data.
             Before I start working on the data estimation agent, I need to make sure that the trees
             are actually growing/dying how I expect them to be.
"""

from threepg import compute, TreeViz, Month
from plot_trees_random import init_trees

speciesdata_filename = 'test_data/douglas_fir_species_data.csv'
climatedata_filename = 'test_data/sample_climate_data.csv'  # Create this
"""
    CLIMATE DATA FILE -- REQUIREMENTS FROM ALLISON 3-PG
    Should be able to pull this sample climate data from Allison's code
    Must include:
        // monthly climate data
        struct month monthdata[13]          i.e. a list of month data for each of the 12 months of the year
        struct month initmonthdata[13]      i.e. the list of month data for the first year?

        // for modding sliders -- I don't use sliders in this implementation (yet?), but Allison does
        // these all correspond to the attributes in the MONTH class
        site_tmax_mod = 0.
        site_tmin_mod = 0.
        site_rain_mod = 0.
        site_solar_rad_mod = 0.
        site_frost_days_mod = 0.

        // temperature-- all in degrees C
        -- float ta -- mean monthly temperature -> shouldn't need anymore (C code)
        t_min -> minimum monthly temperature for growth
        t_opt -> optimum monthly temperature for growth */
        t_max -> maximum monthly temperature for growth */

        // frost */
        df -> mean number of frost days per month */
        kf -> number of days of production lost for each frost day */

        // CO2 */
        fcax_700 -> this one is the "assimilation enhancement factor at 700 ppm" "parameter[s] define the species specific repsonses to changes in atmospheric co2" */
        co2 -> atmospheric CO2 (ppm) -- number from oregon values from random site, change later */

        /* VPD */
        d -> mean daytime VPD */
        kd -> "defines the stomatal response to VPD" */

        /* soil water mod, and other soil stuff */
        soilwater -> available soil water */
        maxsoilwater -> maximum available soil water */
        n_theta -> "power of moisture ratio deficit" "differences in the relationship between transpiration rate and soil water content for different soil textures" */
        c_theta -> "moisture ratio deficit for fq = 0.5 */
"""