#   Copyright 2019 AUI, Inc. Washington DC, USA
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

########################
def statistics(xds, dv='IMAGE', mode='classic'):
    """
    Generate statistics on specified image data contents
    
    Resulting data is placed in the attributes section of the dataset

    Parameters
    ----------
    xds : xarray.core.dataset.Dataset
        input Image Dataset
    dv : str
        name of data_var in xds to compute statistics on. Default is 'IMAGE'
    mode : str
        algorithm mode to use ('classic', 'fit-half', 'hinges-fences', 'chauvenet', 'biweight'). Default is 'classic'
    
    Returns
    -------
    xarray.core.dataset.Dataset
        output Image
    """
    return xds