#!/bin/sh
# Distributed under MIT license

script_dir=`dirname $0`
main_dir=$script_dir/../
data_dir=$main_dir/data
working_dir=$main_dir/model

#language-independent variables (toolkit locations)
. $main_dir/../vars

#language-dependent variables (source and target language)
. $main_dir/vars

CUDA_VISIBLE_DEVICES=$device python $nematus_home/nematus/train.py \
    --model_type transformer \
    --model $working_dir/model \
    --datasets $data_dir/corpus.bpe.$src $data_dir/corpus.bpe.$trg \
    --valid_datasets $data_dir/corpus_valid2.bpe.$src $data_dir/corpus_valid2.bpe.$trg \
    --dictionaries $data_dir/corpus.bpe.$src.json $data_dir/corpus.bpe.$trg.json \
    --valid_script $script_dir/validate.sh \
    --reload latest_checkpoint \
    --dim_word 512 \
    --dim 512 \
    --learning_schedule transformer \
    --optimizer adam \
    --maxlen 50 \
    --batch_size 150 \
    --valid_batch_size 40 \
    --validFreq 10000 \
    --dispFreq 1000 \
    --saveFreq 30000 \
    --sampleFreq 10000 \
    --tie_decoder_embeddings \

