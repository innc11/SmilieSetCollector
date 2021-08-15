from file import File

cacheDir = File(r'D:\QQFile\1805795356\Image\Group2')
# cacheDir = File(r'1')
exportDir = File('exports')
historyDir = File('all')

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
for ef in exportDir:
	filehash = ef.sha1
	if filehash not in exportsExisted:
		exportsExisted += [filehash]
for ef in historyDir:
	filehash = ef.sha1
	if filehash not in exportsExisted:
		exportsExisted += [filehash]
print(f'found {len(exportsExisted)} files in export directory')

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
				print(newfile.name)
				added += 1
			
walkDir(cacheDir)

print(f'collected {added} pictures.')