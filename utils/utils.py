import json
def load_data_from_json(file_path):
    """从指定路径加载JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def load_prompt_from_file(file_path):
    """Load evaluation prompt template from a text file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read().strip()
        
def save_result_to_json(result, output_file):
    """将单个结果追加到JSON文件中"""
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            results = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        
        results = []

    results.append(result)

    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(results, file, ensure_ascii=False, indent=4)
