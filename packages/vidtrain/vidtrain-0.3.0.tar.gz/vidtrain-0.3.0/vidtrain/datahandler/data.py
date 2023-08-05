import re
import copy
import os
import pathlib
import glob
import collections
import warnings
from time import strftime
import numpy as np
import pandas as pd
import micdata
from . import interface
from . import config
from . import models


def get_eval_dir(path):
    (dirname, basename) = os.path.split(path)
    (name, _) = os.path.splitext(basename)
    if dirname[-5:] == '_eval':
        evaldir = dirname
    else:
        evaldir = os.path.join(dirname, name + '_eval')
    pathlib.Path(evaldir).mkdir(parents=True, exist_ok=True)
    return evaldir


class ImageStack(interface.ImageStack):
    def __init__(self, data=None, normalizer=micdata.formatting.StackNormalizer()):
        self.normalizer = normalizer
        self.data = data
        self.flatten_formatter = micdata.formatting.ParallelFlattener(function=np.median, kw={'axis': 0})

    @property
    def data(self):
        '''the raw data'''
        return self._data

    @data.setter
    def data(self, data):
        if data is not None:
            assert isinstance(data, np.ndarray)
            if data.ndim == 2:
                data = data[np.newaxis, :, :, np.newaxis]
            elif data.ndim == 3:
                data = data[..., np.newaxis]
            assert data.ndim == 4
            data = self.normalizer.apply(data)
        self._data = data

    @property
    def num_slices(self):
        '''return: int: number of images in the stack'''
        return self.data.shape[0]

    @property
    def width(self):
        '''return: int: width of each image in pixels'''
        return self.data.shape[1]

    @property
    def height(self):
        '''return: int: height of each image in pixels'''
        return self.data.shape[2]

    @property
    def image_shape(self):
        '''return: tuple: shape of each image in pixels'''
        return self.data.shape[1:]

    @property
    def num_channels(self):
        '''return: int: number of color channels of each image'''
        return self.data.shape[3]

    def load(self, path):
        self.data = micdata.io.IOFactory(path).load()

    def save(self, path):
        if self.data is not None:
            micdata.io.IOFactory(path).write(self.data, ext='.tif')

    def median(self):
        '''return: 2D np.ndarray: median projection of the stack'''
        self.flatten_formatter.parameters['function'] = np.median
        return np.squeeze(self.flatten_formatter.apply(self.data))

    def mean(self):
        '''return: 2D np.ndarray: mean projection of the stack'''
        self.flatten_formatter.parameters['function'] = np.mean
        return np.squeeze(self.flatten_formatter.apply(self.data))

    def std(self):
        '''return: 2D np.ndarray: standard deviation projection of the stack'''
        self.flatten_formatter.parameters['function'] = np.std
        return np.squeeze(self.flatten_formatter.apply(self.data))

    def max(self):
        '''return: 2D np.ndarray: maximum projection of the stack'''
        return np.squeeze(np.max(self.data, axis=0))

    def copy_tile(self, pos, dim):
        '''copy a tile out of the stack.
        Arguments:
        tuple pos: x and y coordinates
        typle dim: wdth and height of the tile
        return: 4D np.ndarray: copy a part of the stack or None if the tile does not fit onto the stack'''
        tile = np.copy(self.data[:, pos[1]: pos[1] + dim[1], pos[0]: pos[0] + dim[0], :])
        if tile.shape[1:3] < dim:
            raise IndexError
        return tile

    def empty(self):
        return self.data is None or self.data.size == 0


