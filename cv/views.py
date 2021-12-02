import base64
from pathlib import Path

import cv2
from django.shortcuts import render

from . import forms
from .mahjong import mahjong, mahjong_sim


def index(request):
    return render(request, 'cv/index.html')


def hazard(request):
    if request.method == 'POST':
        form = forms.ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            base_dir = Path(__file__).resolve().parent.parent
            filename = form.cleaned_data.get('img').name
            filepath = str(base_dir / 'media/image' / filename)
            img = cv2.imread(filepath)
            res = mahjong.Analyze(img).read_river('')
            df = mahjong.gen_pai_df(res)
            dic, suit_dic = mahjong_sim.sutehai_sim(res)
            context = {
                'query': ndarray2base64(cv2.resize(img, (500, int(img.shape[0] / img.shape[1] * 500)))),
                'form': form,
                'msg': 'アップロード成功！',
                'df': df,
                'dic': dic,
                'suit_dic': suit_dic,
            }
            return render(request, 'cv/image-feature.html', context)
    contexts = {'form': forms.ImageForm(),}
    return render(request, 'cv/image-feature.html', contexts)

def ndarray2base64(dst):
    _, dst_data = cv2.imencode('.jpg', dst)
    dst_base64 = base64.b64encode(dst_data).decode().replace("'", "")
    return dst_base64
