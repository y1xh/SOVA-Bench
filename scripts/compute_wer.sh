#!/bin/bash


PREDICTIONS_FILE="./results/example/inputs/asr.json"
OUTPUT_FILE="./results/example/eval_outputs/asr.json"

# Create the output directory if it doesn't exist
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
mkdir -p "$OUTPUT_DIR"

# Execute the Python script with provided arguments
python ./utils/compute_wer.py \
    --predictions_file "$PREDICTIONS_FILE" \
    --output_file "$OUTPUT_FILE"

# Check the execution status of the Python script
if [ $? -eq 0 ]; then
    echo "WER calculation completed. Results saved to: $OUTPUT_FILE"
else
    echo "WER calculation failed."
    exit 1
fi
    