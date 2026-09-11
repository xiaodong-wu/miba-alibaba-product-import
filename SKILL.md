---
name: miba-alibaba-product-import-v2
description: 将 Alibaba 商品 CSV 转为英文商品导入数据，重新生成封面和至少四张组图，生成丰富的模块化英文详情并在正文与最底部FAQ之间插入固定公司简介及三个标题加图片版块，按指定 Google 产品优化规范创作应用场景图、转换 WebP、上传 ImgBB 并校验。用于含 link 的商品迁移表，不绑定固定品牌。
---

# Miba Alibaba Product Import V2

流程：Alibaba 链接 → 提取事实和图库 → 生成英文详情及原创应用场景图，并在详情下方追加三个固定图片版块 → WebP → ImgBB → 回填 CSV → 校验。

## 必读规则与优先级

执行前读取 [字段与交付规则](references/schema-and-workflow.md) 和用户指定的 Google 产品规范。
原文路径：`C:\Users\wulic\Desktop\miba\谷歌搜索引擎产品优化要求.md`。
本机文件可读时读其最新全文；无法访问时使用随包原文 [google-product-seo-requirements.md](references/google-product-seo-requirements.md)，告知使用了快照，不得声称读取了最新本机版本。

用户当前要求优先。Google 文档的规范必须落实；其中 BNS Railings 品牌、栏杆产品和参数是领域示例，不能直接套入当前商品。不绑定 Xinbada 或任何固定品牌、公司名。品牌和公司信息仅使用用户明确提供的目标信息；未提供时生成中性文案，不自动沿用来源商家、模板示例或历史品牌，不因缺少品牌而阻塞。技能标识为 miba-alibaba-product-import-v2，不代表输出必须使用 Miba 品牌。

本版明确替代旧版三项规则：
- 不再要求 HTML 模板，不再拼接旧模板。最终 content 为英文产品详情 + 三个固定纯图版块；详见 [固定图片版块](references/fixed-blocks.md)。
- `seo_title1`、`seo_desc` 按 Google 文档独立编写，不再强制等于 `title`、`remark`。
- 图片尺寸、命名、体积按 Google 文档执行；质量 82 / method 6 为初始值，不再要求所有图片保持原尺寸或只用数字命名。

## Current fidelity and layout requirements

Read [Product identity and MiBA layout](references/identity-and-miba-layout.md) before generation. This supersedes conflicting image-redraw and S1-S9 layout guidance: preserve the real product, and follow the supplied MiBA product-detail page structure. Previously rejected images must not be reused. The latest image-source rule below overrides earlier physical-photo priority and novelty requirements.

## 最新排版与属性换行规则

