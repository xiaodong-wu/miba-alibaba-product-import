---
name: miba-alibaba-product-import-v2
description: 将 Alibaba 商品 CSV 转为英文商品导入数据，生成英文详情并在末尾追加指定的三个标题加图片版块，按指定 Google 产品优化规范创作应用场景图、转换 WebP、上传 ImgBB 并校验。用于含 link 的商品迁移表，不绑定固定品牌。
---

# Miba Alibaba Product Import V2

流程：Alibaba 链接 → 提取事实和图库 → 生成英文详情及原创应用场景图，并在详情下方追加三个固定图片版块 → WebP → ImgBB → 回填 CSV → 校验。

## 必读规则与优先级

执行前读取 [字段与交付规则](references/schema-and-workflow.md) 和用户指定的 Google 产品规范。
如用户提供本机规范文件路径，优先使用该文件。
本机文件可读时读其最新全文；无法访问时使用随包原文 [google-product-seo-requirements.md](references/google-product-seo-requirements.md)，告知使用了快照，不得声称读取了最新本机版本。

用户当前要求优先。Google 文档的规范必须落实；其中 BNS Railings 品牌、栏杆产品和参数是领域示例，不能直接套入当前商品。不绑定 Xinbada 或任何固定品牌、公司名。品牌和公司信息仅使用用户明确提供的目标信息；未提供时生成中性文案，不自动沿用来源商家、模板示例或历史品牌，不因缺少品牌而阻塞。技能标识为 miba-alibaba-product-import-v2，不代表输出必须使用 Miba 品牌。

本版明确替代旧版三项规则：
- 不再要求 HTML 模板，不再拼接旧模板。最终 content 为英文产品详情 + 三个固定纯图版块；详见 [固定图片版块](references/fixed-blocks.md)。
- `seo_title1`、`seo_desc` 按 Google 文档独立编写，不再强制等于 `title`、`remark`。
- 图片尺寸、命名、体积按 Google 文档执行；质量 82 / method 6 为初始值，不再要求所有图片保持原尺寸或只用数字命名。

## 执行

### 1. 检查输入与固定图片

保留输入文件，默认输出 `<input-stem>_completed.csv`。逐行检查 link 和 IMGBB_API_KEY；保留行顺序、原字段值和未知列。密钥仅由上传脚本读取，不打印整行或整表，不把含密钥 CSV 放入日志或 Git。

需要新表时使用 [空白字段模板](assets/content_import_template.csv)，无需 template 列。已有表若含 template，仅原样保留该列，不读取为生成依据、不拼入 content。检查三个指定本机 PNG，缺失时用随包同名副本；两者均缺失才报告阻塞，不能用 AI 替代这些指定图片。

### 2. 提取事实与搜索意图

用可用浏览器读取当前 Alibaba 页面及有必要查看的图库，提取标题、参数、材质/配方、结构、用途、包装和认证等实际可验证信息。保留数值和单位。规格属性冲突优先规格表；份量/营养信息优先清晰标签；仍有冲突则记录，不猜测。

每行写本地 evidence JSON：源 URL、访问时间、事实及对应可见原文/图像来源、1 个主关键词、2–5 个长尾词、缺失信息、冲突。禁止复用其他商品的事实。页面不可访问时跳过并记录原因，不猜测缺失参数。

### 3. 编写新增详情

逐项落实 Google 文档的关键词、元数据、图片、内容结构、页面体验及验收要求。用独立英文组织采购商需要的信息，不逐句翻译/复制 Alibaba 或旧模板文案。

新增区必须先概览，再按资料组织介绍、参数表、优势、应用、案例/模拟效果、包装交付、认证、工厂能力、公司优势及六个采购 FAQ。推荐栏目不是虚构事实的理由；没有依据的认证/案例不展示，没有交期等信息时说明需确认。公司名及 OEM/ODM 能力仅在用户提供或当前来源可验证时使用，不推断属于目标公司。

