# fuyohai-recognition
### Djangoを用いたWebアプリケーションの形で実装しました
1. OpenCVのマーカーを麻雀卓に配置し、写真を撮影することで、牌の自動認識を行います。
2. 認識された牌は[不要牌類似計量法式](https://ipsj.ixsq.nii.ac.jp/ej/index.php?active_action=repository_view_main_item_detail&page_id=13&block_id=8&item_id=210937&item_no=1)を用いて解析を行い、推定結果をユーザに返します。

### Motivation
- [不要牌類似計量法式](https://ipsj.ixsq.nii.ac.jp/ej/index.php?active_action=repository_view_main_item_detail&page_id=13&block_id=8&item_id=210937&item_no=1)をより使いやすい形で実装を行いました。

### Trick
- マーカーを用い、座標を取得することで射影変換行う
- 特徴量マッピングを行うための矩形抽出+二値化
- Chart.jsを用いたUI向上

### マーカーを用いた射影変換
![demo](./media/transform.png)

### A-KAZEを用いた類似度軽量
![demo](./media/akaze.png)

### デモ画像
![demo](./media/demo.png)

### 環境
- python3.8
- Django 3.2.5
- opencv-python 4.5.3.56
