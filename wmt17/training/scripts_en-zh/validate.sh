#!/bin/sh
# Distributed under MIT license

# this script evaluates translations of the newstest2013 test set
# using detokenized BLEU (equivalent to evaluation with mteval-v13a.pl).

translations=$1

script_dir=`dirname $0`
main_dir=$script_dir/../
data_dir=$main_dir/data

#language-independent variables (toolkit locations)
. $main_dir/../vars

#language-dependent variables (source and target language)
. $main_dir/vars
dev_prefix=corpus_valid2
ref=$dev_prefix.bpe.$trg

# evaluate translations and write BLEU score to standard output (for
# use by nmt.py)
#$script_dir/postprocess.sh < $translations | \
#    $nematus_home/data/multi-bleu-detok.perl $data_dir/$ref | \
#    cut -f 3 -d ' ' | \
#    cut -f 1 -d ','

# === 08/20 KP, bleu in py ===
cat $translations | \
sed 's/,/，/g' | \
sed 's/\.$/。/g' > $data_dir/tmp_valid

ref_pwd=`realpath $data_dir/$ref`
trans_pwd=`realpath $data_dir/tmp_valid`

python $script_dir/evaluation_utils.py $ref_pwd $trans_pwd
#rm $data_dir/tmp_valid
# ============================

