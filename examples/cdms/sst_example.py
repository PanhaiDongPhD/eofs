"""
Compute and plot the leading EOF of sea surface temperature in the
central and northern Pacific during winter time.

The spatial pattern of this EOF is the canonical El Nino pattern, and
the associated time series shows large peaks and troughs for well-known
El Nino and La Nina events.

This example uses the metadata-retaining cdms2 interface.

"""
import cdms2
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

from eofs.cdms import Eof
from eofs.examples import example_data_path


# Read SST anomalies using the cdms2 module from CDAT. The file contains
# November-March averages of SST anomaly in the central and northern Pacific.
filename = example_data_path('sst_ndjfm_anom.nc')
ncin = cdms2.open(filename, 'r')
sst = ncin('sst')
ncin.close()

# Create an EOF solver to do the EOF analysis. Square-root of cosine of
# latitude weights are applied before the computation of EOFs.
solver = Eof(sst, weights='coslat')

# Retrieve the leading EOF, expressed as the correlation between the leading
# PC time series and the input SST anomalies at each grid point, and the
# leading PC time series itself.
eof1 = solver.eofsAsCorrelation(neofs=1)
pc1 = solver.pcs(npcs=1, pcscaling=1)

# Plot the leading EOF expressed as correlation in the Pacific domain.
m = Basemap(projection='cyl', llcrnrlon=120, llcrnrlat=-20,
        urcrnrlon=260, urcrnrlat=60)
lons, lats = eof1.getLongitude()[:], eof1.getLatitude()[:]
x, y = m(*np.meshgrid(lons, lats))
clevs = np.linspace(-1, 1, 11)
m.contourf(x, y, eof1(squeeze=True), clevs, cmap=plt.cm.RdBu_r)
m.drawcoastlines()
cb = plt.colorbar(orientation='horizontal')
cb.set_label('correlation coefficient', fontsize=12)
plt.title('EOF1 expressed as correlation', fontsize=16)

# Plot the leading PC time series.
plt.figure()
years = range(1962, 2012)
plt.plot(years, pc1, color='b', linewidth=2)
plt.axhline(0, color='k')
plt.title('PC1 Time Series')
plt.xlabel('Year')
plt.ylabel('Normalized Units')
plt.xlim(1962, 2012)
plt.ylim(-3, 3)

plt.show()

