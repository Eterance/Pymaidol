import argparse
import os
from pymaidol.code_templates.SubClassTemplate import SubClassTemplate


parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', type=str, help="the class name of the pymaidol files")
parser.add_argument('-d', '--dir', type=str, help="the directory of the pymaidol files", default="")
args = parser.parse_args()
path = args.dir
template_file_path =  os.path.join(path, f'{args.name}.pymd')
code_file_path =  os.path.join(path, f'{args.name}.py')
# designer file
if os.path.exists(template_file_path):
    message = f'Fail: file "{template_file_path}" already exist'
    print(f'\033[0;31;49m{message}\033[0m')
else:
    with open(template_file_path, 'w', encoding='utf-8') as f:
        f.write("")
        f.close()
    message = f'Success: file "{template_file_path}" created'
    print(f'\033[0;32;49m{message}\033[0m')
# py file
if os.path.exists(code_file_path):
    message = f'Fail: file "{code_file_path}" already exist'
    print(f'\033[0;31;49m{message}\033[0m')
else:
    template = SubClassTemplate(args.name)
    with open(code_file_path, 'w', encoding='utf-8') as f:
        f.write(template.Render())
        f.close()
    message = f'Success: file "{template_file_path}" created'
    print(f'\033[0;32;49m{message}\033[0m')
