./linux_arm_benchmark_model \
  --graph=data/mobilenet_v1_1.0_224_quant.tflite \
  --num_threads=4 \
  --enable_op_profiling=true \
  --profiling_output_csv_file=benchmark.csv