以下规则优先于旧排版参考：
- 所有版块外层左右 padding 为 0（包括概览、正文、公司简介、三个固定图片区和 FAQ），手机端同样为 0。上下保留合适间距，建议桌面 28–40px、手机 20–28px；表格单元格等内部必要间距可保留。
- 同一段文字保持在同一个连续文本块中，不拆成左右两栏，不使用 CSS 多栏分流。图文可左右排列，不同主题的独立版块可并排；每段正文须完整留在所属版块内，窄屏自然堆叠。
- 每个版块的标题统一用 `<h2>`，`font-weight:700;text-align:center`。不要用 H3、普通 div 或行内粗体冒充版块标题；段内标签和 FAQ 问题不属于版块标题。
- `pro_fields` 必须在 CSV 同一单元格内一行一条，共 4–8 条。第一条不加分隔符，从第二条开始每行行首紧贴添加一次 ``|`-+#$&*|``；条目之间仍使用真实 LF 连接。保存后重新读取并检查 3–7 个真实换行；详情预览的属性区模拟现有 PHP `nl2br()` 展示，肉眼确认逐条换行。禁止以空格、分号、字面量 `\n` 或 `<br>` 替代 CSV 中的换行。详见字段规则。

## 执行

### 1. 检查输入与固定图片

保留输入文件，默认输出 `<input-stem>_completed.csv`。逐行检查 link 和 IMGBB_API_KEY；保留行顺序、原字段值和未知列。密钥仅由上传脚本读取，不打印整行或整表，不把含密钥 CSV 放入日志或 Git。

需要新表时使用 [空白字段模板](assets/content_import_template.csv)，无需 template 列。已有表若含 template，仅原样保留该列，不读取为生成依据、不拼入 content。检查三个指定本机 PNG，缺失时用随包同名副本；两者均缺失才报告阻塞，不能用 AI 替代这些指定图片。

### 2. 完整提取资料与搜索意图

BrowserAct 浏览器偏好：先检查其可连接的现有浏览器与标签页，优先复用用户已打开的普通浏览器及登录状态；访问新商品时在该浏览器中打开普通标签页，不主动使用无痕/隐私模式或隔离的临时浏览上下文。不覆盖或关闭用户原有标签页。需要人工验证时保持可见窗口，用户完成后继续同一标签页。只有没有可复用的浏览器时才按 BrowserAct 能力和规则打开可见的普通浏览器；若无法连接已有浏览器或无法保留普通会话，明确说明实际限制，不把新建隔离会话称为复用。用户已要求不使用 Codex 内置浏览器，不自动回退至内置浏览器。

先读 [来源覆盖检查](references/source-coverage.md)。尽可能完整使用当前商品链接内可访问、可验证且与采购决策有关的资料，不能只读标题和首屏就生成简略详情。展开参数与详情、滚动加载全部相关图片、检查规格选项与包装交付等信息；逐项记录已提取、已使用、未使用的理由和未能访问的区域。

用可用浏览器读取当前 Alibaba 页面全部相关区域及图库，提取标题、参数、材质/配方、结构、用途、包装和认证等实际可验证信息。保留数值和单位。规格属性冲突优先规格表；份量/营养信息优先清晰标签；仍有冲突则记录，不猜测。

每行写本地 evidence JSON：源 URL、访问时间、事实及对应可见原文/图像来源、资料覆盖清单、各项事实对应的详情小节或未采用理由、1 个主关键词、2–5 个长尾词、缺失信息、冲突。禁止复用其他商品的事实。页面不可访问时跳过并记录原因，不猜测缺失参数。

### 3. 编写新增详情

读取[固定公司简介规则](references/company-profile.md)。产品正文之后固定插入用户提供的公司简介，逐字保留文案，仅重新排版；其后依次是三个指定图片区，FAQ 在最底部。固定简介由拼接器从 assets/company-profile.html 读取，不在生成正文中重复编写。该版块中的 MiBA 品牌、公司能力和商业条款是用户明确提供的例外，不自动归属到其他商品参数或 SEO 中。

前台文案面向购买者，直接介绍有依据的产品结构、功能、用途和选择。禁止把 evidence、审核意见、AI制作过程或“供应商声称但未核验”的清单作为产品卖点/图注发布。无法支持的协议、认证、保护功能、磁铁等级等不以确定语气改写；省略该卖点并在内部报告说明原因。不能通过删除免责声明把未证实信息变成承诺。适配型号、电源要求、配件是否包含等影响购买的信息仍需保留，写成简洁的产品条件或配置说明。交付前单独检查正文、表格、图注、FAQ、SEO及alt，确保它们都是客户需要的信息。

先读 [内容与排版规则](references/content-layout.md)，再读取用户排版参考 `C:\Users\wulic\Desktop\产品详情内容排版.txt`；本机不可读时使用 [随包排版参考](references/product-detail-layout-source.txt)，说明使用快照。参考图为 S1–S9 结构示意，按商品事实选择双栏图文、交错图文和多列卡片，不是必须机械填满的九个模板。

详情应充分展开已核实的结构、功能、操作、适配、选型、应用、包装和定制信息，以“事实 → 采购意义 → 使用条件”组织正文。不能仅用简短概览、参数表和大量待确认提示构成整页，也不能靠同义改写、重复 FAQ、无依据的卖点或虚构案例凑篇幅。先制作 evidence.content_plan，再写正文；来源差异、核验过程、未证实卖点及其未采用理由保留在 evidence/review，不直接写成客户正文。无法可靠解决的参数不作为前台确定规格；影响购买的限制改成简洁、具体的选型说明。

逐项落实 Google 文档的关键词、元数据、图片、内容结构、页面体验及验收要求。用独立英文组织采购商需要的信息，不逐句翻译/复制 Alibaba 或旧模板文案。

新增区必须先概览，再按资料组织介绍、参数表、优势、应用、案例/模拟效果、包装交付、认证、工厂能力、公司优势及六个采购 FAQ。推荐栏目不是虚构事实的理由；没有依据的认证/案例不展示，没有交期等信息时说明需确认。公司名及 OEM/ODM 能力仅在用户提供或当前来源可验证时使用，不推断属于目标公司。

页面主要 H1 总计只能有一个。详情版块标题始终使用加粗居中的 H2；产品页的唯一 H1 由外层产品标题提供，独立预览在详情容器外提供 H1。未知外层情况记为部署待验。产品详情包含六个采购 FAQ，顺序固定为：英文产品正文 → 固定公司简介 → Factory Photo → MiBA Logo Options → MiBA Accessory Options → 六个 FAQ。FAQ 是整份详情的最后一个内容版块。

完整产品详情（包含三个固定版块和最底部 FAQ）最大宽度 **1400px**，宽屏居中、窄屏宽度 100%，不能固定为 1400px。由 compose_content.py 添加统一外层容器。内层图文宽度不超过容器；图片 max-width:100%、height:auto，表格在自身容器内横向滚动，禁止 100vw、超宽 min-width 或绝对定位撑出容器。新增区采用 `.xb_import_v2` 命名空间，所有 CSS 选择器限定于此，移动端表格可横向滚动，图片提供 width/height 和响应式样式。只输出 HTML 片段，不引入 html/head/body、外部字体、全局 CSS、可执行 JavaScript 或 meta keywords。SEO 元数据填 CSV，不塞进详情 HTML。结构化数据属于站点集成，不能虚构评分/价格/库存。

将六个 FAQ 放入单独的 `<section class="xb_import_v2 miba_faq_section" style="padding:26px 0">` 容器，内部保留六个 `xb_faq_item`；该 FAQ 容器置于待拼接详情末尾，之后仅可有外层闭合标签。拼接器将其移至三个固定版块之后；FAQ 不得混在产品正文中。

将英文详情写入 `<file_name>.detail.html`，上传完成后通过 `scripts/compose_content.py` 追加三个固定图片版块，并把 FAQ 放到三个版块之后，生成最终 content。固定版块每个仅有一个 H2 标题和一张图片，不添加介绍、说明、按钮或额外内容。

### 4. 图片创作与处理

最新图片参考规则：Alibaba 原组图和原详情图是产品身份、功能和用途的参考，必须作为 imagegen 输入，但不是照搬画面设计的模板。锁定产品外形、比例、部件、材质、接口及设备接触关系；重新设计整体构图、主体位置与尺度、背景场景、道具、光线、配色和图文层级。不能仅改背景颜色、替换文字或轻微挪动元素；不复制原图的特殊光效、巨大数字背景、箭头组合及缩略图拼版。可保留有依据的产品观察角度，不能为降低相似度虚构未见部件。生成前分别记录 identity_locks 和 design_changes；验收分开判断产品准确性与画面独立性。用户所说“相似度80%”是对上一版过度相似的批评，不是目标比例；不编造量化相似度或承诺固定百分比。未证实宣传不照搬。

先读 [图片制作规则](references/image-workflow.md)。Alibaba 图库仅用作实物与事实参考。产品封面、产品组图、详情介绍图及应用图全部调用 imagegen 重新生成，不直接把来源文件作为生成结果；使用 imagegen 进行有针对性的参考图编辑，保留产品本体，同时对整体视觉设计作实质重构。每个商品生成 1 张独立 cover 和至少 4 张独立 gallery，即 CSV images 至少 5 张；不把封面、详情图、场景图或固定素材算入四张组图。组图应分别展示有依据的不同角度、结构、状态或颜色，不用同图改名或轻微变化凑数。三个用户指定图片是明确例外：直接使用提供的 PNG 转 WebP，不重新生成、改字、裁切或变更图片内容。

图的产品身份和功能重点参考对应 Alibaba 原图，整体画面与信息组织独立设计；产品结构、连接、比例及可核实标签保持准确。场景示意需要区分实拍时使用简短自然的图注，如 `Desk setup illustration.`；不能冒充真实客户案例或工厂现场。图片生成方法、供应商视频帧来源、手部比例核验等制作说明只写入内部记录，不放入商品详情。

取消 Lifeworth → Xinbada 的固定替换。用户指定目标品牌时用 imagegen 按其要求处理组图品牌，并检查其他标签文字和数字未变；未指定时新增图片采用无品牌设计，不擅自植入品牌，真实产品的形状、接口、部件数量、比例和可核实标签必须准确，不能为凑四张组图发明未观察到的背面结构或附件。逐张视觉核对后准备角色清单，运行 `scripts/prepare_images.py`：gallery/cover 为 800×800；scenario 宽度至少 1200；detail 按版面确定。WebP 从质量 82、method 6 开始压缩，保真优先；超体积记录理由并复核。

### 5. 上传与回填

使用每行 CSV 中的 IMGBB_API_KEY，调用随包上传脚本；不得改用命令行明文密钥。只有该行全部所需图片上传成功后才回填图片字段。上传会对网络/429/5xx 有界重试；仍失败则记录，禁止无限重试。保留部分成功清单，重新尝试前检查它，脚本自身不提供断点续传。

thumb 用产品封面；scenario_image 用新生成应用图。**CSV 的 images 仅写产品封面和产品组图**（cover/gallery），按新生成清单的展示顺序排列：封面第一，至少四张组图随后，逐行 `<url>|<English alt>`。详情介绍图、应用场景图、Factory Photo、MiBA Logo Options、MiBA Accessory Options 都不写入 images；详情图片仅放入 content，场景图还写入 scenario_image。不要为了满足旧校验而混入详情图。

`pro_fields` 按[专用字段规则](references/schema-and-workflow.md#pro_fields适配现有-php-输出)生成：4–8 条英文纯文本卖点，用真实换行分隔，第一条无前缀，第二条起每行行首添加一次 ``|`-+#$&*|``。该专用分隔符是允许的格式例外；卖点正文无 HTML、Markdown、编号和空行，不重复程序单独输出的 `$code`；每条建议 5–15 个单词，直接面向客户。程序负责换行显示，不在字段内插入 `<br>`。

