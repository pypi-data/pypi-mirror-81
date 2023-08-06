import random

import torch
from sklearn.preprocessing import MultiLabelBinarizer
from torch.utils.data import Dataset
from transformers import AutoTokenizer

from .data_utils import compose, grouping_idx
from .domain import Cases, Params
from .io_utils import load_datazip

random.seed(42)


class CustomDataset(Dataset):
    def __init__(self, texts, tokenizer: AutoTokenizer, max_len, tags=None):
        self.tokenizer = tokenizer
        self.texts = texts
        self.tags = tags
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, index):
        text = self.texts[index]

        inputs = self.tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            truncation=True,
            max_length=self.max_len,
            padding="max_length",
            return_token_type_ids=True,
        )
        ids = inputs["input_ids"]
        mask = inputs["attention_mask"]
        token_type_ids = inputs["token_type_ids"]

        if self.tags is None:
            return {
                "input_ids": torch.tensor(ids, dtype=torch.long),
                "attention_mask": torch.tensor(mask, dtype=torch.long),
                "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            }

        return {
            "input_ids": torch.tensor(ids, dtype=torch.long),
            "attention_mask": torch.tensor(mask, dtype=torch.long),
            "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            "labels": torch.tensor(self.tags[index], dtype=torch.float),
        }


class DatasetFactory:
    def __init__(self, params: Params):
        self.params = params
        raw_data = load_datazip(params.datazip_path)
        self.x_test_dict = raw_data.x_test_dict
        self.x_train_dict = raw_data.x_train_dict
        self.y_train_tags = raw_data.y_train_tags
        self.y_test_tags = raw_data.y_test_tags
        self.init_mlb()
        self.init_tokenizer(params.identifier)

    def init_mlb(self):
        y = self.y_train_tags + self.y_test_tags
        mlb = MultiLabelBinarizer().fit(y)
        self.mlb = mlb
        self.num_labels = len(mlb.classes_)
        assert self.num_labels >= 18, "load labels error"

    def init_tokenizer(self, identifier: str):
        self.tokenizer = AutoTokenizer.from_pretrained(identifier)

    def supply_training_dataset(self):
        x_train, y_train_raw = self._upsampling(
            self.x_train_dict, self.y_train_tags, target=self.params.upsampling
        )
        y_train = self.mlb.transform(y_train_raw)
        x_test = list(map(compose, self.x_test_dict))
        y_test = self.mlb.transform(self.y_test_tags)
        train_dataset = CustomDataset(
            x_train, self.tokenizer, self.params.max_len, y_train
        )
        testing_set = CustomDataset(x_test, self.tokenizer, self.params.max_len, y_test)
        return train_dataset, testing_set

    def supply_unlabelled_dataset(self, cases: Cases):
        texts = list(map(self._compose, cases))
        dataset = CustomDataset(texts, self.tokenizer, self.params.max_len)
        return dataset

    def _upsampling(self, x, y, target=100):
        group_by_idx = grouping_idx(y)
        new_x = []
        new_y = []
        for group_idx in group_by_idx.values():
            upsample_idx = random.choices(group_idx, k=target)
            new_x.extend(map(lambda idx: self._compose(x[idx]), upsample_idx))
            new_y.extend(map(lambda idx: y[idx], upsample_idx))
        return new_x, new_y

    # Makeshift upsampling to 125 cases per tag
    def _compose(self, case):
        return compose(case, shuffle=True)
