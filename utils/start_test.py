import json
import os
import argparse
from ultralytics import YOLO
import torch
from pathlib import Path
import shutil
from ultralytics.yolo.utils import metrics
from utils_ import ap_per_class_prc


def create_args_parser():
    pars = argparse.ArgumentParser()
    pars.add_argument('--model_path', nargs='?', type=str, help="", default='./models/yolov8_under.pt')
    pars.add_argument('--data_path', nargs='?', type=str, help="", default='./datasets/yolo.yaml')
    pars.add_argument('--conf', nargs='?', type=float, help="", default=0.001)
    pars.add_argument('--iou', nargs='?', type=float, help="", default=0.7)
    pars.add_argument('--split', nargs='?', type=str, help="", default='test')
    result = pars.parse_args()
    return result


if __name__ == '__main__':
    ROOT = Path().resolve()
    Path(ROOT / 'metrics').mkdir(parents=True, exist_ok=True)
    Path(ROOT / 'plots').mkdir(parents=True, exist_ok=True)

    parser_args = create_args_parser()

    model_path = parser_args.model_path
    data_path = parser_args.data_path
    conf = parser_args.conf
    iou = parser_args.iou
    split = parser_args.split

    model = YOLO(model_path)

    metrics.ap_per_class = ap_per_class_prc

    test_res = model.val(data_path, iou=iou, conf=conf, split='test', project=ROOT / 'runs')
    with open(ROOT / 'metrics' / 'metrics.json', 'w') as f:
        json.dump(test_res.results_dict, f)

    torch.cuda.empty_cache()
    shutil.rmtree('./runs')
