#!/bin/sh
# Source of server configs: https://github.com/ggerganov/llama.cpp/blob/master/examples/server/README.md

# Server variables
host=127.0.0.1
port=5002

# Rarely modified variables
threads=6 # num cpu threads for processing
main_gpu=0 # gpu number for processing

# Model process variables
model=./models/Hermes-2-Pro-Llama-3-8B-Q6_K.gguf
n_gpu_layers=51 # (51 max for current model) you must set the optimal option if you will be replacing the default model
ctx_size=2048
#ctx_size=4096
batch_size=512

# Model prompt format example:

### Instruction:
### Input:
### Response:

./server \
    -t $threads \
    -ngl $n_gpu_layers \
    -m $model \
    -c $ctx_size \
    -b $batch_size \
    -mg $main_gpu \
    --host $host\
    --port $port
