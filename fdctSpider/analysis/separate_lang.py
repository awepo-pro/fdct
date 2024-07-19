import pandas as pd 
from os.path import join, isfile, exists
from os import getcwd, listdir, remove


def get_files():
	relative_path = '../info/'
	folder_path = join(getcwd(), relative_path)
	files = [relative_path + f for f in listdir(folder_path) if isfile(join(folder_path, f)) and f.endswith('.json')]

	return files

def update_files():
	files = ['fdct_zh.json', 'fdct_pt.json', 'fdct_en.json']
	for file in files:
		if exists(file):
			remove(file)


def separate_lang():
	update_files()

	for file in get_files():
		print(f'{file=}')


		original = []
		with open(file) as input:
			while line := input.readline():
				original.append(line)
		original = original[1:]
		data_dict = pd.read_json(file).to_dict()

		with open('fdct_zh.json', 'a') as zh, open('fdct_pt.json', 'a') as pt, open('fdct_en.json', 'a') as en:
			for lang, line in zip(data_dict['lang'].values(), original):
				if lang == 'zh':
					zh.write(line)
				elif lang == 'pt':
					pt.write(line)
				else:
					en.write(line)


if __name__ == '__main__':
	separate_lang()