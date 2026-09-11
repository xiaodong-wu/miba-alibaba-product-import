# 字段、执行与验收契约

## CSV

必须保留原字段、顺序、行数、UTF-8；使用 csv 模块处理 HTML 中的逗号、引号和换行，不使用文本按行拆 CSV。上传参数 row-number 是含表头计数的逻辑记录序号，首条商品为 2，不是多行 HTML 的物理行号。

| 字段 | 规则 |
|---|---|
| link、IMGBB_API_KEY | 原值逐字符保留；不得日志输出密钥 |
| 未知列 | 原值保留 |
| content | 英文产品正文 → 固定公司简介 → Factory Photo → MiBA Logo Options → MiBA Accessory Options → FAQ（最底部），统一居中容器最大宽度 1400px |
| title | 自然英文商品标题；目标品牌为 MiBA，按语义自然使用，用于页面主标题，不堆关键词 |
| remark | 1–2 句真实产品价值说明 |
| pro_fields | 4–8 条已验证卖点，各占一行，无项目符号、点、横线或编号 |
| file_name | 简短描述性小写英文数字及连字符，无扩展名；各行唯一 |
| seo_title1 | 单独编写，英文 Title Case，50–65 字符，目标约 60；主词靠前，MiBA 品牌通常放末尾；各行唯一 |
| seo_desc | 单独编写，不超过 140 字符；正文支持的优势与用途；各行唯一 |
| thumb | 封面图的 ImgBB WebP Direct URL |
| scenario_image | 原创场景图的 ImgBB WebP Direct URL，不是 Markdown |
| images | 1 张重新生成 cover + 至少 4 张重新生成 gallery，封面在前，有序换行分隔 `<url>|<alt>`；排除 detail/scenario/supplied_static 详情图；alt 英文、准确且不同 |

seo_title1 的 50–65 是用户文档编辑区间，不称为 Google 强制限制。全部新增文案英文，不自动继承来源品牌；品牌展示按 MiBA 人工核验，不将来源供应商资质归属于 MiBA。template 不再必填；已有 template 列仅保留源值，不使用其内容。

公司简介使用 [固定公司简介规则](company-profile.md) 和随包固定 HTML，逐字保留用户文案，置于三个固定图片之前。

## pro_fields

`pro_fields`：4–8 条已验证卖点，各占一行，无项目符号、点、横线或编号。

## 文件布局与命令

路径均可使用绝对路径，以下相对路径以任务输出目录为工作目录；scripts 路径需替换为本技能的真实绝对路径。

```text
input_completed.csv
images/<file_name>/<descriptive-name>.webp
staging/<file_name>/             # 不属于最终图库
evidence/<file_name>.json        # 来源、事实、关键词和缺失信息，无密钥
upload-manifests/<file_name>.json
review.json
validation.json
```

```text
python scripts/prepare_images.py image-plan.json --output-dir images/product-slug
python scripts/upload_images_to_imgbb.py images/product-slug --csv-file input.csv --row-number 2 --manifest upload-manifests/product-slug.json
python scripts/compose_content.py --detail-file product.detail.html --image-manifest images/product-slug.image-manifest.json --upload-manifest upload-manifests/product-slug.json --output content.html
```

拼接脚本不负责写 CSV，使用 csv.DictWriter 回填生成内容，不要输出行数据到终端。

## review.json

这是代理实际完成检查后写的记录，不是预先填 true 的通行证。所有 populated 行均要记录，空行不需要。缺事实/页面不可访问为 skipped；固定图片缺失、图像无法正确生成、上传失败等为 blocked；success 表示人工及自动校验待共同验证的成功候选。

```json
{
  "rows": [
    {
      "row_number": 2,
      "status": "success",
      "reason": "",
      "checks": {
        "facts_verified": true,
        "source_coverage_reviewed": true,
        "fixed_blocks_verified": true,
        "original_detail_images_verified": true,
        "generated_gallery_verified": true,
        "content_richness_reviewed": true,
        "layout_reference_reviewed": true,
        "visual_review_passed": true,
        "seo_document_reviewed": true
      },
      "evidence": "evidence/product-slug.json",
      "notes": ["说明检查依据，不能写密钥"]
    }
  ],
  "deployment_pending": ["CMS 外层 H1、canonical、图片 HTTP、Sitemap、robots 和真实用户 CWV 待上线环境检查"]
}
```

脚本自动检查 1400px 外层容器、组图与详情图分离、字段、源值保留、三个固定版块的标题、图片及顺序、FAQ/H1、元数据长度与唯一性、新增图片 URL 与 alt、本地 WebP 和图像角色尺寸。人工必须额外检查原文规范全部条目、商品一致性、独立文案、事实证据、图片视觉原创性/准确性、CSS 作用域及页面渲染。`success` 的人工记录不能覆盖自动错误。退出码 0 表示本地候选通过且无跳过，2 表示部分完成，1 表示校验错误；部署未验始终单独报告。

校验器从 `--images-dir` 的父目录读取 `upload-manifests/<file_name>.json`，对照上传结果、本地文件、图片角色和 CSV URL；CSV images 仅对照 cover/gallery，详情图则对照完整上传清单，二者不能混用。原创产品详情图使用 generated=true；末尾三个指定图使用 supplied_static，明确豁免 AI 生成要求，并仍需人工核查该标记真实。跳过/阻塞行的生成字段保留输入值，草稿放在表外，避免被误导入。

## 源码来源

上传辅助脚本基于 xiaodong-wu/xinbada-alibaba-product-import 提交 `1f5b0cc6b3cbe69dbf1cf9c1641d03c56ac93480` 的 MIT 许可代码，本版增加长 HTML CSV 字段支持；保留随包 LICENSE。其他流程与校验按本次需求重写。Google 规范附件为用户指定文件的完整原文快照，不是自动更新的 Google 官方规则库。

资料覆盖审查按 [source-coverage.md](source-coverage.md) 执行；source_coverage_reviewed 必须基于实际逐项核对。脚本只检查复核标记，不证明网页采集完整或内容正确。1400px 静态容器检查不代替实际浏览器布局检查。
