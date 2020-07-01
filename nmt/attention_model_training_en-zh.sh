#rm /tmp/nmt_trans_model -r

# remove external output trans files
rm /tmp/nmt_trans_model/output_dev
rm /tmp/nmt_trans_model/output_test

# remove hparams of last train
rm /tmp/nmt_trans_model/hparams
mkdir /tmp/nmt_trans_model

python -m nmt.nmt \
    --attention=scaled_luong \
    --src=en --tgt=zh \
    --vocab_prefix=/tmp/nmt_trans_data/vocab_trans \
    --train_prefix=/tmp/nmt_trans_data/corpus_train \
    --dev_prefix=/tmp/nmt_trans_data/corpus_valid  \
    --test_prefix=/tmp/nmt_trans_data/corpus_test \
    --out_dir=/tmp/nmt_trans_model \
    --infer_mode=beam_search \
    --beam_width=10 \
    --attention_architecture=gnmt_v2 \
    --num_train_steps=600000 \
    --steps_per_stats=200 \
    --steps_per_eval=5000 \
    --steps_per_external_eval=40000 \
    --num_layers=2 \
    --num_units=512 \
    --learning_rate=0.2 \
    --decay_scheme=luong5 \
    --dropout=0.2 \
    --metrics=bleu
