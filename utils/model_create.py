from pathlib import Path
import yaml

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# from rewrite_params import rewrite_params


def get_GDrive_id(path):
    path_splitted = path.split('/')

    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for path_part in path_splitted:
        if not len(path_part):
            continue

        for file in file_list:
            if file['title'] == path_part:
                folder_ID = file['id']
        file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(folder_ID)}).GetList()
    return folder_ID


if __name__ == '__main__':
    ROOT = Path().resolve()

    # GDrive set up
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile(ROOT / 'mycreds.txt')
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(ROOT / 'mycreds.txt')

    drive = GoogleDrive(gauth)
    # params set up
    with open('params.yaml', 'r') as f:
        model_name = yaml.safe_load(f)['model_test']['name']
    model_name = model_name.split('.')[0]

    files_dict = {
        'model': {'name': 'yolov8_under.pt', 'path': f'/yolov8_train_results/{model_name}/weights/best.pt'},
        'args': {'name': 'args.yaml', 'path': f'/yolov8_train_results/{model_name}/args.yaml'}
    }

    for downloaded_file in files_dict:
        donwload_path = files_dict[downloaded_file]['path']
        file_name = files_dict[downloaded_file]['name']

        folder_ID = get_GDrive_id(donwload_path)
        file = drive.CreateFile({'id': folder_ID})

        print(f'Downloading file from: {donwload_path}')
        file.GetContentFile(ROOT / 'models' / file_name)
        print(f'{file_name} downloaded\n')

    # rewrite_params()
    # print('Model training parameters rewritten\n')
