import asyncio
# import sched
import time
from dataclasses import asdict
from typing import Dict, List, Tuple

import aiohttp
import networkx as nx
import numpy as np
import pandas as pd

import pcoss_scheduler_pkg.algorithms as a
import pcoss_scheduler_pkg.constants as c
import pcoss_scheduler_pkg.helpers as h
import pcoss_scheduler_pkg.operations as o
from pcoss_scheduler_pkg.problem_input import ProblemInput


class Scheduler:
    def __init__(self, problem_input: ProblemInput):
        self.problem_input = problem_input

        self.table: pd.DataFrame = problem_input.table_in
        self._table = self.table
        # use_cols = [c for c in self.table.columns if c not in self.problem_input.grouping_cols]
        # self._table: pd.DataFrame = self.table[use_cols].to_numpy()
        self.row_grouping_func = h.id_func
        self.cloumn_grouping_func = h.id_func
        self.column_operation_dict: Dict = {}
        self.conflict_graph: nx.Graph = None
        self._conflict_graph: nx.Graph = None
        self.processing_times: pd.DataFrame = None
        self._processing_times: pd.DataFrame = None
        
        self.algorithm = None
        self.objective = c.DEFAULT_OBJECTIVE
        self.beam_witdh = c.DEFAULT_BEAM_WIDTH

        self.schedule: List[h.scheduled_operation] = []
        
        self._session = aiohttp.ClientSession()

    def _find_best_algorithm(self):
        if self.algorithm:
            return
        
        self.algorithm = c.DEFAULT_ALGORITHM

    def _group_rows(self):
        self._table = self.row_grouping_func(self._table)

    def _group_columns(self):
        self._table = self.cloumn_grouping_func(self._table)

    def _convert_to_numpy(self):
        self._table = self._table.to_numpy()

    def _fill_times(self):
        if self.problem_input.processing_times is not None:
            self._processing_times = self.processing_times.to_numpy()
            return

        if self.problem_input.complexity_list:
            vc = self.table.groupby(self.problem_input.grouping_cols).count()
            for col, f in zip(vc, self.problem_input.complexity_list):
                vc[col] = vc[col].apply(f)
            self._processing_times = vc.to_numpy() + c.DEFAULT_ADDED_TIME_MS
            return
        
        self._processing_times = self._assses_aproximate_execution_times()

    def _assses_aproximate_execution_times(self):
        raise NotImplementedError('Aproximate execution times not implemented')

    @h.get_func_exec_time_decorator
    def _prepare_data(self):
        self._group_rows()
        self._group_columns()
        self._convert_to_numpy()
        self._fill_times()
        self._find_best_algorithm()

        assert self._processing_times.shape == self._table.shape, f'Shape of (grouped) data: {self._table.shape} is different than shape of processing times {self._processing_times.shape}'
    
    @h.get_func_exec_time_decorator
    def _prepare_schedule(self):
        self.schedule = (
            a.ALGORITHM_CLASS_DICT[self.algorithm]
            (self._processing_times, self.conflict_graph, self.problem_input)
            .run()
        )

    def prepare(self):
        self._prepare_data()
        self._prepare_schedule()

    async def run(self):
        t0 = time.perf_counter()

        al = []
        for so in self.schedule:
            so.endpoint = '0' 
            so.item = self._table[so.job][so.machine]
            
            al.append(o.operation(so, self._session, t0))
            
        t1 = time.perf_counter()
        await asyncio.gather(*al)
        t2 = time.perf_counter()
        try:
            await self._session.close()
        except Exception as e:
            pass
        t3 = time.perf_counter()
        if c.PRINT_DEBUG_MESSSAGES:
            print(f't1-t0: {t1-t0}\tt2-t1: {t2-t1}\tt3-t2: {t3-t2}\tt3-t0: {t3-t0}')

    @classmethod
    def from_ProblemInput(cls, problem_input: ProblemInput):
        # s = cls(problem_input.table_in)
        s = cls(problem_input)

        # s.problem_input = problem_input
        if problem_input.column_operation_dict:
            s.column_operation_dict = problem_input.column_operation_dict
        if problem_input.conflict_graph_in:
            s.conflict_graph = problem_input.conflict_graph_in
        if problem_input.processing_times is not None and not problem_input.processing_times.empty:
            s.processing_times = problem_input.processing_times
        if problem_input.algorithm:
            s.algorithm = problem_input.algorithm
        if problem_input.objective:
            s.objective = problem_input.objective
        if problem_input.beam_width:
            s.beam_width = problem_input.beam_width
        if problem_input.grouping_cols:
            s.row_grouping_func = lambda t: h.grouping(
                t,
                problem_input.grouping_cols,
                problem_input.grouping_func_name)

        return s
