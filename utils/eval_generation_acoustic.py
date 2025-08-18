import os
import json
import argparse
from pathlib import Path
import utmosv2
from tqdm import tqdm

def main(args):
    model = utmosv2.create_model(pretrained=True)
    input_folder = Path(args.input_folder)
    output_file = args.output_file
    os.makedirs(Path(output_file).parent, exist_ok=True)
    
    if not os.path.exists(output_file):
        with open(output_file, "w") as f:
            json.dump([], f, indent=4)

    wav_files = list(input_folder.rglob('*.wav'))
    total_files = len(wav_files)
    print(f"Found {total_files} .wav files in {input_folder}")

    for wav_file in tqdm(wav_files, desc="Processing files"):
        try:
            file_id = wav_file.stem
            mos = model.predict(input_path=str(wav_file))
            result = {"id": file_id, "mos": float(mos)}
            
            with open(output_file, "r") as f:
                results = json.load(f)
            
            results.append(result)
            
            with open(output_file, "w") as f:
                json.dump(results, f, indent=4)
        except Exception as e:
            print(f"Error processing {wav_file}: {str(e)}")
            continue

    print(f"Predictions saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Predict MOS scores using UTMOSv2 model')
    parser.add_argument('--input_folder', required=True, help='Path to the folder containing .wav files')
    parser.add_argument('--output_file', required=True, help='Path to the output JSON file')
    args = parser.parse_args()
    main(args)    