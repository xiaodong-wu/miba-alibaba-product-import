# Miba Alibaba Product Import V2

用于 Codex 的 Alibaba 商品导入技能：从商品链接完整提取可核实资料，生成模块化英文详情、产品封面、组图与应用场景图，转换 WebP、上传 ImgBB，并回填及校验 CSV。

## 功能

- 保留输入 CSV 的原字段、未知列与行顺序。
- 独立编写英文标题、SEO 元数据、产品详情及六个采购 FAQ。
- 使用 imagegen 重新生成 1 张封面、至少 4 张独立组图及详情/应用图，保留真实产品身份并重新设计画面，按规则处理尺寸和 WebP 压缩。
- 详情顺序固定为：英文产品正文 → 随包公司简介 → Factory Photo → MiBA Logo Options → MiBA Accessory Options → 六个 FAQ。
- 详情最大宽度 1400px，各版块左右外层 padding 为 0，版块标题使用加粗居中的 H2，兼顾移动端阅读。
- `pro_fields` 在同一 CSV 单元格内保留 4–8 条真实换行属性，从第二行开始以 ``|`-+#$&*|`` 为行首分隔符。
- 附带图片处理、上传、HTML 拼接、输出校验脚本及测试。

技能名称不代表商品必须使用 Miba 品牌；目标品牌以用户提供的信息为准。随包固定公司简介保留 MiBA 文案，属于固定版块例外，不自动套用到商品参数或 SEO 中。

## 安装

将此仓库完整克隆到 Codex 的个人技能目录。Windows PowerShell 示例（目标目录应不存在）：

```powershell
$skillRoot = Join-Path $env:USERPROFILE '.codex/skills'
git clone https://github.com/xiaodong-wu/miba-alibaba-product-import.git (Join-Path $skillRoot 'miba-alibaba-product-import-v2')
```

如自定义了 CODEX_HOME，请将技能放到对应的 skills 目录。也可以下载仓库 ZIP，解压后将包含 SKILL.md 的目录命名为 miba-alibaba-product-import-v2，放入个人技能目录。

运行辅助脚本需要 Python 3.10+ 和 Pillow。在仓库根目录安装依赖：

```text
python -m pip install -r requirements.txt
```

执行完整流程还需要可用的网页浏览能力、imagegen 图像生成能力，以及用户自己的 ImgBB API Key。脚本本身不提供网页事实提取或 AI 图像生成。

## 使用

从 assets/content_import_template.csv 复制空白表头到任务目录，为每条商品填写 link 与 IMGBB_API_KEY，然后在 Codex 中请求：

```text
使用 $miba-alibaba-product-import-v2 处理这个 Alibaba 商品 CSV，生成英文详情、封面、至少四张组图及应用场景图，按规则插入固定公司简介和三个固定图片版块，并将六个 FAQ 放在最底部。
```

可同时提供目标品牌、公司资料和最新产品优化规范；没有品牌信息时生成中性文案。

执行规则见 [SKILL.md](SKILL.md)，命令及交付格式见 [字段与交付规则](references/schema-and-workflow.md)。随包 [产品优化规范](references/google-product-seo-requirements.md) 是用户提供文档的快照，并非自动更新的 Google 官方规则。

## 随包图片

以下三张 PNG 保留原始内容，执行导入时仅按规则转换和压缩为 WebP：

- [Factory Photo](assets/fixed-blocks/Factory%20Photo.png)
- [MiBA Logo Options](assets/fixed-blocks/MiBA%20Logo%20Options.png)
- [MiBA Accessory Options](assets/fixed-blocks/MiBA%20Accessory%20Options.png)

路径和顺序详见 [固定图片版块规则](references/fixed-blocks.md)。这些素材中的品牌不应被自动套用到其他商品。

## 密钥与任务数据

IMGBB_API_KEY 仅由上传脚本从用户的本地 CSV 读取。输入和完成版 CSV 都可能含密钥，不应提交到 GitHub；仓库仅包含空白字段模板。默认忽略 CSV、环境文件、Python 缓存及常见任务输出目录。

## 测试

在仓库根目录运行现有本地测试：

```text
python -m unittest discover -s scripts -p test_workflow.py -v
```

本地测试不代表实时 Alibaba 访问、AI 图像质量或实际 ImgBB 上传已经通过；完整任务仍需事实核查、视觉复核和输出校验。

## 来源与许可

保留原有 [MIT LICENSE](LICENSE)。上传辅助脚本来源及改动说明见 [字段与交付规则](references/schema-and-workflow.md#源码来源)。