所有图片仍要转换 WebP、上传 ImgBB 并在本地图片清单和上传清单中保留。只有 data.url 的 `https://i.ibb.co/...webp` 可回填。content 的图片链接从上传清单按 detail/scenario/supplied_static 角色读取，不要求出现在 CSV images。三个固定版块的标题、图片和顺序保持不变。

### 6. 校验与交付

按 [字段与交付规则](references/schema-and-workflow.md) 记录行状态和人工复核结果，运行：

```text
python scripts/validate_output.py input.csv input_completed.csv --images-dir images --report validation.json --review review.json
```

修复成功行的全部错误。对照来源覆盖清单查漏补缺，核对每个已访问且有价值的参数、说明和图片信息已合理使用；无法访问的区域如实列出，不宣称已完整采集。视觉复核英文详情、三个固定图片版块及最底部FAQ的组合在手机（如 390px）和宽桌面（如 1920px）下的效果，确认内容宽度不超过 1400px 且没有页面横向溢出，核对图片中的商品、标签、结构、模拟图说明以及事实来源。脚本不证明 SEO 收录、图片原创性或事实真实性。

交付完成版 CSV、本地 WebP、上传清单、证据记录及校验报告；报告成功/跳过/阻塞行数。存在跳过或阻塞时明确为部分完成。原 CSV 密钥列按原要求保留，因此含密钥的完成表仅交还用户，不用作公开示例。站点 canonical、301、站内链接、Sitemap、robots、hreflang、HTTP 图片可访问性及 CWV 等没有部署环境时列为待验，不能声称通过或擅自发布。
