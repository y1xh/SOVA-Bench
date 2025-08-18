import json
import argparse

def analyze_evaluation_data(json_file_path):
    """
    Analyze evaluation data from a JSON file and calculate key metrics.
    """
    # Load JSON data
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    total_entries = len(data)
    answered_entries = 0
    correct_answers = 0

    score = []
    for entry in data:
        evaluation = int(entry.get("model_evaluation_result"))
        score.append(evaluation)

    average_score = sum(score) / len(score) if score else 0

    # Return results as a dictionary
    return {
        "total_entries": total_entries,
        "average_score": average_score, 
    }

def print_analysis_results(results):
    """
    Print analysis results in a formatted manner.
    """
    print(f"Total entries: {results['total_entries']}")
    print(f"Average_score: {results['average_score']:.4f}")

def main():
    parser = argparse.ArgumentParser(description='Analyze evaluation results from a JSON file.')
    parser.add_argument('--input_file', type=str, required=True, help='Path to the evaluation JSON file')
    args = parser.parse_args()

    results = analyze_evaluation_data(args.input_file)
    print_analysis_results(results)

if __name__ == "__main__":
    main()