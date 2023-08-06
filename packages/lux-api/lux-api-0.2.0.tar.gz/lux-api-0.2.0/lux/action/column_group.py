#  Copyright 2019-2020 The Lux Authors.
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import lux
from lux.interestingness.interestingness import interestingness
from lux.processor.Compiler import Compiler
from lux.utils import utils

from lux.vis.Vis import Vis
from lux.vis.VisList import VisList
import pandas as pd

def column_group(ldf):
	recommendation = {"action":"Column Groups",
					"description":"Shows charts of possible visualizations with respect to the column-wise index."}
	collection = []
	ldf_flat = ldf
	if isinstance(ldf.columns,pd.DatetimeIndex):
		ldf_flat.columns = ldf_flat.columns.format()
	ldf_flat = ldf_flat.reset_index() #use a single shared ldf_flat so that metadata doesn't need to be computed for every vis
	if (ldf.index.nlevels==1):
		index_column_name = ldf.index.name
		if isinstance(ldf.columns,pd.DatetimeIndex):
			ldf.columns = ldf.columns.to_native_types()
		for attribute in ldf.columns:
			vis = Vis([index_column_name,lux.Clause(str(attribute),aggregation=None)],ldf_flat)
			collection.append(vis)
	vlst = VisList(collection)
	# Note that we are not computing interestingness score here because we want to preserve the arrangement of the aggregated ldf
	
	recommendation["collection"] = vlst
	return recommendation