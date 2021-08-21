from tqdm import tqdm
from file import File

cacheDir = File(r'D:\QQFile\1805795356\Image\Group2')
exportDir = File('export')
historyDir = File('history')

if not cacheDir.exists:
	print(cacheDir.path+' not found')
	exit(1)

if not cacheDir.isDirectory:
	print(cacheDir.path+' was not a directory')
	exit(1)

exportDir.mkdirs()
historyDir.mkdirs()

# 加载已有的图片
exportsExisted = []

print("加载已有的图片")
with tqdm(total=len(exportDir)+len(historyDir), dynamic_ncols=True, unit='',
                      bar_format="{percentage:3.0f}% {bar} {n_fmt}/{total_fmt}{postfix}") as pbar:
	for ef in exportDir:
		filehash = ef.sha1
		if filehash not in exportsExisted:
			exportsExisted += [filehash]
			pbar.update(1)
	for ef in historyDir:
		filehash = ef.sha1
		if filehash not in exportsExisted:
			exportsExisted += [filehash]
			pbar.update(1)

print(f'已加载 {len(exportsExisted)} 个图片')

# 计算文件总数
totalCount = 0
def countDir(dir):
	global totalCount
	for file in dir:
		if file.isDirectory:
			countDir(file)
		if file.isFile:
			totalCount += 1
countDir(cacheDir)

# 收集新图片
print('收集新图片...')
with tqdm(total=totalCount, dynamic_ncols=True, unit='',
                      bar_format="{percentage:3.0f}% {bar} {n_fmt}/{total_fmt}{postfix}") as pbar:
	added = 0
	def walkDir(dir):
		global added
		for file in dir:
			if file.isDirectory:
				walkDir(file)
			if file.isFile:
				filehash = file.sha1
				if filehash not in exportsExisted:
					suffix = file.name.split('.')
					suffix.reverse()
					suffix = suffix[0]
					newfile = exportDir(filehash+'.'+suffix)
					file.copyTo(newfile)
					# print(newfile.name)
					added += 1
				pbar.update(1)
			
	walkDir(cacheDir)

print(f'\n找到了 {added} 个图片')