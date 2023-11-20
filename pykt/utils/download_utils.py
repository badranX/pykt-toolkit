#this code was partly adapted from https://github.com/HFUT-LEC/EduStudio

from contextlib import closing
from tqdm import tqdm
import requests
import zipfile
import pathlib
import os, tempfile

class BigfileDownloader(object):
    @staticmethod
    def download(url, title, filepath, chunk_size=10240):
        with closing(requests.get(url, stream=True)) as resp:
            if resp.status_code != 200:
                raise Exception("[ERROR]: {} - {} -{}".format(str(resp.status_code), title, url))
            chunk_size = chunk_size
            content_size = int(resp.headers['content-length'])
            with tqdm(total=content_size, desc=title, ncols=100) as pbar:
                with open(filepath, 'wb') as f:
                    for data in resp.iter_content(chunk_size=chunk_size):
                        f.write(data)
                        pbar.update(len(data))


class DecompressionUtil(object):
    @staticmethod
    def unzip_file(zip_src, dst_dir):
        r = zipfile.is_zipfile(zip_src)
        if r:     
            fz = zipfile.ZipFile(zip_src, 'r')
            for file in tqdm(fz.namelist(), desc='unzip...', ncols=100):
                fz.extract(file, dst_dir)       
            return fz.namelist()
        else:
            raise Exception(f'{zip_src} is not a zip file')
        

class FileEncodingUtil(object):
    BLOCKSIZE = 131072
    @classmethod
    def change_encoding(cls, src_path, src_encoding, trg_encoding='utf-8'):
        trg_path = src_path + 'pykt.org.tmp_file'
        with open(src_path, 'r', encoding=src_encoding) as src_f, open(trg_path, 'w', encoding=trg_encoding) as trg_f:
            while True:
                buffer = src_f.read(cls.BLOCKSIZE)
                if not buffer:
                    break
                trg_f.write(buffer)
        
        pathlib.Path(src_path).unlink()
        pathlib.Path(trg_path).rename(src_path)
    
        
if __name__ == '__main__':
    foo = u'Δ, Й, ק, م, ๗, あ, 叶, 葉, and 말.'
    foo += "---normal text"
    tmp = tempfile.NamedTemporaryFile(mode='w', encoding='utf-16', delete=False)
    tmp.write(foo)
    tmp.close()
    
    ChangeEncoding.change_encoding(tmp.name, 'utf-16')
    print('file content: ', open(tmp.name, mode='r', encoding='utf-8').read())
    os.unlink(tmp.name)
