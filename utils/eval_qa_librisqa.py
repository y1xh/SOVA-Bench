import argparse
import json
from utils import load_data_from_json, save_result_to_json

def parse_prediction(prediction_str):
    """
    Parse the predicted answer option from the model's response.
    Returns None if the format is invalid.
    """
    start_marker = "The correct answer is"
    start_index = prediction_str.find(start_marker)
    if start_index == -1:
        return None
    start_index += len(start_marker)
    end_index = prediction_str.find(".", start_index)
    if end_index == -1:
        return None
    return prediction_str[start_index:end_index].strip().split(":")[0].strip()

def evaluate_predictions(input_file, output_file):
    """
    Evaluate model predictions against ground truth answers and save results.
    """
    data = load_data_from_json(input_file)
    options = ['A', 'B', 'C', 'D']
    total = 0
    correct = 0
    results = []  
    
    for item in data:
        try:
            question_id = item['id']
            prediction_text = item['prediction']
            actual_answer_idx = item['answer']
            
            # Parse predicted answer
            predicted_option = parse_prediction(prediction_text)
            predicted_idx = options.index(predicted_option) if predicted_option in options else -1
            
            # Check correctness
            is_correct = predicted_idx == actual_answer_idx
            if is_correct:
                correct += 1
            total += 1
            
            # Prepare result
            result = {
                'question_id': question_id,
                'predicted': predicted_option,
                'actual': options[actual_answer_idx],
                'is_correct': is_correct
            }
            
            results.append(result)
            print(f"Processed {question_id}: {'Correct' if is_correct else 'Incorrect'}")
            
        except Exception as e:
            print(f"Skipping item {item.get('id', 'unknown')} due to error: {str(e)}")

    results.append({
        'total_accuracy': correct / total if total > 0 else 0,
        'total_questions': total
    })
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
    
    accuracy = correct / total if total > 0 else 0
    print(f"Evaluation complete. Accuracy: {accuracy:.2%}")

def main():
    parser = argparse.ArgumentParser(description='Evaluate model predictions against ground truth answers.')
    parser.add_argument('--input_file', required=True, help='Path to input JSON file')
    parser.add_argument('--output_file', required=True, help='Path to output JSON results file')
    args = parser.parse_args()
    
    evaluate_predictions(args.input_file, args.output_file)

if __name__ == "__main__":
    main()