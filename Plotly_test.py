import plotly.express as px
import pandas as pd
from LoadSpectrum import read_spa
import numpy as np
import plotly.graph_objects as go
import pathlib
from matplotlib import pyplot as plt
#https://github.com/lerkoah/spa-on-python
path='templates/cy785lo.SPA'
path2='templates/naph785lo.SPA'
path2='templates/Acetominophen Caffeine Acetylsalicylic acid.SPA'


spectra_tmp, wavelength_tmp, title_tmp = read_spa(path2)
#spectra_tmp2, _, _ = read_spa(path2)
#spectra_tmp2=np.nan_to_num(spectra_tmp2, copy=True, nan=0.0, posinf=None, neginf=None)
graph=[spectra_tmp,spectra_tmp,spectra_tmp,spectra_tmp]
df=pd.DataFrame(graph)
fig =go.Figure(data=[go.Surface(z=df.values)])
fig.show()