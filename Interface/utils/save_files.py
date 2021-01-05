import imghdr
import os
import pathlib
from .utils import uuid_32_upper


# 判断文件夹路径是否可用
def save_folder_effective(folder):
    path = pathlib.Path(folder)
    if not path.exists():
        try:
            os.makedirs(folder)
        except Exception as e:
            print(e)
            return False
    return True


# 按指定路径保存文件并返回文件名
def save_file(path, file):
    file_name = uuid_32_upper() + '.' + file.filename.split('.')[-1]
    try:
        file_dir = os.path.join(path, file_name)
        file.save(file_dir)
    except Exception as e:
        print(e)
        return False
    return file_name


# 判断是否是图片
def is_image(file):
    image_type_list = {'jpg', 'bmp', 'png', 'jpeg', 'rgb', 'tif', 'gif',
                    'pbm', 'pgm', 'ppm', 'tiff', 'rast', 'xbm', 'webp', 'exr'}
    if imghdr.what(file) not in image_type_list:
        return False
    return True


def get_image(path, file_name):
    image_path = os.path.join(path, file_name)
    mimetype_dict = {
        'jpeg': 'image/jpeg',
        'jpg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif'
    }
    mime = mimetype_dict[(file_name.split('.')[-1])]
    if not os.path.exists(image_path):
        return False
    with open(image_path, 'rb') as f:
        image = f.read()
    return {'image': image, 'mime': mime}
#
# if os.path.isfile(path):
#             img = Image.open(path)
#             imgSize = img.size #图片的长和宽
#             if(imgSize[0]>w):
#                 w = imgSize[0]
#             if (imgSize[1] > h):
#                 h = imgSize[1]
#
# im = Image.open('/home/shaoyidu/Program/pythonCnn/baidu/dataset/train0/%s' % name)
#         #im = im.resize((1024,48),PIL.Image.ANTIALIAS)
#         # 制作最大尺寸 1024*48 背景用白色填充
#         newim = Image.new('RGB', (maxw, maxh), 'white')
#         w, h = im.size
#         scale= min(maxw/w,maxh/h)
#         print(w,h)
#         out = im.resize((int(w*scale),int(h*scale)))
#         newim.paste(out,(0,0))
#         #newim.show()
#         newim.save('/home/dataset/train_max0/%s' % name)
