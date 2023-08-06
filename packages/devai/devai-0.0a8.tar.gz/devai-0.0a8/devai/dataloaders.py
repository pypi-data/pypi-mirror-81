import torch
from devai.utils.ml import *
from torch.utils.data import DataLoader, SequentialSampler, RandomSampler
import random


class Dataset():
    """simple data structure for storing x and y values"""

    def __init__(self, x, y): self.x, self.y = x, y
    def __len__(self): return len(self.x)
    def __getitem__(self, i): return self.x[i], self.y[i]


class DataBunch():
    """Stores train and valid dataloaders"""

    def __init__(self, train_dl, valid_dl, c_in=None, c_out=None):
        self.train_dl, self.valid_dl, self.c_in, self.c_out = train_dl, valid_dl, c_in, c_out

    @property
    def train_ds(self): return self.train_dl.dataset

    @property
    def valid_ds(self): return self.valid_dl.dataset


def get_dls(train_ds, valid_ds, bs, **kwargs):
    """ transforms datasets into dataloaders"""
    return (DataLoader(train_ds, batch_size=bs, shuffle=True, **kwargs),
            DataLoader(valid_ds, batch_size=bs*2, **kwargs))


class ItemList(ListContainer):
    """Base item container which stores inputs and labels optionally"""

    def __init__(self, items, path='.', tfms=None, labels=None):
        super().__init__(items)
        self.path, self.tfms = Path(path), tfms
        if labels:
            # dev added code to add labels during the creation of items list (also added the func argument 'labels')
            self.labels = labels

    def __repr__(self): return f'{super().__repr__()}\nPath: {self.path}'

    def new(self, items, cls=None):
        if cls is None:
            cls = self.__class__
        return cls(items, self.path, tfms=self.tfms)

    def get(self, i): return i
    def _get(self, i): return compose(self.get(i), self.tfms)

    def __getitem__(self, idx):
        res = super().__getitem__(idx)
        if isinstance(res, list):
            return [self._get(o) for o in res]
        return self._get(res)


def grandparent_splitter(fn, valid_name='valid', train_name='train'):
    """splits items based on folder structure"""
    gp = fn.parent.parent.name
    return True if gp == valid_name else False if gp == train_name else None


# https://github.com/fastai/course-v3/blob/master/nbs/dl2/11a_transfer_learning.ipynb
def random_splitter(fn, p_valid): return random.random() < p_valid


def split_by_func(items, f):
    """ splits by specific function"""
    mask = [f(o) for o in items]
    # `None` values will be filtered out
    f = [o for o, m in zip(items, mask) if m == False]
    t = [o for o, m in zip(items, mask) if m == True]
    return f, t


class SplitData():
    """data structure for storing post split data"""

    def __init__(self, train, valid): self.train, self.valid = train, valid

    def __getattr__(self, k): return getattr(self.train, k)
    # This is needed if we want to pickle SplitData and be able to load it back without recursion errors
    def __setstate__(self, data: Any): self.__dict__.update(data)

    @classmethod
    def split_by_func(cls, il, f):
        lists = map(il.new, split_by_func(il.items, f))
        return cls(*lists)

    def __repr__(
        self): return f'{self.__class__.__name__}\nTrain: {self.train}\nValid: {self.valid}\n'


def databunchify(sd, bs, c_in=None, c_out=None, **kwargs):
    """converts datasets --> dataloaders --> databunch"""
    dls = get_dls(sd.train, sd.valid, bs, **kwargs)
    return DataBunch(*dls, c_in=c_in, c_out=c_out)


SplitData.to_databunch = databunchify


class Processor():
    """simple class to preprocess inputs and labels"""

    def process(self, items): return items


class CategoryProcessor(Processor):
    """label processor which creates a 'vocabulary' of uniques items in labels"""

    def __init__(self, vocab=None):
        self.vocab = vocab
        self.otoi = None

    def __call__(self, items):
        # The vocab is defined on the first use.
        if self.vocab is None:
            self.vocab = uniqueify(items)
        if self.otoi is None:
            self.otoi = {v: k for k, v in enumerate(self.vocab)}
        return [self.proc1(o) for o in items]

    def proc1(self, item): return self.otoi[item]

    def deprocess(self, idxs):
        assert self.vocab is not None
        return [self.deproc1(idx) for idx in idxs]

    def deproc1(self, idx): return self.vocab[idx]


def parent_labeler(fn):
    """sets labels based on parent folder e.g. train/df.csv"""
    return fn.parent.name


def _label_by_func(ds, f, cls=ItemList):
    """label items based on function f"""
    return cls([f(o) for o in ds.items], path=ds.path)


class LabeledData():
    """post labelled data object which stores x and y pairs for each observation"""

    def process(self, il, proc): return il.new(compose(il.items, proc))

    # this is where the processors are run
    def __init__(self, x, y, proc_x=None, proc_y=None):
        self.x, self.y = self.process(x, proc_x), self.process(y, proc_y)
        self.proc_x, self.proc_y = proc_x, proc_y

    def __repr__(
        self): return f'{self.__class__.__name__}\nx: {self.x}\ny: {self.y}\n'

    def __getitem__(self, idx): return self.x[idx], self.y[idx]
    def __len__(self): return len(self.x)

    def x_obj(self, idx): return self.obj(self.x, idx, self.proc_x)
    def y_obj(self, idx): return self.obj(self.y, idx, self.proc_y)

    def obj(self, items, idx, procs):
        isint = isinstance(idx, int) or (isinstance(
            idx, torch.LongTensor) and not idx.ndim)
        item = items[idx]
        for proc in reversed(listify(procs)):
            item = proc.deproc1(item) if isint else proc.deprocess(item)
        return item

    @classmethod
    def label_by_func(cls, il, f, proc_x=None, proc_y=None):
        return cls(il, _label_by_func(il, f), proc_x=proc_x, proc_y=proc_y)


def label_by_func(sd, f, proc_x=None, proc_y=None):
    train = LabeledData.label_by_func(
        sd.train, f, proc_x=proc_x, proc_y=proc_y)
    valid = LabeledData.label_by_func(
        sd.valid, f, proc_x=proc_x, proc_y=proc_y)
    return SplitData(train, valid)


def to_byte_tensor(item):
    res = torch.ByteTensor(torch.ByteStorage.from_buffer(item.tobytes()))
    w, h = item.size
    return res.view(h, w, -1).permute(2, 0, 1)


to_byte_tensor._order = 20


def to_float_tensor(item): return item.float().div_(255.)


to_float_tensor._order = 30


class TextList(ItemList):
    @classmethod
    def from_df(cls, df, feat_cols, label_cols, sep_tok=" ", test=False):
        """
        converts a dataframe into an ItemList
        :param df: dataframe
        :param feat_cols: feature columns
        :param label_cols: label columns
        :param sep_tok: the tok which separates question and answer sequences
        :param test: whether the df is test or not, mainly to determine whether labels exist.
        :return: Itemlist
        """
        feat_cols = listify(feat_cols)
        x = df[feat_cols[0]]
        for i in range(1, len(feat_cols)):
            x += f" {sep_tok} " + df[feat_cols[i]]
        labels = cls(df[label_cols].values) if not test else cls(
            [[None, None] for _ in len(df)])
        return cls(x, labels=labels)
