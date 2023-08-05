import os
import numpy as np
from matplotlib import pyplot as plt
from .. import gui
from .. import datahandler
from . import interface


class JunctionEvaluation(gui.backend.Panel, interface.WorkflowStep):
    NAME = 'Evaluate'

    def __init__(self, master, workflow_data: datahandler.interface.WorkflowData):
        gui.backend.Panel.__init__(self, master=master)
        self.workflow_data = workflow_data
        self.file_versioning = datahandler.FileVersioning()
        self.plot_heigth = 350
        self.current_stack = 0
        self.left_panel = gui.backend.Panel(master=self)
        self.config = datahandler.Config(panel_name='')
        self.config.new_item(name='Result type', value=0, options=self._get_options(), on_change=self.update_everything)
        self.config_panel = gui.backend.ConfigPanel(master=self.left_panel, config=self.config)
        self.config_panel.show(side=gui.interface.TOP)
        self.perf_junction_panel = gui.backend.Panel(master=self.left_panel)
        self.perf_junction_panel.add_label('Junction stats:')
        self.perf_junction = gui.backend.Text(master=self.perf_junction_panel)
        self.perf_junction.show(side=gui.interface.LEFT)
        self.perf_summary_panel = gui.backend.Panel(master=self.left_panel)
        self.perf_summary_panel.add_label('Total stats:')
        self.perf_summary = gui.backend.Text(master=self.perf_summary_panel)
        self.perf_summary.show(side=gui.interface.LEFT)
        self.left_panel.show(side=gui.interface.LEFT, fill=gui.interface.Y, expand=gui.interface.ON)
        self.single_stack_container = gui.backend.Panel(master=self)
        self.single_stack_container.add_label('Individual Stack Results')
        self.single_plots = None
        self.single_plots_compare = None
        self.controls = gui.backend.StackControls(master=self.single_stack_container, callback=self.update_frame)
        self.single_stack_container.show(side=gui.interface.TOP, pady=5)
        self.combined_container = gui.backend.Panel(master=self)
        self.combined_container.add_label('Combined Results')
        self.combined_plots = None
        self.combined_plots_compare = None
        self.combined_container.show(side=gui.interface.TOP, pady=5)
        self.force_update = False
        self.update()
        # TODO: (prio 2) configure junction types

    @property
    def input(self):
        '''Input data to be processed'''
        return (self.workflow_data.annotation, self.workflow_data.pred_med, self.workflow_data.pred_std, self.workflow_data.pred_corr)

    @property
    def output(self):
        '''Output data after processing'''
        return None

    def update(self, _=None):
        if self.is_ready():
            self.create_figures()

    def update_frame(self, _=None):
        if self.can_compare():
            self.perf_junction.update(text=self._format_performance(
                self.workflow_data.pred_med[self.controls.frame], self.workflow_data.pred_corr[self.controls.frame]))
        if self.config['Result type'].current_option == 'compare':
            self.single_plots_compare.update(self.controls.frame)
        else:
            self.single_plots.update(self.controls.frame)

    def create_figures(self):
        if self.single_plots is None:
            self.single_plots = gui.backend.EvalPlotJunctions(
                master=self.single_stack_container, data=self.workflow_data.annotation, height=self.plot_heigth)
            self.combined_plots = gui.backend.EvalPlots(
                master=self.combined_container, data=self.workflow_data.annotation, height=self.plot_heigth)
        if self.can_compare():
            self.create_compare()
        self.single_plots.show(side=gui.interface.TOP)
        self.controls.show(side=gui.interface.TOP, fill=gui.interface.X, expand=gui.interface.ON)
        self.combined_plots.show(side=gui.interface.TOP)
        self.update_everything()

    def create_compare(self):
        if self.single_plots_compare is None:
            self.single_plots_compare = gui.backend.CompareEvalPlotJunctions(
                master=self.single_stack_container, data=self.workflow_data.pred_med, compare=self.workflow_data.pred_corr, height=self.plot_heigth, labels=['predictions', 'corrected'])
            self.combined_plots_compare = gui.backend.CompareEvalPlots(
                master=self.combined_container, data=self.workflow_data.pred_med, compare=self.workflow_data.pred_corr, height=self.plot_heigth, labels=['predictions', 'corrected'])

    def update_everything(self, _=None):
        self.config['Result type'].options = self._get_options()
        if self.config['Result type'].current_option == 'annotations':
            self.combined_plots.update(self.workflow_data.annotation)
            self.single_plots.data = self.workflow_data.annotation
            self.controls.max_frame = len(self.workflow_data.annotation) - 1
            self.perf_junction_panel.hide()
            self.perf_summary_panel.hide()
        elif self.config['Result type'].current_option == 'predictions':
            self.combined_plots.update(self.workflow_data.pred_med)
            self.single_plots.data = self.workflow_data.pred_med
            self.controls.max_frame = len(self.workflow_data.pred_med) - 1
            if self.can_compare():
                self.perf_summary.update(text=self._format_performance())
                self.perf_summary_panel.show(side=gui.interface.BOTTOM, pady=150)
                self.perf_junction_panel.show(side=gui.interface.TOP, pady=90)
        elif self.config['Result type'].current_option == 'corrected predictions':
            self.combined_plots.update(self.workflow_data.pred_corr)
            self.single_plots.data = self.workflow_data.pred_corr
            self.controls.max_frame = len(self.workflow_data.pred_corr) - 1
            self.controls.hide()
            self.single_plots_compare.hide()
            self.combined_plots_compare.hide()
            self.single_plots.show(side=gui.interface.TOP)
            self.controls.show(side=gui.interface.TOP, fill=gui.interface.X, expand=gui.interface.ON)
            self.combined_plots.show(side=gui.interface.TOP)
        elif self.config['Result type'].current_option == 'compare':
            if self.single_plots_compare is None:
                self.create_compare()
            self.combined_plots_compare.update(data=self.workflow_data.pred_med, compare=self.workflow_data.pred_corr)
            self.controls.hide()
            self.single_plots.hide()
            self.combined_plots.hide()
            self.single_plots_compare.show(side=gui.interface.TOP)
            self.controls.show(side=gui.interface.TOP, fill=gui.interface.X, expand=gui.interface.ON)
            self.combined_plots_compare.show(side=gui.interface.TOP)
            self.controls.max_frame = len(self.workflow_data.pred_med) - 1
        self.update_frame()

    def is_ready(self):
        '''Check if this step is ready to be run.'''
        return not self.workflow_data.annotation.empty()

    def is_done(self):
        '''Check if this step is done and ready for the next step.'''
        return not self.workflow_data.annotation.empty()

    def can_compare(self):
        return not self.workflow_data.pred_med.empty() and not self.workflow_data.pred_corr.empty() and len(self.workflow_data.pred_med) == len(self.workflow_data.pred_corr)

    def load_input(self):
        '''Ask user for data path and load input.'''
        if self.workflow_data.path is None:
            fd = gui.backend.Filedialog()
            self.workflow_data.path = fd.ask_open(filetypes=([]))
        path = self.default_in_file()
        try:
            self.workflow_data.annotation.load(self.file_versioning.get_newest_file(path[0]))
            self.workflow_data.pred_med.load(self.file_versioning.get_newest_file(path[1]))
            self.workflow_data.pred_std.load(self.file_versioning.get_newest_file(path[2]))
            self.workflow_data.pred_corr.load(self.file_versioning.get_newest_file(path[3]))
        except TypeError:
            pass
        self.update()

    def save_output(self):
        '''Ask user for data path and save output.'''
        pass

    def default_in_file(self):
        '''Calculate default input file path relative to path.
        Arguments:
        path: string path of original file
        Returns:
        string: default output file path
        '''
        paths = (os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_annotations.npz'),
                 os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_predicted_mean.npz'),
                 os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_predicted_std.npz'),
                 os.path.join(datahandler.get_eval_dir(self.workflow_data.path), 'junction_predicted_manual_corrected.npz'))
        return paths

    def default_out_file(self):
        '''Calculate default output file path relative to path.
        Arguments:
        path: string path of original file
        Returns:
        string: default output file path
        '''
        pass

    def _get_options(self):
        options = ['annotations']
        if not self.workflow_data.pred_med.empty():
            options.append('predictions')
        if not self.workflow_data.pred_corr.empty():
            options.append('corrected predictions')
        if self.can_compare():
            options.append('compare')
        return options

    def _format_performance(self, pred=None, corr=None, threshold=0.1):
        if pred is not None and corr is not None:
            pr = (pred > threshold).astype(np.float32)
            cor = (corr > threshold).astype(np.float32)
            dice = datahandler.loss.dice_coe(pr, cor, axis=(0, 1))
        else:
            pr = (np.concatenate(self.workflow_data.pred_med) > threshold).astype(np.float32)
            cor = (np.concatenate(self.workflow_data.pred_corr) > threshold).astype(np.float32)
            dice = np.median(np.array([datahandler.loss.dice_coe(p, c, axis=(0, 1))
                                       for p, c in zip(self.workflow_data.pred_med, self.workflow_data.pred_corr)]))
        return 'Dice coefficient: {:.3f}\nTotal predicted: {:d}\nTotal corrected: {:d}\nPercent detected: {:.1f}%'.format(dice, int(np.sum(pr)), int(np.sum(cor)), np.sum(pr)/np.sum(cor) * 100)
