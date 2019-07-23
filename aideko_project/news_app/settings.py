import os


CUR_DIR_DECONSTRUCTED: list = __file__.split('/')
APP_DIR: str = '/'.join(CUR_DIR_DECONSTRUCTED[0:len(CUR_DIR_DECONSTRUCTED)-1]) + '/models/'

NEWS_PATH: str = os.path.join(APP_DIR, 'news.json')
COMMENTS_PATH = os.path.join(APP_DIR, 'comments.json')