# 15分钟从简历生成个人主页skill

中文 | [English](README.en.md)

**cv-to-homepage 是一个供 Codex 和 Claude 使用的 Skill**，帮你在约 15 分钟内，把简历变成可公开访问的个人主页，并部署到 GitHub Pages。

Skill 内置 **10 种网站风格和 12 种背景素材**。排版与背景可以自由搭配，也可以让 AI 随机组合，生成你喜欢的主页。

[选择网站风格](https://liranmao.github.io/cv-to-homepage/) · [背景素材库](https://liranmao.github.io/cv-to-homepage/library/) · [下载 Skill](https://github.com/liranmao/cv-to-homepage/releases/latest/download/cv-to-homepage.zip)

## Quick Start / 快速开始

上传你的简历（PDF、Word 或纯文本），然后把下面这段话发给 Codex 或 Claude Code：

```text
请从 https://github.com/liranmao/cv-to-homepage 安装 skills/cv-to-homepage。
Codex 安装到 ~/.agents/skills/，Claude Code 安装到 ~/.claude/skills/。
使用 $cv-to-homepage，根据我的简历建立个人网站。
风格选择「经典学术」（theme: classic），背景选择「粒子连线」（background: particles）。
按简历填写内容，创建新的公开 GitHub 仓库并部署到 GitHub Pages。
```

Claude Code 中用 `/cv-to-homepage` 替换 `$cv-to-homepage`。想换一种搭配，可以在[风格总览](https://liranmao.github.io/cv-to-homepage/)中选好后替换风格和背景，或把选择那一行改成：“请随机选择并组合一种网站风格和背景。”

## 选择风格

打开[风格总览](https://liranmao.github.io/cv-to-homepage/)，查看 10 种完整页面：经典学术、纸墨书页、瑞士网格、终端笔记、自然手记、蓝图研究、极光玻璃、独立作品集、包豪斯和手绘笔记。

每个页面顶部都能切换背景。选好“风格＋背景”后，点击“复制建站指令”，和简历一起发给 AI。可以先从[经典学术](https://liranmao.github.io/cv-to-homepage/styles/classic/)开始看。

[素材库](https://liranmao.github.io/cv-to-homepage/library/)收录了粒子、纸感、点阵、网格、极光、星野、等高线、聚光、柔彩渐变、流线、几何游乐和铅笔涂鸦，附完整预览、参数与[源码下载](https://liranmao.github.io/cv-to-homepage/downloads/background-library.zip)。

各风格配有轻量动效：纸页浮尘、点阵呼吸、网格扫描、叶形漂浮、极光微闪、柔光圆环、几何转动和涂鸦描画。文字保持稳定；开启系统“减少动态效果”后，背景以静态方式显示。

## 安装

把下面这段话发给 Codex 或 Claude Code：

> 请从 https://github.com/liranmao/cv-to-homepage 安装 skills/cv-to-homepage。Codex 安装到 ~/.agents/skills/，Claude Code 安装到 ~/.claude/skills/。

也可以在终端安装：

```bash
git clone https://github.com/liranmao/cv-to-homepage.git
cd cv-to-homepage
python3 scripts/install.py --agent codex
```

Claude Code 用户将最后一行的 `codex` 改成 `claude`。两边都安装就用 `both`。安装后重新打开会话。

Claude 网页版或 Cowork 用户可以下载上面的 ZIP，在自定义技能界面上传。要让 AI 直接完成 GitHub 部署，使用本机 Codex 或 Claude Code。

## 给它一份简历

上传 PDF、Word 或纯文本简历，发送：

```text
使用 $cv-to-homepage，根据我的简历建立个人网站。
保留模板样式，按简历内容填写，缺少的栏目隐藏。
创建一个新的公开 GitHub 仓库，部署到 GitHub Pages，完成后给我网址。
```

Claude Code 中用 `/cv-to-homepage` 替换 `$cv-to-homepage`。

照片可以一起上传。想在网站上放可下载的简历，就再附上一份适合公开的 PDF，并告诉 AI：“把这份 PDF 放到网站的 CV 链接里。”

## 发布网站

发布前，Skill 会询问你想用的网站名，并列出对应的公开 GitHub 仓库和完整网址，等你确认后再发布。例如，仓库名 `my-homepage` 对应 `https://USERNAME.github.io/my-homepage/`。这里的网站名用于网址，不会替换页面上的姓名。

准备一个 GitHub 账号，在电脑上安装 Python 3.9+、Git 和 [GitHub CLI](https://cli.github.com/)。首次使用时运行 `gh auth login` 登录，并设置 Git 提交用的姓名和邮箱。AI 会完成建站、预览和部署，你核对页面内容即可。

网站地址是 `https://USERNAME.github.io/`。如果你已经有这个站点，新网站会使用 `https://USERNAME.github.io/REPO/`。把链接放进简历、邮件签名或社交账号，就可以分享了。

## 更新内容

继续在 Codex 或 Claude Code 中说：

> 把这段新经历加到我的网站里，预览后更新到 GitHub Pages。

也可以编辑网站目录中的 `site.json`，运行 `python3 build.py`，然后提交并推送改动。[查看字段说明](skills/cv-to-homepage/references/profile-schema.md)。

更新 Skill：在本仓库运行 `git pull`，再运行安装命令并加上 `--update`。

## 手动试跑

在本仓库目录运行：

```bash
python3 skills/cv-to-homepage/scripts/create_site.py \
  --profile examples/undergraduate.json --output ../my-homepage \
  --theme editorial --background paper
python3 -m http.server 8000 --bind 127.0.0.1 --directory ../my-homepage/docs
```

打开 `http://127.0.0.1:8000` 查看页面。三个示例分别是 `undergraduate.json`、`masters-zh.json` 和 `phd.json`，在 `examples/` 中。把占位符换成自己的信息即可。`--theme` 选择风格，`--background` 选择背景；不填写时使用经典学术风格。

手动部署时，将 `USERNAME/REPO` 换成自己的用户名和新仓库名：

```bash
python3 skills/cv-to-homepage/scripts/deploy.py \
  --site ../my-homepage --repo USERNAME/REPO --publish
```

网站发布目录为 `main` 分支的 `/docs`。部署中断时，可以按[部署说明](skills/cv-to-homepage/references/deployment.md)继续完成。

## 贡献网页模版

欢迎贡献你自己的网页模版，也欢迎分享背景效果、改进现有风格。可以直接提交 [Pull Request](https://github.com/liranmao/cv-to-homepage/pulls)，或先在 [Issues](https://github.com/liranmao/cv-to-homepage/issues) 里交流想法。提交时附上预览链接或截图、模版源码、简短的风格介绍，以及素材来源和许可，方便大家预览和复用。

## Acknowledgements / 致谢

感谢以下项目和资源：

- [Minimal Light — Yaoyao Liu](https://github.com/yaoyao-liu/minimal-light)：经典学术风格的基础主题。
- [pages-themes/minimal](https://github.com/pages-themes/minimal)、[orderedlist/minimal](https://github.com/orderedlist/minimal) 和 [al-folio](https://github.com/alshedivat/al-folio)：Minimal Light 致谢的上游主题与设计来源。
- [particles.js — Vincent Garreau](https://github.com/VincentGarreau/particles.js)：粒子连线背景使用的动画库。
- [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)：为图库的卡片目录、素材配方和部分视觉方向提供了参考。
- [MDN Web Docs](https://developer.mozilla.org/)：CSS 渐变、SVG 与 Canvas 背景实现的技术参考。
- [tsParticles](https://github.com/tsparticles/tsparticles)、[Vanta.js](https://github.com/tengbao/vanta)、[css-doodle](https://css-doodle.com/) 和 [Codrops Ambient Canvas](https://tympanus.net/Development/AmbientCanvasBackgrounds/)：素材库收录的扩展工具与动效灵感来源。

详细来源见 [ATTRIBUTION.md](ATTRIBUTION.md)，第三方许可见 [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt)。
