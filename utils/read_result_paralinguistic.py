import json
import argparse

def result_correctness_emotion(prediction, reference):
    """
    Determine if a single prediction is correct (including special cases).
    
    Args:
        prediction (str): Model's prediction result
        reference (str): Reference standard answer
        
    Returns:
        tuple: (is_answered, is_correct)
               is_answered: Whether the prediction is non-"none"
               is_correct: Whether the prediction is correct
    """
    pred = prediction.strip().lower()
    ref = reference.strip().lower()
    
    is_answered = (pred != "none")
    is_correct = (
        (pred == ref)
    )
    
    return is_answered, is_correct

def result_correctness_age(prediction, reference):
    """
    Determine if a single prediction is correct (including special cases).
    
    Args:
        prediction (str): Model's prediction result
        reference (str): Reference standard answer
        
    Returns:
        tuple: (is_answered, is_correct)
               is_answered: Whether the prediction is non-"none"
               is_correct: Whether the prediction is correct
    """
    pred = prediction.strip().lower()
    ref = reference.strip().lower()
    
    is_answered = (pred != "none")
    is_correct = (
        (pred == ref) or
        (pred == 'forties' and ref == 'fourties') or
        (pred == 'teens' and ref == 'teens (less than twenties)')
        
    )
    
    return is_answered, is_correct

def result_correctness_gender(prediction, reference):
    """
    Determine if a single prediction is correct (including special cases).
    
    Args:
        prediction (str): Model's prediction result
        reference (str): Reference standard answer
        
    Returns:
        tuple: (is_answered, is_correct)
               is_answered: Whether the prediction is non-"none"
               is_correct: Whether the prediction is correct
    """
    pred = prediction.strip().lower()
    ref = reference.strip().lower()
    
    is_answered = (pred != "none")
    is_correct = (
        (pred == ref)
    )
    
    return is_answered, is_correct

def analyze_predictions(json_file_path):
    """
    Analyze prediction data and calculate key metrics.
    
    Args:
        json_file_path (str): Path to the input JSON file
        
    Returns:
        dict: Dictionary containing calculated metrics
    """
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    total_count = 0
    answered_count = 0
    correct_count = 0
    answered_correctly_count = 0

    for entry in data:
        total_count += 1
        prediction = entry['prediction']
        reference = entry['reference']
        is_correct = entry["model_evaluation_result"]
        is_answered = entry['is_answered']
        
        if is_answered:
            answered_count += 1
            if is_correct:
                correct_count += 1
    
    answer_rate = answered_count / total_count if total_count > 0 else 0
    accuracy_rate = correct_count / total_count if total_count > 0 else 0
    answered_accuracy_rate = correct_count / answered_count if answered_count > 0 else 0
    
    return {
        "answer_rate": answer_rate,
        "accuracy_rate": accuracy_rate,
        "answered_accuracy_rate": answered_accuracy_rate,
        "total_count": total_count,
        "answered_count": answered_count,
        "correct_count": correct_count
    }

def print_metrics(metrics):
    """Print the calculated metrics in a formatted manner."""
    print(f"1. Answer rate (Prediction is not 'none'): {metrics['answer_rate']:.2%}")
    print(f"2. Overall accuracy (Prediction = Reference): {metrics['accuracy_rate']:.2%}")
    print(f"3. Accuracy among answered (Correct predictions in answered entries): {metrics['answered_accuracy_rate']:.2%}")

def main():
    parser = argparse.ArgumentParser(description='Prediction accuracy analysis tool')
    parser.add_argument('--input_file', required=True, help='Path to the input JSON file')
    args = parser.parse_args()
    
    try:
        metrics = analyze_predictions(args.input_file)
        print_metrics(metrics)
    except FileNotFoundError:
        print(f"Error: File {args.input_file} not found")
    except json.JSONDecodeError:
        print(f"Error: {args.input_file} is not a valid JSON file")
    except KeyError as e:
        print(f"Error: Missing required field {e} in JSON data")

if __name__ == "__main__":
    main()