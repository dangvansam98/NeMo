# =============================================================================
# Copyright 2020 NVIDIA. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =============================================================================

__all__ = ['get_pretrained_lm_models_list', 'get_pretrained_lm_model']

import wget

from nemo import logging
from nemo.collections.nlp.nm.trainables.common.huggingface.huggingface_utils import *
from nemo.collections.nlp.nm.trainables.common.megatron.megatron_bert_nm import MegatronBERT
from nemo.collections.nlp.nm.trainables.common.megatron.megatron_utils import *


def get_pretrained_lm_models_list():
    '''
    Returns the list of support pretrained models
    '''
    return get_megatron_lm_models_list() + get_huggingface_lm_models_list()


def get_pretrained_lm_model(pretrained_model_name, config=None, vocab=None, checkpoint=None):
    '''
    Returns pretrained model
    Args:
        pretrained_model_name (str): pretrained model name, for example, bert-base-uncased.
            See the full list by calling get_pretrained_lm_models_list()
        config (str): path to the model configuration file
        vocab (str): path to the vocabulary file used during model training 
        checkpoint (str): path to the pretrained model checkpoint
    Returns:
        Pretrained model (NM)
    '''
    if pretrained_model_name in get_huggingface_lm_models_list():
        model = get_huggingface_lm_model(bert_config=config, pretrained_model_name=pretrained_model_name)
    elif pretrained_model_name in get_megatron_lm_models_list():
        if not config:
            config = get_megatron_config_file(pretrained_model_name)
        if not vocab:
            vocab = get_megatron_vocab_file(pretrained_model_name)
        if not checkpoint:
            checkpoint = get_megatron_checkpoint(pretrained_model_name)
        model = MegatronBERT(
            model_name=pretrained_model_name,
            vocab_file=vocab,
            hidden_size=config['hidden-size'],
            num_attention_heads=config['num-attention-heads'],
            num_layers=config['num-layers'],
            max_seq_length=config['max-seq-length'],
        )
    else:
        raise ValueError(f'{pretrained_model_name} is not supported')

    if checkpoint:
        model.restore_from(checkpoint)
        logging.info(f"{pretrained_model_name} model restored from {checkpoint}")
    return model
