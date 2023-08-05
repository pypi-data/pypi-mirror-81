import torch
from torch import tensor
from devai.utils import *
from devai.callbacks import *
from devai.optimizers import *
from tqdm import tqdm


def normalize(x, m, s): return (x-m)/s


def normalize_to(train, valid):
    """
    normalizes train and valid input variables
    :param train: train data
    :param valid: valid data
    :return: normalized train and valid data to the train mean and std
    """
    m, s = train.mean(), train.std()
    return normalize(train, m, s), normalize(valid, m, s)


def near(a, b): return torch.allclose(a, b, rtol=1e-3, atol=1e-5)


def test_near(a, b): test(a, b, near)


# Learner
def param_getter(m): return m.parameters()


class Learner():
    def __init__(self, model, data, loss_func, opt_func=sgd_opt, lr=1e-2, splitter=param_getter,
                 cbs=None, cb_funcs=None):
        """
        Highly versatile, model agnostic object which performs training and inference.
        :param model: pytorch model to be trained
        :param data: databunch containing train dataloader and valid_dataloader
        :param loss_func: loss function
        :param opt_func: optimizer as a function. default: stochastic gradient descent
        :param lr: maximum gloab learning rate
        :param splitter: parameter splitter for discriminative learning rates.
        :param cbs: callbacks as Callback classes
        :param cb_funcs: callbacks as functions
        """
        self.model, self.data, self.loss_func, self.opt_func, self.lr, self.splitter = model, data, loss_func, opt_func, lr, splitter
        self.in_train, self.logger, self.opt = False, print, None

        # NB: Things marked "NEW" are covered in lesson 12
        # NEW: avoid need for set_runner
        self.cbs = []
        self.add_cb(TrainEvalCallback())
        self.add_cbs(cbs)
        self.add_cbs(cbf() for cbf in listify(cb_funcs))

    def add_cbs(self, cbs):
        for cb in listify(cbs):
            self.add_cb(cb)

    def add_cb(self, cb):
        cb.set_runner(self)
        setattr(self, cb.name, cb)
        self.cbs.append(cb)

    def remove_cbs(self, cbs):
        for cb in listify(cbs):
            self.cbs.remove(cb)

    def one_batch(self, i, xb, yb):
        try:
            self.iter = i
            self.xb, self.yb = xb, yb
            self('begin_batch')
            self.pred = self.model(self.xb)
            self('after_pred')
            self.loss = self.loss_func(self.pred, self.yb)
            self('after_loss')
            if not self.in_train:
                return  # if not in train, stop function
            self.loss.backward()
            self('after_backward')
            self.opt.step()
            self('after_step')
            self.opt.zero_grad()
        except CancelBatchException:
            self('after_cancel_batch')
        finally:
            self('after_batch')

    def all_batches(self):
        self.iters = len(self.dl)
        try:
            for i, (xb, yb) in enumerate(self.dl):
                self.one_batch(i, xb, yb)
        except CancelEpochException:
            self('after_cancel_epoch')

    def do_begin_fit(self, epochs):
        self.epochs, self.loss = epochs, tensor(0.)
        self('begin_fit')

    def do_begin_epoch(self, epoch):
        self.epoch, self.dl = epoch, self.data.train_dl
        return self('begin_epoch')

    def fit(self, epochs, cbs=None, reset_opt=False):
        # NEW: pass callbacks to fit() and have them removed when done
        self.add_cbs(cbs)
        # NEW: create optimizer on fit(), optionally replacing existing
        if reset_opt or not self.opt:
            self.opt = self.opt_func(self.splitter(self.model), lr=self.lr)

        try:
            self.model.train()
            self.do_begin_fit(epochs)
            for epoch in range(epochs):
                if not self.do_begin_epoch(epoch):
                    self.all_batches()

                with torch.no_grad():
                    self.model.eval()
                    self.dl = self.data.valid_dl
                    if not self('begin_validate'):
                        self.all_batches()
                self('after_epoch')

        except CancelTrainException:
            self.in_train = False  # added by dev 08.2020
            self('after_cancel_train')
        finally:
            self('after_fit')
            self.remove_cbs(cbs)

    ALL_CBS = {'begin_batch', 'after_pred', 'after_loss', 'after_backward', 'after_step',
               'after_cancel_batch', 'after_batch', 'after_cancel_epoch', 'begin_fit',
               'begin_epoch', 'begin_validate', 'after_epoch',
               'after_cancel_train', 'after_fit'}

    def __call__(self, cb_name):
        res = False
        assert cb_name in self.ALL_CBS
        for cb in sorted(
            self.cbs, key=lambda x: x._order): res = cb(cb_name) and res
        return res

    def get_raw_preds(self, dataset="valid", return_x=False):
        """
        returns preds and actual values for y. 
        Note that callbacks are not used in the prediction generation
        returns predicted, actual (and x if requested in args)
        """
        with torch.no_grad():
            if dataset == "valid":
                self.dl = self.data.valid_dl
            elif dataset == "train":
                self.dl = self.data.train_dl
            else:
                raise ValueError(
                    f"{dataset} is not a valid dataset. Please enter either 'train' or 'valid'"
                )
            yps = []  # predicted y
            ybs = []  # actual y
            if return_x:
                xbs = []  # x
            for i, (xb, yb) in enumerate(tqdm(self.dl)):
                self.iter = i
                self.xb, self.yb = xb, yb
                self("begin_batch")
                ybs.append(yb)
                yps.append(self.model(self.xb))
                if return_x:
                    xbs.append(xb)
        outputs = (
            yps,
            ybs,
        )
        if return_x:
            outputs += (xbs,)
        return outputs

    def get_preds(self, dataset="valid", **kwargs):
        """
        builds on top of raw preds functions. May not work for all models as 
        this assumes the model output is a tensor (and not a tuple)
        """
        output = self.get_raw_preds(dataset=dataset, **kwargs)
        preds = torch.argmax(torch.cat(output[0]), 1)
        actuals = torch.cat(output[1])
        return preds, actuals
