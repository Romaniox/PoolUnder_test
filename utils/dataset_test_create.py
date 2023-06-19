import yaml
from pathlib import Path

if __name__ == '__main__':
    ROOT = Path().resolve()
    print(ROOT)

    with open(ROOT / 'params.yaml', 'r') as f:
        src_dataset_path = yaml.safe_load(f)['dataset']['path_test']

    data_yaml2 = {
        'names': {0: 'person'},
        'path': src_dataset_path,
        'test': 'images/test',
        'train': 'images/train',
        'val': 'images/val'
    }

    with open(ROOT / 'dataset' / 'yolo.yaml', 'w') as f:
        yaml.safe_dump(data_yaml2, f)
