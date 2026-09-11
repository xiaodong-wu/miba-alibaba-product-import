# 正文与 FAQ 之间的三个纯图版块

无需 HTML 模板。英文产品正文和固定公司简介结束后，严格按以下顺序插入三个版块；随后输出六个 FAQ，FAQ 必须位于整份详情最底部。标题取原始文件名去掉扩展名，大小写和空格保持不变：

| 顺序 | H2 标题 | 首选本机文件 | WebP 文件名 |
|---|---|---|---|
| 1 | Factory Photo | `C:\Users\wulic\Desktop\miba\Factory Photo.png` | factory-photo.webp |
| 2 | MiBA Logo Options | `C:\Users\wulic\Desktop\miba\MiBA Logo Options.png` | miba-logo-options.webp |
| 3 | MiBA Accessory Options | `C:\Users\wulic\Desktop\miba\MiBA Accessory Options.png` | miba-accessory-options.webp |

本机文件不可用时读取随包 `assets/fixed-blocks/` 同名副本并告知。仅转 WebP 和合理压缩，保留完整画面、原始像素尺寸、比例和图中文字；不改品牌、不裁剪、不用 AI 重绘。这三张指定素材不受“新详情图必须 AI 原创”限制，不代表所有文案都必须带 MiBA 品牌。

每版块仅 `section > h2 + img`，不加段落、图注、列表或按钮。alt 使用标题，width/height 使用实际尺寸，loading=lazy，图片在最大 1400px 的完整详情容器内响应式全宽且保持比例。压缩后文件名不用于显示标题。

每行 image-plan 的 images 数组在产品图后追加以下三个对象：

```json
[
  {"source":"C:/Users/wulic/Desktop/miba/Factory Photo.png","name":"factory-photo","role":"supplied_static","generated":false},
  {"source":"C:/Users/wulic/Desktop/miba/MiBA Logo Options.png","name":"miba-logo-options","role":"supplied_static","generated":false},
  {"source":"C:/Users/wulic/Desktop/miba/MiBA Accessory Options.png","name":"miba-accessory-options","role":"supplied_static","generated":false}
]
```

prepare_images.py 记录源文件名、SHA-256、标题和输出尺寸。按原流程上传 WebP；三个链接仅用于 content 的固定版块，不写入 CSV images；thumb/scenario_image 仍用商品图/原创应用图。compose_content.py 根据图片和上传清单，将三个固定版块插入正文与 FAQ 之间。

固定图含文字，默认质量 82，不为达到 100 KB 降低质量；较大文件记录清晰度例外。逐图核对原图与转换图。HTML 图片 src 必须为上传后的直链，不写本机路径。

固定版块外层左右 padding 为 0，上下保留适当间距；H2 标题统一加粗（700）居中。