class MultiImageStack(interface.MultiImageStack):
    '''many image stacks stored as collections.MutableSequence'''

    def __init__(self, *args, positions=[]):
        self.data = list(args)
        if len(positions) == len(self.data):
            self.positions = self._parse_all_pos(positions)
        else:
            self.positions = [None] * len(self.data)

    @property
    def names(self):
        return ['x:{:04d} y:{:04d}'.format(pos[0], pos[1]) if isinstance(pos, tuple) else str(i) for i, pos in enumerate(self.positions)]

    def __len__(self): return len(self.data)

    def __getitem__(self, i):
        return self.data[i]

    def __setitem__(self, i, v: tuple):
        self._check(v)
        self.data[i] = v[0]
        self.positions[i] = self._parse_pos(v[1])

    def __delitem__(self, i):
        del self.data[i]
        del self.positions[i]

    def __iter__(self):
        yield from self.data

    def __add__(self, other: interface.MultiImageStack):
        self.data += other.data
        self.positions += other.positions
        return self

    def insert(self, i, v: tuple):
        self._check(v)
        self.data.insert(i, v[0])
        self.positions.insert(i, self._parse_pos(v[1]))

    def get_position(self, i):
        return self.positions[i]

    def append(self, stack, position):
        self.data.append(stack)
        self.positions.append(position)

    def np_array(self):
        '''return an ndarray from data.values. only works if the shape of all values is the same'''
        return np.array(self.data)

    def image_stacks(self, i=None):
        '''return a generator that yields ImageStacks.
        if i is provided, an individual ImageStack is created from the data corresponding to that index.
        '''
        if i is None:
            return (ImageStack(data=v) for v in self.data)
        return ImageStack(data=self.data[i])

    def update_from(self, template: interface.MultiImageStack):
        self.data = template.data
        self.positions = template.positions

    def load(self, path):
        assert path[-4:] == '.npz', 'File must be a .npz file. Got {}'.format(path)
        data = dict(np.load(path, allow_pickle=False))
        try:
            self.positions = self.load_positions(path)
        except FileNotFoundError:
            self.positions = self._parse_all_pos(data.keys())
        self.data = list(data.values())

    def load_positions(self, path):
        with open(self._positions_file(path), 'r') as f:
            return self._parse_all_pos(f.read().splitlines())

    def save(self, path):
        np.savez_compressed(path, *self.data)
        with open(self._positions_file(path), 'w') as f:
            for pos in self.positions:
                f.write(str(pos) + '\n')

    def empty(self):
        return len(self.data) == 0

    def copy(self):
        return copy.deepcopy(self)

    def from_dict(self, d: dict):
        self.data = list(d.values())
        self.positions = self._parse_all_pos(d.keys())

    def clear(self):
        self.data = []
        self.positions = []

    def _parse_pos(self, pos):
        if isinstance(pos, tuple):
            return pos
        if pos is None:
            return None
        x = y = False
        if pos[0] == '(' or pos[0] == '[':
            x = re.search(r'[\(\[](\d+),', pos)
            y = re.search(r',\s*(\d+)[\)\]]', pos)
        if pos[0] == 'x' or pos[0] == 'y':
            x = re.search(r'x:(\d+)', pos)
            y = re.search(r'y:(\d+)', pos)
        if x and y:
            return (int(x.group(1)), int(y.group(1)))
        return None

    def _parse_all_pos(self, pos_list):
        return [self._parse_pos(p) for p in pos_list]

    def _positions_file(self, path):
        return path + '.positions'

    def _check(self, v):
        assert len(v) == 2, 'value must be a tuple of length 2: (data: np.ndarray, position: tuple or None). Got {}.'.format(str(v))
        assert isinstance(v[0], np.ndarray)


