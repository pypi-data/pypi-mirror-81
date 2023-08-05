"""Classification trainer/evaluator implementation module."""
import logging
from typing import AnyStr  # noqa: F401

import torch
import torch.optim

import thelper.concepts
import thelper.typedefs as typ  # noqa: F401
import thelper.utils
from thelper.train.base import Trainer

logger = logging.getLogger(__name__)


@thelper.concepts.classification
class ImageClassifTrainer(Trainer):
    """Trainer interface specialized for image classification.

    This class implements the abstract functions of :class:`thelper.train.base.Trainer` required to train/evaluate
    a model for image classification or recognition. It also provides a utility function for fetching i/o packets
    (images, class labels) from a sample, and that converts those into tensors for forwarding and loss estimation.

    .. seealso::
        | :class:`thelper.train.base.Trainer`
    """

    def __init__(self,
                 session_name,    # type: AnyStr
                 session_dir,     # type: AnyStr
                 model,           # type: thelper.typedefs.ModelType
                 task,            # type: thelper.tasks.Task
                 loaders,         # type: thelper.typedefs.MultiLoaderType
                 config,          # type: thelper.typedefs.ConfigDict
                 ckptdata=None    # type: typ.Optional[thelper.typedefs.CheckpointContentType]
                 ):
        """Receives session parameters, parses image/label keys from task object, and sets up metrics."""
        super().__init__(session_name, session_dir, model, task, loaders, config, ckptdata=ckptdata)
        assert isinstance(self.task, thelper.tasks.Classification), "expected task to be classification"
        self.warned_no_shuffling_augments = False

    def _to_tensor(self, sample):
        """Fetches and returns tensors of input images and class labels from a batched sample dictionary."""
        assert isinstance(sample, dict), "trainer expects samples to come in dicts for key-based usage"
        assert self.task.input_key in sample, f"could not find input key '{self.task.input_key}' in sample dict"
        input_val, target_val = sample[self.task.input_key], None
        if isinstance(input_val, list):
            if self.task.gt_key in sample and sample[self.task.gt_key] is not None:
                gt_tensor = sample[self.task.gt_key]
                assert isinstance(gt_tensor, list) and len(gt_tensor) == len(input_val), \
                    "target tensor should also be a list of the same length as input"
                target_val = [None] * len(input_val)
                for idx in range(len(input_val)):
                    input_val[idx], target_val[idx] = self._to_tensor({self.task.input_key: input_val[idx],
                                                                      self.task.gt_key: gt_tensor[idx]})
            else:
                for idx in range(len(input_val)):
                    input_val[idx] = torch.FloatTensor(input_val[idx])
        else:
            input_val = torch.FloatTensor(input_val)
            if self.task.gt_key in sample and sample[self.task.gt_key] is not None:
                gt_tensor = sample[self.task.gt_key]
                assert len(gt_tensor) == len(input_val), \
                    "target tensor should be an array of the same length as input (== batch size)"
                if isinstance(gt_tensor, torch.Tensor) and gt_tensor.dtype == torch.int64:
                    target_val = gt_tensor  # shortcut with less checks (dataset is already using tensor'd indices)
                else:
                    if self.task.multi_label:
                        assert isinstance(gt_tensor, torch.Tensor) and \
                            gt_tensor.shape == (len(input_val), len(self.task.class_names)), \
                            "gt tensor for multi-label classification should be 2d array (batch size x nbclasses)"
                        target_val = gt_tensor.float()
                    else:
                        target_val = []
                        for class_name in gt_tensor:
                            assert isinstance(class_name, (int, torch.Tensor, str)), \
                                "expected gt tensor to be an array of names (string) or indices (int)"
                            if isinstance(class_name, (int, torch.Tensor)):
                                if isinstance(class_name, torch.Tensor):
                                    assert torch.numel(class_name) == 1, "unexpected scalar label, got vector"
                                    class_name = class_name.item()
                                # dataset must already be using indices, we will forgive this...
                                assert 0 <= class_name < len(self.task.class_names), \
                                    "class name given as out-of-range index (%d) for class list" % class_name
                                target_val.append(class_name)
                            else:
                                assert class_name in self.task.class_names, \
                                    "got unexpected label '%s' for a sample (unknown class)" % class_name
                                target_val.append(self.task.class_indices[class_name])
                        target_val = torch.LongTensor(target_val)
        return input_val, target_val

    def train_epoch(self, model, epoch, dev, loss, optimizer, loader, metrics, output_path):
        """Trains the model for a single epoch using the provided objects.

        Args:
            model: the model to train that is already uploaded to the target device(s).
            epoch: the epoch index we are training for (0-based).
            dev: the target device that tensors should be uploaded to.
            loss: the loss function used to evaluate model fidelity.
            optimizer: the optimizer used for back propagation.
            loader: the data loader used to get transformed training samples.
            metrics: the dictionary of metrics/consumers to update every iteration.
            output_path: directory where output files should be written, if necessary.
        """
        assert loss is not None, "missing loss function"
        assert optimizer is not None, "missing optimizer"
        assert loader, "no available data to load"
        assert isinstance(metrics, dict), "expect metrics as dict object"
        epoch_loss = 0
        epoch_size = len(loader)
        self.logger.debug("fetching data loader samples...")
        for idx, sample in enumerate(loader):
            input_val, target_val = self._to_tensor(sample)
            assert target_val is not None, "groundtruth required when training a model"
            optimizer.zero_grad()
            if isinstance(input_val, list):  # training samples got augmented, we need to backprop in multiple steps
                assert input_val, "cannot train with empty post-augment sample lists"
                assert isinstance(target_val, list) and len(target_val) == len(input_val), \
                    "target should also be a list of the same length as input"
                if not self.warned_no_shuffling_augments:
                    self.logger.warning("using training augmentation without global shuffling, "
                                        "gradient steps might be affected")
                    # see the docstring of thelper.transforms.operations.Duplicator for more information
                    self.warned_no_shuffling_augments = True
                iter_loss = None
                iter_pred = None
                augs_count = len(input_val)
                for input_idx in range(augs_count):
                    aug_pred = model(self._move_tensor(input_val[input_idx], dev))
                    aug_loss = loss(aug_pred, self._move_tensor(target_val[input_idx], dev))
                    aug_loss.backward()  # test backprop all at once? might not fit in memory...
                    if iter_pred is None:
                        iter_loss = aug_loss.clone().detach()
                        iter_pred = aug_pred.clone().detach()
                    else:
                        iter_loss += aug_loss.detach()
                        iter_pred = torch.cat((aug_pred.detach(), iter_pred), dim=0)
                iter_loss /= augs_count
                target_val = torch.cat(target_val, dim=0)
            else:  # this is the default (simple) case where we generate predictions without augmentations
                iter_pred = model(self._move_tensor(input_val, dev))
                iter_loss = loss(iter_pred, self._move_tensor(target_val, dev))
                iter_loss.backward()
            optimizer.step()
            iter_pred_cpu = self._move_tensor(iter_pred, dev="cpu", detach=True)
            target_val_cpu = self._move_tensor(target_val, dev="cpu", detach=True)
            iter_loss = iter_loss.item()
            for metric in metrics.values():
                metric.update(task=self.task, input=input_val, pred=iter_pred_cpu,
                              target=target_val_cpu, sample=sample, loss=iter_loss, iter_idx=idx,
                              max_iters=epoch_size, epoch_idx=epoch, max_epochs=self.epochs,
                              output_path=output_path)
            epoch_loss += iter_loss
        epoch_loss /= epoch_size
        return epoch_loss

    def eval_epoch(self, model, epoch, dev, loader, metrics, output_path):
        """Evaluates the model using the provided objects.

        Args:
            model: the model to evaluate that is already uploaded to the target device(s).
            epoch: the epoch index we are training for (0-based).
            dev: the target device that tensors should be uploaded to.
            loader: the data loader used to get transformed valid/test samples.
            metrics: the dictionary of metrics/consumers to update every iteration.
            output_path: directory where output files should be written, if necessary.
        """
        assert loader, "no available data to load"
        assert isinstance(metrics, dict), "expect metrics as dict object"
        with torch.no_grad():
            epoch_size = len(loader)
            self.logger.debug("fetching data loader samples...")
            for idx, sample in enumerate(loader):
                if idx < self.skip_eval_iter:
                    continue  # skip until previous iter count (if set externally; no effect otherwise)
                input_val, target_val = self._to_tensor(sample)
                if isinstance(input_val, list):  # evaluation samples got augmented, we need to get the mean prediction
                    assert input_val, "cannot eval with empty post-augment sample lists"
                    assert isinstance(target_val, list) and len(target_val) == len(input_val), \
                        "target should also be a list of the same length as input"
                    # this might be costly for nothing, we could remove the check and assume user is not dumb
                    assert not any([not torch.eq(lbl, target_val[0]).all() for lbl in target_val]), \
                        "all target values should be identical! (why do eval-time augment otherwise?)"
                    target_val = target_val[0]  # since all identical, just pick the first and pretend its the only one
                    preds = None
                    for input_idx in range(len(input_val)):
                        pred = model(self._move_tensor(input_val[input_idx], dev))
                        if preds is None:
                            preds = torch.unsqueeze(pred.clone(), 0)
                        else:
                            preds = torch.cat((preds, torch.unsqueeze(pred, 0)), 0)
                    pred = torch.mean(preds, dim=0)
                else:  # this is the default (simple) case where we generate predictions without augmentations
                    pred = model(self._move_tensor(input_val, dev))
                pred_cpu = self._move_tensor(pred, dev="cpu", detach=True)
                target_val_cpu = self._move_tensor(target_val, dev="cpu", detach=True)
                for metric in metrics.values():
                    metric.update(task=self.task, input=input_val, pred=pred_cpu,
                                  target=target_val_cpu, sample=sample, loss=None, iter_idx=idx,
                                  max_iters=epoch_size, epoch_idx=epoch, max_epochs=self.epochs,
                                  output_path=output_path)
