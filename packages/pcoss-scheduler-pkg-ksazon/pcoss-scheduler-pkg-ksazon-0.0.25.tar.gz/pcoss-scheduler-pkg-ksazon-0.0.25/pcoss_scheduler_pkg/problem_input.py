from typing import Dict, List, Set, Tuple

import pandas as pd
import toml

import pcoss_scheduler_pkg.constants as c
import pcoss_scheduler_pkg.helpers as h


class ProblemInput:
    def __init__(self, init_dict: Dict):
        if 'index_cols' in init_dict['problem_data']:
            self.index_cols = init_dict['problem_data']['index_cols']
        else:
            self.index_cols = []
        
        if 'grouping_cols' in init_dict['problem_data']:
            self.grouping_cols = init_dict['problem_data']['grouping_cols']
        else:
            self.grouping_cols = []
        if 'grouping_func_name' in init_dict['problem_data']:
            self.grouping_func_name = init_dict['problem_data']['grouping_func_name']
        else:
            self.grouping_func_name = None
        if bool(self.grouping_cols) != bool(self.grouping_func_name):
            raise Exception('If grouping is used, both `grouping_func_name` and `grouping_cols` have to be filled in `problem_data` group')

        if 'conflicting_machines' in init_dict['problem_data']:
            self.conflicting_machines_list = init_dict['problem_data']['conflicting_machines']
        else:
            self.conflicting_machines_list = []
        
        if 'base_url' in init_dict['problem_data']:
            self.base_url = init_dict['problem_data']['base_url']
        else:
            raise Exception('Parameter `base_url` in `problem_data` group is needed')
        
        if 'algorithm_name' in init_dict['algorithm_config']:
            self.algorithm = init_dict['algorithm_config']['algorithm_name']
        else:
            self.algorithm = None
        if 'objective' in init_dict['algorithm_config']: 
            self.objective = init_dict['algorithm_config']['objective']
        else:
            self.objective = None
        if 'beam_width' in init_dict['algorithm_config']: 
            self.beam_width = init_dict['algorithm_config']['beam_width']
        else:
            self.beam_width = None

        if 'print_responses' in init_dict['display_config']: 
            self.print_responses = init_dict['display_config']['print_responses']
        else:
            self.print_responses = c.PRINT_RESPONSES
        if 'print_method_times' in init_dict['display_config']:
            self.print_method_times = init_dict['display_config']['print_method_times']
        else:
            self.print_method_times = c.PRINT_METHOD_TIMES
        if 'show_conflict_graph' in init_dict['display_config']:
            self.show_conflict_graph = init_dict['display_config']['show_conflict_graph']
        else:
            self.show_conflict_graph = c.SHOW_CONFLICT_GRAPH
        if 'show_result_schedule_graph' in init_dict['display_config']:
            self.show_result_schedule_graph = init_dict['display_config']['show_result_schedule_graph']
        else:
            self.show_result_schedule_graph = c.SHOW_RESULT_SCHEDULE_GRAPH
        if 'show_gantt_plot' in init_dict['display_config']:
            self.show_gantt_plot = init_dict['display_config']['show_gantt_plot']
        else:
            self.show_gantt_plot = c.SHOW_GANTT


        self.table_in = pd.read_csv(
            init_dict['files']['data'],
            index_col=self.index_cols,
            header=None,
            )

        self.column_operation_dict = {}
        avaliable_operations_list = ['A', 'B', 'C']

        use_operation_num = 0

        for cm in self.conflicting_machines_list:
            self.column_operation_dict[cm[0]] = avaliable_operations_list[use_operation_num]
            self.column_operation_dict[cm[1]] = avaliable_operations_list[use_operation_num]
            use_operation_num = (use_operation_num + 1) % 3

        for col_num in range(len(self.table_in.columns)):
            if col_num not in [cm for te in self.conflicting_machines_list for cm in te]:
                self.column_operation_dict[col_num] = '0'

        job_cnt, machine_cnt = self.table_in.shape

        if self.grouping_cols:
            job_cnt = len(self.table_in.groupby(self.grouping_cols))

        self.conflict_graph_in = (
            h.create_conflict_graph_from_cnts_and_conflicting_machine_list(
                job_cnt=job_cnt,
                machine_cnt=machine_cnt,
                conflicting_machines=self.conflicting_machines_list,
                show=self.show_conflict_graph))

        if 'processing_times' in init_dict['files']:
            self.processing_times = pd.read_csv(
                init_dict['files']['processing_times'],
                index_col=self.index_cols,
                header=None,
                ) + c.DEFAULT_ADDED_TIME_MS
        
        else:
            self.processing_times = None
        
        if 'complexity_list' in init_dict['problem_data']:
            self.complexity_list = list(map(eval, init_dict['problem_data']['complexity_list']))
        else:
            self.complexity_list = None

    @classmethod
    def from_toml(cls, toml_file: str):
        config_dict = toml.load(toml_file)
        
        config_dict['problem_data']['conflicting_machines'] = list(
            map(tuple, config_dict['problem_data']['conflicting_machines'])
            )
        
        return cls(config_dict)
