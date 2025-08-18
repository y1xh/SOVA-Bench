#!/bin/bash

# Set proxy environment variables
export http_proxy=http://127.0.0.1:7892
export https_proxy=http://127.0.0.1:7892
export HTTP_PROXY=http://127.0.0.1:7892
export HTTPS_PROXY=http://127.0.0.1:7892

# Define logging functions
log_info() {
    echo -e "\033[1;32m[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1\033[0m"
}

log_error() {
    echo -e "\033[1;31m[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1\033[0m" >&2
}

# Function to run Python scripts with error handling
run_python_script() {
    local script_path="$1"
    shift  # Remove the first argument (script path), treat the rest as parameters
    local script_args=("$@")
    
    log_info "Executing Python script: $script_path ${script_args[*]}"
    
    # Create output directory if necessary (for --output_file parameter)
    local output_file=""
    for ((i=0; i<${#script_args[@]}; i++)); do
        if [[ "${script_args[$i]}" == "--output_file" && $((i+1)) -lt ${#script_args[@]} ]]; then
            output_file="${script_args[i+1]}"
            mkdir -p "$(dirname "$output_file")"
            break
        fi
    done
    
    python3 "$script_path" "${script_args[@]}"
    local exit_code=$?
    
    if [ $exit_code -ne 0 ]; then
        log_error "Script $script_path failed with exit code: $exit_code"
        return $exit_code
    fi
    
    log_info "Script $script_path executed successfully!"
    return 0
}

# Execute model evaluation script
run_python_script "./utils/model_eval.py" \
  --task "emotion" \
  --input_file "./results/example/inputs/emotion.json" \
  --output_file "./results/example/eval_outputs/emotion.json" \
  --prompt_file "./prompts/emotion.txt" \
  --api_key "" || exit 1

# Execute result reading script (adjusted to match parameter format)
run_python_script "./utils/read_result_paralinguistic.py" \
  --input_file "./results/example/eval_outputs/emotion.json" || exit 1

log_info "All scripts executed successfully!"