class ImageStackClassification(interface.ImageStackClassification):
    def __init__(self, data=None, category_names=None):
        self.data = data
        self.category_names = category_names or []
        self.force = False

    @property
    def data(self):
        '''the raw data'''
        return self._data

    @data.setter
    def data(self, data: np.ndarray):
        if data is not None:
            assert isinstance(data, np.ndarray)
            assert data.ndim == 2
        self._data = data

    @property
    def category_names(self):
        n = 0
        while n < self.num_categories:
            try:
                yield self._category_names[n]
            except IndexError:
                yield 'cat {}'.format(n)
            n += 1

    @category_names.setter
    def category_names(self, names):
        self._category_names = names

    @property
    def num_slices(self):
        '''return: int: number of images in the stack'''
        return self.data.shape[0]

    @property
    def num_categories(self):
        '''the number of categories'''
        return self.data.shape[1]

    @num_categories.setter
    def num_categories(self, categories):
        if self.num_categories < categories:
            self.data = np.pad(self.data, ((0, 0), (0, categories - self.num_categories)))
        elif self.num_categories > categories:
            if np.any(self.data[:, categories:] != 0) and not self.force:
                raise interface.VidtrainDataLossException(
                    'Reducing the number of categories will lead to data loss. Add force=True to override this error.')
            self.data = self.data[:, : categories]
            self.force = False

    def load(self, path):
        assert path[-4:] == '.npz', 'File must be a .npz file. Got {}'.format(path)
        with np.load(path, allow_pickle=False) as loaded:
            self.data = loaded['arr_0']

    def save(self, path):
        np.savez_compressed(path, self.data)

    def empty(self):
        return len(self.data) == 0


class MultiImageStackClassification(MultiImageStack, interface.MultiImageStackClassification):
    def __init__(self, multi_image_stack=None, num_categories=6, all_category_names=['A1', 'A2', 'B1', 'B2', 'detach', 'land', 'AB', 'BA', 'AA', 'BB', '1A', '1B', '2A', '2B', '12', '21', '11', '22']):
        self.data = []
        self._num_categories = num_categories
        self.all_category_names = all_category_names
        self.force = False
        if multi_image_stack is not None:
            self.create_from_multi_image_stack(multi_image_stack)

    @property
    def category_names(self):
        n = 0
        while n < self.num_categories:
            try:
                yield self.all_category_names[n]
            except IndexError:
                yield 'cat {}'.format(n)
            n += 1

    @category_names.setter
    def category_names(self, names):
        self.all_category_names = names

    @property
    def num_categories(self):
        '''the number of categories'''
        return self._num_categories

    @num_categories.setter
    def num_categories(self, categories):
        if self._num_categories != categories:
            self._test_data_loss(categories)
            self._num_categories = categories
            for i, data in enumerate(self.data):
                if data.shape[1] < categories:
                    self.data[i] = np.pad(data, ((0, 0), (0, categories - data.shape[1])))
                elif data.shape[1] > categories:
                    if np.any(self.data[i][:, categories:] != 0) and not self.force:
                        raise interface.VidtrainDataLossException(
                            'Reducing the number of categories will lead to data loss. Set the force property to True to override this error.')
                    self.data[i] = data[:, :categories]
            self.force = False

    def save(self, path):
        super().save(path)
        with open(self._category_file_name(path), 'w') as f:
            f.write('\n'.join(self.all_category_names))

    def load(self, path):
        super().load(path)
        self._num_categories = self.data[0].shape[1]
        try:
            with open(self._category_file_name(path), 'r') as f:
                self.all_category_names = f.read().splitlines()
        except FileNotFoundError:
            pass

    def update_from(self, template: interface.MultiImageStackClassification):
        if self.num_categories > template.num_categories:
            self.all_category_names[0:template.num_categories] = list(template.category_names)
            for n, d in enumerate(template.data):
                self.data[n][:, :d.shape[1]] = d.copy()
        else:
            self.data = copy.deepcopy(template.data)
            self.num_categories = template.num_categories
            self.all_category_names = template.all_category_names
        self.positions = template.positions.copy()

    def update_multi_stack(self, mis: interface.MultiImageStack):
        temp = self.data.copy()
        self.create_from_multi_image_stack(mis)
        if len(temp) >= len(self.data):
            self.data = temp[0:len(self.data)]
        else:
            self.data[0:len(temp)] = temp

    def image_stacks(self, key=None):
        '''return a generator that yields ImageStacks.
        if key is provided, an individual ImageStack is created from the data corresponding to that key.
        '''
        if key is None:
            return (ImageStackClassification(data=v, category_names=self.all_category_names) for v in self.data)
        return ImageStackClassification(data=self.data[key], category_names=self.all_category_names)

    def create_from_multi_image_stack(self, mis: interface.MultiImageStack):
        self.data = []
        for stack in mis:
            self.data.append(np.zeros((stack.shape[0], self.num_categories)))
        self.positions = mis.positions

    def apply_threshold(self, threshold):
        for i, val in enumerate(self.data):
            self.data[i] = (val > threshold).astype(np.float32)

    def _test_data_loss(self, categories):
        for d in self.data:
            if d.shape[1] > categories:
                if np.any(d[:, categories:] != 0) and not self.force:
                    raise interface.VidtrainDataLossException(
                        'Reducing the number of categories will lead to data loss. Add force=True to override this error.')

    def _category_file_name(self, path):
        return path + '.categories'


