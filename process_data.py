import os 
import json


def read_json(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    return data


def write_json(data: list, output_name: str):
    with open(output_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


def qwen_create_conversation(img_dir: str, anotation: list) -> dict:
    conversations = []
    question = anotation['question']
    answers = anotation['answer']
    human_prompt = f"Picture 1: <img>{img_dir}</img>\n{question}"
    conversations.append({
        'from': 'user',
        'value': human_prompt.format(question=question),
    })
    conversations.append({
        'from': 'assistant',
        'value': answers,
    })
    return conversations


def qwen_main(img_dir, json_path, saved_dir):
    label_data = read_json(json_path)
    images = label_data['images']
    annotations = label_data['annotations']
    out_jsons = {}
    not_exist = []
    count = 0
    for k, v in annotations.items():
        img_id = v["image_id"]
        img_path = os.path.join(img_dir, images[str(img_id)])
        if not os.path.exists(img_path):
            not_exist.append(img_path)
            continue
        if count not in out_jsons:
            out_jsons[count] = []
        out_jsons[count].extend(qwen_create_conversation(img_path, v))
        count += 1

    format_out_jsons = []
    idx = 0
    for k, v in out_jsons.items():
        format_out_jsons.append({
            'id': str(idx),
            'conversations': v
        })
        idx += 1
    write_json(format_out_jsons, saved_dir)
    print(f"Done! {len(not_exist)} images do not exist")
    print(not_exist)

def llava_create_conversation(img_dir: str, anotation: list) -> dict:
    conversations = []
    question = anotation['question']
    answers = anotation['answer']
    human_prompt = f"<image>\n{question}"
    conversations.append({
        'from': 'human',
        'value': human_prompt.format(question=question),
    })
    conversations.append({
        'from': 'gpt',
        'value': answers,
    })
    return conversations


def llava_main(img_dir, json_path, saved_dir):
    label_data = read_json(json_path)
    images = label_data['images']
    annotations = label_data['annotations']
    out_jsons = {}
    not_exist = []
    count = 0
    for k, v in annotations.items():
        img_id = v["image_id"]
        img_path = os.path.join(img_dir, images[str(img_id)])
        if not os.path.exists(img_path):
            not_exist.append(img_path)
            continue
        if img_id not in out_jsons:
            out_jsons[img_id] = []
        out_jsons[img_id].extend(llava_create_conversation(img_path, v))
        print(out_jsons[img_id])
        count += 1
        # import pdb; pdb.set_trace()

    format_out_jsons = []
    idx = 0
    for k, v in out_jsons.items():
        format_out_jsons.append({
            'id': str(idx),
            'image': os.path.join(img_dir, images[str(k)]),
            'conversations': v
        })
        idx += 1
    write_json(format_out_jsons, saved_dir)
    print(f"Done! {len(not_exist)} images do not exist")
    print(not_exist)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.realpath(__file__))
    json_path = os.path.join(current_dir, 'vlsp2023_train_data.json')
    img_dir = os.path.join(current_dir, 'training-images')
    saved_dir = os.path.join(current_dir, 'llava_format_train.json')
    # qwen_main(img_dir, json_path, saved_dir)
    llava_main(img_dir, json_path, saved_dir)
    print("Done") 