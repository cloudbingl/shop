#### Install
```
pip install django
pip install django-tinymc
pip install django-haystack
pip install jieba
pip install whoosh
pip install pillow
```
#### 搜索的配置
在路径`venv/site-packages/haystack/backends`中创建 `ChineseAnalyzer.py` 文件
```
import jieba
from whoosh.analysis import Tokenizer, Token


class ChineseTokenizer(Tokenizer):
    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0, mode='', **kwargs):
        t = Token(positions, chars, removestops=removestops, mode=mode,
                  **kwargs)
        seglist = jieba.cut(value, cut_all=True)
        for w in seglist:
            t.original = t.text = w
            t.boost = 1.0
            if positions:
                t.pos = start_pos + value.find(w)
            if chars:
                t.startchar = start_char + value.find(w)
                t.endchar = start_char + value.find(w) + len(w)
            yield t


def ChineseAnalyzer():
    return ChineseTokenizer()
```
复制当前文件夹内的 whoosh_backend.py 文件，改名为 whoosh_cn_backend.py ，在此文件内修改。
```
# 导入模块
from .ChineseAnalyzer import ChineseAnalyzer

# 将模块中的  analyzer=StemmingAnalyzer()
# 替换为  analyzer=ChineseAnalyzer()
```
初始化索引
```
python manage.py rebuild_index
```