class FormatTrainingData(interface.FormatTrainingData):
    def __init__(self, slice_len, slice_padding, target_dim=None):
        self.slice_len = slice_len
        self.slice_padding = slice_padding
        self.target_dim = target_dim
        self.reversible = True
        self.data_structure = []

    def apply(self, x: interface.MultiImageStack, y: interface.MultiImageStackClassification):
        '''slice the numpy arrays in dict x and y into slices and concatenate the slices into a list
        x and y must have identical keys and the first dimension of the numpy arrays must match
        '''
        x_out = []
        y_out = []
        slicer = micdata.formatting.StackSlicer(slice_len=self.slice_len, slice_padding=self.slice_padding)
        if self.target_dim is not None:
            scaler = micdata.formatting.StackScaler(target_dim=self.target_dim)
        for i, _ in enumerate(x):
            if self.target_dim is not None:
                self.reversible = False
                x[i] = (scaler.apply(x[i]), x.positions[i])
            if x[i].shape[0] > self.slice_len:
                x_list = list(slicer.apply(x[i]))
                self.data_structure.append((i, len(x_list)))
                x_out += x_list
                y_out += list(slicer.apply(y[i]))
            else:
                self.reversible = False
                x_out += [x[i]]
                y_out += [y[i]]
        return (x_out, y_out)


class FileVersioning():
    TIMEFORMAT = '%Y-%m-%d_%H%M'
    TIMEFORMAT_REGEX = r'_\d{4}-\d{2}-\d{2}_\d{4}'

    def __init__(self, base_path=None):
        self.base_path = base_path

    def get_name(self, base_path=None, unique=True):
        base_path = base_path or self.base_path
        if unique:
            (path_prefix, ext) = os.path.splitext(base_path)
            return path_prefix + '_' + strftime(self.TIMEFORMAT) + ext
        else:
            return base_path

    def get_file_list(self, base_path=None):
        base_path = base_path or self.base_path
        (path_prefix, ext) = os.path.splitext(base_path)
        return sorted(glob.glob(path_prefix + '*' + ext))

    def get_newest_file(self, base_path=None):
        base_path = base_path or self.base_path
        try:
            return self.get_file_list(base_path)[-1]
        except IndexError:
            return None

    def get_part_before_time(self, base_path=None):
        base_path = base_path or self.base_path
        return re.split(self.TIMEFORMAT_REGEX, base_path, maxsplit=1)[0]


class SequencePredictionFormatter(interface.PredictionFormatter):
    def __init__(self, sequence_len=64, time_overlap=16):
        self.sequence_len = sequence_len
        self.time_overlap = time_overlap
        self.stack_sizes = []
        self.unique_frames = self.sequence_len - self.time_overlap
        assert self.unique_frames > 0, 'Time overlap must be smaller than sequence length. Got sequence_len: {} and time_overlap: {}'.format(
            self.sequence_len, self.time_overlap)
        self.formatter = micdata.formatting.StackSlicer(slice_len=self.unique_frames, slice_padding=self.time_overlap)

    def apply(self, data: interface.MultiImageStack):
        stacks = []
        for stack in data:
            self.stack_sizes.append(stack.shape[0])
            stacks.append(stack)
        stack = np.vstack(stacks)
        return self.formatter.apply(stack)

    def revert(self, data: interface.MultiImageStack, y_pred):
        padding = sum(self.stack_sizes) % self.unique_frames
        reverted = self.formatter.revert(y_pred)
        if padding > 0:
            remove = self.unique_frames - padding
            reverted = reverted[:-remove]
        result = MultiImageStackClassification(multi_image_stack=data, num_categories=y_pred.shape[-1])
        split_at = np.cumsum(self.stack_sizes[:-1])
        for i, stack in enumerate(np.array_split(reverted, split_at)):
            result.data[i] = stack
        return result


