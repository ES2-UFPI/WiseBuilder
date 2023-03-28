import pandas as pd
import sys, os

from framework.domain.value_object import UUID

from ..domain.repositories import IDataFrameRepository

sys.path.insert(0, os.getcwd())


class DataFrameRepository(IDataFrameRepository):
    def __init__(self, path):
        self.cpus = self._import_df(f"{path}/cpu.json")
        self.gpus = self._import_df(f"{path}/gpu.json")
        self.psus = self._import_df(f"{path}/psu.json")
        self.rams = self._import_df(f"{path}/ram.json")
        self.hdds = self._import_df(f"{path}/hdd.json")
        self.ssds = self._import_df(f"{path}/ssd.json")
        self.motherboards = self._import_df(f"{path}/motherboard.json")

        from polyfuzz import PolyFuzz
        from polyfuzz.models import TFIDF

        tfidf_vec = TFIDF(n_gram_range=(3, 3), clean_string=True)
        self.tfidf = PolyFuzz(tfidf_vec)

        idx = ["uid", "model"]
        self.all = pd.concat(
            [
                self.cpus[idx],
                self.gpus[idx],
                self.psus[idx],
                self.rams[idx],
                self.hdds[idx],
                self.ssds[idx],
                self.motherboards[idx],
            ]
        )

    def _import_df(self, path):
        from thefuzz.utils import full_process

        print(path)
        df = pd.read_json(path)
        df.set_index("uid")
        df.model = df.model.apply(lambda x: full_process(x))

        return df

    def _add(self, component):
        pass

    def _get_by_uid(self, ref: UUID):
        pass

    def _get(self, **kwargs):
        pass
