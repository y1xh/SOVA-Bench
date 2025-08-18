#!/bin/bash

# Assign arguments
INPUT_FOLDER="$1"
OUTPUT_FILE="$2"

# Create output directory if not exists
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Activate virtual environment (if needed)
# source /path/to/venv/bin/activate

# Run the Python script
python utmosv2_predictor.py \
    --input_folder "$INPUT_FOLDER" \
    --output_file "$OUTPUT_FILE"

# Check execution status
if [ $? -eq 0 ]; then
    echo "Successfully generated predictions: $OUTPUT_FILE"
else
    echo "Prediction failed"
    exit 1
fi    