class NetworkList(interface.NetworkList):
    def __init__(self):
        self.networks = pd.DataFrame({'Median loss': [], 'FileName': [], 'Full path': [], 'Network object': []})
        self.file_versioning = FileVersioning()

    def append(self, network, file_name):
        self.networks.loc[len(self.networks)] = [self._calc_loss(network),
                                                 os.path.basename(file_name), file_name, network]
        self.networks.sort_values(by=['Median loss'], inplace=True, ignore_index=True)

    def update_from(self, template: interface.NetworkList):
        self.networks = template.networks

    def load(self, path_prefix):
        for f in self.file_versioning.get_file_list(path_prefix + '.h5'):
            self.load_network(f.rpartition('_')[0])

    def save(self, path_prefix):
        for network in self.networks.loc[:, 'Network object']:
            network.save(path_prefix)

    def __delitem__(self, i):
        for file in glob.glob(self.networks.loc[i, 'Full path'] + '*'):
            os.remove(file)
        self.networks.drop(index=i, inplace=True)
        self.networks.reset_index(drop=True, inplace=True)

    def apply_threshold(self, threshold):
        for t in reversed(list(enumerate(self.networks['Median loss'] > threshold))):
            if t[1]:
                del self[t[0]]

    def empty(self):
        return len(self.networks) == 0

    def load_network(self, file_name_no_ext):
        if file_name_no_ext not in list(self.networks.loc[:, 'Full path']):
            network = models.NetworkTrainer()
            network.load(file_name_no_ext)
            self.append(network, file_name_no_ext)

    def get_network(self, index):
        return self.networks.loc[index, 'Network object']

    def clear(self):
        self.networks.drop(list(self.networks.index), inplace=True)
        print(self.networks)  # needed to avoid race condition

    def predict(self, data: interface.MultiImageStack, formatter: interface.PredictionFormatter, best=None):
        if best is None:
            best = self.networks.shape[0]
        split_data = formatter.apply(data)
        num_categories = max([network.num_categories for _, network in self.networks['Network object'].items()])
        result = np.zeros((best,) + split_data.shape[:2] + (num_categories,))
        for n, network in self.networks['Network object'].items():
            if n == best:
                break
            pred = network.model.predict(split_data)
            result[n, :, :, :pred.shape[-1]] = pred
        median = formatter.revert(data, np.median(result, axis=0))
        std = formatter.revert(data, np.std(result, axis=0))
        return (median, std)

    @ staticmethod
    def _calc_loss(network):
        return np.median(network.history.history['val_loss'][-10:])

    def __len__(self):
        return len(self.networks)


class JunctionAnalysisData(interface.WorkflowData):
    def __init__(self,
                 path=None,
                 raw=ImageStack(),
                 processed=MultiImageStack(),
                 annotation=MultiImageStackClassification(),
                 networks=NetworkList(),
                 pred_med=MultiImageStackClassification(),
                 pred_std=MultiImageStackClassification(),
                 pred_corr=MultiImageStackClassification()):
        self.raw = raw
        self.processed = processed
        self.annotation = annotation
        self.networks = networks
        self.pred_med = pred_med
        self.pred_std = pred_std
        self.pred_corr = pred_corr
        self.path = path
        # TODO: (prio 3) move save and load methods from workflow steps here

    @ property
    def path(self):
        '''path where the data will be stored'''
        return self._path

    @ path.setter
    def path(self, path):
        self._path = path
