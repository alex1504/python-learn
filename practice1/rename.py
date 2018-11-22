# 批量重命名文件
import os

def main():
    cwd = os.getcwd()
    imgDir = os.path.join(cwd, 'images')
    files = os.listdir('images')
    count = 1
    for file in files:
        src = os.path.join(imgDir, file)
        filename = os.path.splitext(file)[0]
        ext = os.path.splitext(file)[1]
        dist = os.path.join(imgDir, str(count) + ext)
        os.rename(src, dist)
        count += 1

if __name__ == "__main__":
    main()
