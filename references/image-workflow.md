Current override: Read [Product identity and MiBA layout](identity-and-miba-layout.md) first. Its fidelity and primary layout rules take precedence over conflicting older guidance below.

# 图片：真实产品、原创详情、合理应用

## 区分用途

- 产品封面/组图：以来源实物图为参考，全部通过 imagegen 重新生成。每商品 1 张 cover + 至少 4 张 gallery，封面不计入四张组图；各张是独立成图，不是重复文件、仅换色或裁剪凑数。800×800、干净背景、完整主体，不拉伸、不裁掉关键产品。
- 新增详情介绍图：从产品真实外形出发，通过 imagegen 新创作。参考对应 Alibaba 图的产品身份、使用状态与功能信息；重新设计构图、场景、配色、主体位置及图文排版，不能做只换背景/文字的近似重绘。未经核实的宣传不照搬。
- 应用场景图：展示该产品有事实支持的合理应用；至少一张，用于 scenario_image 及相关新增详情小节；宽度至少 1200px。
- 末尾三个固定图片：按 [固定版块规则](fixed-blocks.md) 使用用户指定 PNG，角色 supplied_static，保留全部图像内容和原始比例，不用 imagegen 重做。

全部重新创作的图按实际用途标记 cover / gallery / detail / scenario，并记录 generated=true；仅三个 supplied_static 保持 generated=false；这只是来源记录，不代替人工核查。不伪造证书、客户工程或工厂现场，需要区分实拍时，场景图旁用简短自然的英文图注标识示意（如 Desk setup illustration）；制作方法、参考帧和保真核验只记入内部报告。只在标签明确可核实时保留数字，检查 imagegen 没有新增或误改文字。无法可靠保留结构时改用更简单场景重试，仍不可靠则阻塞，不能退回任何来源原图充数。

## 图像提示词骨架

```text
Create an original application visualization of the referenced [verified product].
Preserve its actual [shape/material/connections/package proportions] faithfully.
Show it in [supported application] with physically plausible installation or use.
Preserve the referenced product geometry, observed state and factual information purpose.
Create an independent composition, setting, palette and information hierarchy; do not copy the source visual template or merely replace its text/background.
Use only the user's explicitly supplied target brand; otherwise create an unbranded image.
Do not invent specifications, certifications,
customer projects, labels or performance evidence. [Target aspect ratio and dimensions].
```

## image-plan.json

source 相对于清单文件解析，文件名用描述性英文；name 不含扩展名。每行商品有独立清单，清单顺序即展示顺序。下面是角色片段示例，完整清单还必须增加至少四条 gallery，且全部 generated=true。

生成前写 image_plan：每张的角色、参考图、核实结构、独立视角/状态、信息目的和提示词。建议封面为清晰三分之四视角；四张组图从正面、已观察到的侧后视、结构连接、真实展开/收合状态或其他已核实配置中选择。无足够结构依据时采用已知视角的新构图，不能猜接口、尺寸、配件或变体。详情用另一套有说明价值的图文组合，不把同一文件同时用于组图和详情。记录实际 imagegen 输出路径及生成提示词；generated=true 不能替代真实调用和逐张视觉复核。

```json
{
  "images": [
    {"source": "staging/cover.png", "name": "product-white-background", "role": "cover", "generated": true},
    {"source": "staging/application.png", "name": "product-application-concept", "role": "scenario", "generated": true, "width": 1200},
    {"source": "staging/detail.png", "name": "product-detail-concept", "role": "detail", "generated": true, "width": 1000}
  ]
}
```

prepare_images.py 用 Pillow 进行尺寸/格式/压缩处理，不代替 imagegen 创作。输出目录仅存 WebP，处理记录写在目录旁的 `<folder>.image-manifest.json`。从质量 82 / method 6 开始，cover/gallery/detail 尝试降至质量 70 以接近 100 KB；不牺牲清晰度强制达到体积目标。超过 100 KB 由人工复核并记录接受理由；画质不足时用 --min-quality 82 重做。场景图清晰优先，不强制 100 KB。多帧图不静默丢帧，要求先选择合适静态图。

上传成功后，将每张本地图片与 Direct URL、角色、尺寸、alt 对照复核；重要图片 alt 唯一且与实际内容一致。首屏主图 loading=eager，其余按位置使用 lazy；新增图片必须带 width/height 防止布局跳动。站点级响应式图片派生/srcset 需求写入部署验收，不能伪造不同尺寸的 URL。

## CSV 组图与详情图分离

- cover/gallery：写入 CSV images；cover 同时用于 thumb。
- detail：仅用于 content，不写 images。
- scenario：用于 scenario_image 和 content，不写 images。
- supplied_static：仅用于 content 三个固定版块，不写 images。

所有角色均保留在本地 image-manifest 和上传清单，不能因为不写 images 就不上传详情图。同一详情图 URL 不得再以 cover/gallery 角色混入产品组图。1400px 是 HTML 显示容器的最大宽度，不是要求将所有原始图片强制缩至 1400px；固定素材仍按固定版块规则保留尺寸和可读性。