页面主要 H1 总计只能有一个。若网站外层已有产品标题 H1，详情从 H2 开始；否则使用 H1。未知外层情况记为部署待验。产品详情包含六个采购 FAQ，三个固定图片版块在 FAQ 及全部详情之后。

新增区采用 `.xb_import_v2` 命名空间，所有 CSS 选择器限定于此，移动端表格可横向滚动，图片提供 width/height 和响应式样式。只输出 HTML 片段，不引入 html/head/body、外部字体、全局 CSS、可执行 JavaScript 或 meta keywords。SEO 元数据填 CSV，不塞进详情 HTML。结构化数据属于站点集成，不能虚构评分/价格/库存。

将英文详情写入 `<file_name>.detail.html`，上传完成后通过 `scripts/compose_content.py` 追加三个固定图片版块，生成最终 content。固定版块每个仅有一个 H2 标题和一张图片，不添加介绍、说明、按钮或额外内容。

### 4. 图片创作与处理

先读 [图片制作规则](references/image-workflow.md)。提取图库用于识别真实商品及准备产品组图；新增详情和应用位置使用基于真实产品重新创作的图，必须调用 imagegen，不能直接使用 Alibaba 详情原图或仅换 logo 充当新图。末尾三个用户指定图片是明确例外：直接使用提供的 PNG 转 WebP，不重新生成、改字、裁切或变更图片内容。

图的应用环境、构图、视角和配色应有明显独立设计，同时保留产品真实结构、连接、包装比例及可核实标签。模拟图在相邻英文说明中标明 `Application concept visualization`，不能当成真实工程、客户或工厂照片。

取消 Lifeworth → Xinbada 的固定替换。用户指定目标品牌时用 imagegen 按其要求处理组图品牌，并检查其他标签文字和数字未变；未指定时新增图片采用无品牌设计，不擅自植入品牌，来源组图的品牌处理按用户具体要求执行。逐张视觉核对后准备角色清单，运行 `scripts/prepare_images.py`：gallery/cover 为 800×800；scenario 宽度至少 1200；detail 按版面确定。WebP 从质量 82、method 6 开始压缩，保真优先；超体积记录理由并复核。

### 5. 上传与回填

使用每行 CSV 中的 IMGBB_API_KEY，调用随包上传脚本；不得改用命令行明文密钥。只有该行全部所需图片上传成功后才回填图片字段。上传会对网络/429/5xx 有界重试；仍失败则记录，禁止无限重试。保留部分成功清单，重新尝试前检查它，脚本自身不提供断点续传。

thumb 用产品封面；scenario_image 用新生成应用图；images 收录最终图库（包括用于详情的原创图），按展示顺序逐行 `<url>|<English alt>`。只接受 `https://i.ibb.co/...webp` 的 data.url。详情和三个固定版块的图片均引用本行清单中的地址；images 最后依次追加 Factory Photo、MiBA Logo Options、MiBA Accessory Options 的链接。固定图片使用 supplied_static 角色，不占用 thumb 或 scenario_image。

### 6. 校验与交付

按 [字段与交付规则](references/schema-and-workflow.md) 记录行状态和人工复核结果，运行：

```text
python scripts/validate_output.py input.csv input_completed.csv --images-dir images --report validation.json --review review.json
```

修复成功行的全部错误。视觉复核英文详情及末尾三个图片版块的组合在手机和桌面下的效果，核对图片中的商品、标签、结构、模拟图说明以及事实来源。脚本不证明 SEO 收录、图片原创性或事实真实性。

交付完成版 CSV、本地 WebP、上传清单、证据记录及校验报告；报告成功/跳过/阻塞行数。存在跳过或阻塞时明确为部分完成。原 CSV 密钥列按原要求保留，因此含密钥的完成表仅交还用户，不用作公开示例。站点 canonical、301、站内链接、Sitemap、robots、hreflang、HTTP 图片可访问性及 CWV 等没有部署环境时列为待验，不能声称通过或擅自发布。
