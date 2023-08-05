import pandas as pd
from pandashape import Columns
from pandashape.describers import GeneralDescriber, DistributionDescriber, DTypesDescriber
from pandashape.internal import DescriberExecutor, TransformerExecutor


class PandaShaper:
    def __init__(self, df, inplace=False):
        assert(isinstance(df, pd.DataFrame))
        self.df = df.copy() if not inplace else df

    def describe(self, describers=[GeneralDescriber, DTypesDescriber, DistributionDescriber], columns=Columns.All):
        executor = DescriberExecutor()
        executor.describe(self.df, describers, columns)

    def transform(self, columnDefinitions):
        executor = TransformerExecutor()
        return executor.transform(self.df, columnDefinitions)
