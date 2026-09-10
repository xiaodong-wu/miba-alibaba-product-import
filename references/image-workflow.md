# 图片：真实产品、原创详情、合理应用

## 区分用途

- 产品封面/组图：可使用用户授权来源的真实图库，品牌处理按用户指定目标执行，不固定替换为 Xinbada；800×800 完整主体，禁止拉伸或裁掉关键产品。补边优于裁剪。
- 新增详情介绍图：从产品真实外形出发，通过 imagegen 新创作。不能直接照搬 Alibaba 详情版式、背景、道具和文案，不能仅裁剪/滤镜/换 logo 后称为新图。
- 应用场景图：展示该产品有事实支持的合理应用；至少一张，用于 scenario_image 及相关新增详情小节；宽度至少 1200px。
- 末尾三个固定图片：按 [固定版块规则](fixed-blocks.md) 使用用户指定 PNG，角色 supplied_static，保留全部图像内容和原始比例，不用 imagegen 重做。

所有新详情图应在 image-plan 中标记 detail 或 scenario，并记录 generated=true；这只是来源记录，不代替人工核查。不伪造证书、客户工程或工厂现场，模拟图旁用英文标识概念展示。只在标签明确可核实时保留数字，检查 imagegen 没有新增或误改文字。无法可靠保留结构时改用更简单场景重试，仍不可靠则阻塞，不能退回原详情图充数。

## 图像提示词骨架

```text
Create an original application visualization of the referenced [verified product].
Preserve its actual [shape/material/connections/package proportions] faithfully.
Show it in [supported application] with physically plausible installation or use.
Use a new [viewpoint/composition/environment/lighting] distinct from the source listing.
Do not reproduce the source detail-page composition, graphics, text layout or background.
Use only the user's explicitly supplied target brand; otherwise create an unbranded image.
Do not invent specifications, certifications,
customer projects, labels or performance evidence. [Target aspect ratio and dimensions].
```

## image-plan.json

source 相对于清单文件解析，文件名用描述性英文；name 不含扩展名。每行商品有独立清单。

```json
{
  "images": [
    {"source": "staging/cover.png", "name": "product-white-background", "role": "cover", "generated": false},
    {"source": "staging/application.png", "name": "product-application-concept", "role": "scenario", "generated": true, "width": 1200},
    {"source": "staging/detail.png", "name": "product-detail-concept", "role": "detail", "generated": true, "width": 1000}
  ]
}
```

prepare_images.py 用 Pillow 进行尺寸/格式/压缩处理，不代替 imagegen 创作。输出目录仅存 WebP，处理记录写在目录旁的 `<folder>.image-manifest.json`。从质量 82 / method 6 开始，cover/gallery/detail 尝试降至质量 70 以接近 100 KB；不牺牲清晰度强制达到体积目标。超过 100 KB 由人工复核并记录接受理由；画质不足时用 --min-quality 82 重做。场景图清晰优先，不强制 100 KB。多帧图不静默丢帧，要求先选择合适静态图。

上传成功后，将每张本地图片与 Direct URL、角色、尺寸、alt 对照复核；重要图片 alt 唯一且与实际内容一致。首屏主图 loading=eager，其余按位置使用 lazy；新增图片必须带 width/height 防止布局跳动。站点级响应式图片派生/srcset 需求写入部署验收，不能伪造不同尺寸的 URL。
