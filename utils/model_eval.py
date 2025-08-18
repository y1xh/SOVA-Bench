import argparse
import os
import json
from openai import OpenAI
from utils import load_data_from_json, save_result_to_json,load_prompt_from_file
from read_result_paralinguistic import result_correctness_emotion,result_correctness_gender,result_correctness_age
def evaluate_model_answer(client, prompt_template, question, prediction, reference):
    """Construct prompt using template and call GPT API for evaluation"""
    formatted_prompt = prompt_template.format(
        question=question,
        prediction=prediction,
        reference=reference
    )
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": formatted_prompt}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        return None
def evaluate_predictions(args):
    # Initialize OpenAI client
    client = OpenAI(api_key=args.api_key)
    
    # Load data and prompt template
    data = load_data_from_json(args.input_file)
    prompt_template = load_prompt_from_file(args.prompt_file)
    results = []

    import pdb
    pdb.set_trace()

    if args.task in ('spoken_QA', 'knowledge', 'generation'):
        for item in data:
            question = item.get('question', '')
            prediction = item.get('prediction', '')
            reference = item.get('answer', '')
            item_id = item.get('id', '')
            
            print(f"Evaluating ID: {item_id}")

            result = evaluate_model_answer(client, prompt_template, question, prediction, reference)
            result_item = {
                "id": item_id,
                "model_evaluation_result": result,
                "question": question,
                "prediction": prediction,
                "reference": reference
            }
            results.append(result_item)
            print(f"Result for ID: {item_id} - Evaluation: {result} saved to {args.output_file}")
            # Save all results to output file
            save_result_to_json(result_item, args.output_file)
    else:   
        for item in data:
            question = item.get('question', '')
            prediction = item.get('prediction', '')
            reference = item.get('answer', '')
            item_id = item.get('id', '')
            
            print(f"Evaluating ID: {item_id}")

            retrieved_result = evaluate_model_answer(client, prompt_template, question, prediction, reference)
            if args.task == 'emotion':
                is_answered, result = result_correctness_emotion(retrieved_result, reference)
            elif args.task == 'gender':
                is_answered, result = result_correctness_gender(retrieved_result, reference)
            elif args.task == 'age':
                is_answered, result = result_correctness_age(retrieved_result, reference)
            
            result_item = {
                "id": item_id,
                "model_evaluation_result": result,
                "is_answered": is_answered,
                "question": question,
                "prediction": prediction,
                "reference": reference
            }

            results.append(result_item)
            print(f"Result for ID: {item_id} - Evaluation: {result} saved to {args.output_file}")
            # Save all results to output file
            save_result_to_json(result_item, args.output_file)


    print(f"All results saved to {args.output_file}")

def main():
    parser = argparse.ArgumentParser(description='Evaluate model predictions using GPT-4o-mini')
    parser.add_argument('--task', default='knowledge', choices=['spoken_QA', 'knowledge','emotion','gender','age','generation'], help='Task to evaluate')
    parser.add_argument('--input_file', required=True, help='Path to input JSON file')
    parser.add_argument('--output_file', required=True, help='Path to output JSON file')
    parser.add_argument('--prompt_file', required=True, help='Path to prompt template text file')
    parser.add_argument('--api_key', required=True, help='OpenAI API key')
    
    args = parser.parse_args()
    os.makedirs(os.path.dirname(args.output_file), exist_ok=True)
    evaluate_predictions(args)

if __name__ == "__main__":
    main()