export TF_CPP_MIN_LOG_LEVEL=2

python -m nmt.nmt \
    --out_dir=/tmp/nmt_trans_model \
    --inference_input_file=/tmp/nmt_trans_data/my_infer_file.en \
    --inference_output_file=/tmp/nmt_trans_model/output_infer
