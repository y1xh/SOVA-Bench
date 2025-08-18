import os
import json
import re
import argparse
from collections import defaultdict
import editdistance as ed
from util.evaluate_tokenizer import EvaluationTokenizer
from util.whisper_normalizer.english import EnglishTextNormalizer
from utils import load_data_from_json

english_normalizer = EnglishTextNormalizer()

def remove_sp(text):
    gt = re.sub(r"<\|.*?\|>", " ", text)
    gt = re.sub(rf"\s+", r" ", gt)  
    gt = re.sub(f" ?([!,.?;:])", r"\1", gt)
    gt = re.sub(r"-", " ", gt)  
    gt = gt.lstrip(" ")

    return gt

def compute_wer(refs, hyps):
    distance = 0
    ref_length = 0
    tokenizer = EvaluationTokenizer(
            tokenizer_type="none",
            lowercase=True,
            punctuation_removal=True,
            character_tokenization=False,
        )
    for i in range(len(refs)):
        ref = refs[i]
        pred = hyps[i]

        ref = english_normalizer(ref)
        pred = english_normalizer(pred)

        ref_items = tokenizer.tokenize(ref).split()
        pred_items = tokenizer.tokenize(pred).split()

        distance += ed.eval(ref_items, pred_items)
        ref_length += len(ref_items)
        
    return distance, ref_length

def main(args):
    predicted_texts = load_data_from_json(args.predictions_file)
    
    total_distance = 0
    total_ref_length = 0

    results = []
    for pred_text in predicted_texts:
        question_id = pred_text['id']
        prediction = pred_text['transcription']
        answer = pred_text['reference']
        
        gt = remove_sp(answer)
        transcription = remove_sp(prediction)
        
        distance, ref_length = compute_wer([gt], [transcription])

        total_distance += distance
        total_ref_length += ref_length

        wer = distance / ref_length if ref_length != 0 else 0

        results.append({
            'id': question_id,
            'wer': wer
        })
    
    total_wer = total_distance / total_ref_length if total_ref_length != 0 else 0

    for result in results:
        print(f"ID: {result['id']}, WER: {result['wer']:.4f}")

    print(f"Total WER: {total_wer:.4f}")

    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write(json.dumps({'total_wer': total_wer}) + '\n')
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='compute wer')
    parser.add_argument('--predictions_file', required=True, help='Input predictions file path')
    parser.add_argument('--output_file', required=True, help='Output file path')
    
    args = parser.parse_args()

    main(args)    