# CV → 个人学术网站

**给 Codex 或 Claude 一份简历，用 AI 建立并部署自己的个人网站。**

适合本科生、硕士生和博士生。沿用 [Liran Mao 个人网站](https://liranmao.github.io/)的 Minimal Light 布局：深蓝导航、左侧个人信息、右侧学术内容、论文缩略图、暗色模式和粒子背景。没有论文也能用：展示教育、项目、实习和技能即可。

**[查看演示网站](https://liranmao.github.io/cv-to-homepage/)** · **[下载 Skill ZIP](https://github.com/liranmao/cv-to-homepage/releases/latest/download/cv-to-homepage.zip)**

这是独立的新仓库。不会修改或部署到原作者的网站。演示资料全部虚构。

## 1. 安装 Skill

最省事的方式：把这段话发给 **Codex 或 Claude Code**：

> 请从 https://github.com/liranmao/cv-to-homepage 安装 skills/cv-to-homepage。根据我当前使用的工具，安装到 Codex 的 ~/.agents/skills/ 或 Claude Code 的 ~/.claude/skills/。不要修改任何现有网站。

也可以在终端执行（需要 Git 和 Python 3.9+）：

```bash
git clone https://github.com/liranmao/cv-to-homepage.git
cd cv-to-homepage
python3 scripts/install.py --agent codex
```

Claude Code 用户把最后一行改为：

```bash
python3 scripts/install.py --agent claude
```

同时安装：`python3 scripts/install.py --agent both`。更新：先 `git pull`，再执行安装命令并加 `--update`。安装后重新打开会话，或刷新技能列表。

**Claude 网页版 / Cowork：** 从上面的链接下载 ZIP，在支持自定义技能的界面上传。它可以帮助整理内容和生成网站文件；自动 GitHub 部署需要运行环境具有 Git、GitHub CLI、网络和账号授权。要完整演示“生成 → 部署”，建议使用本机 Codex 或 Claude Code。

## 2. 放入简历，发送这段话

在 Codex 中：

```text
使用 $cv-to-homepage，根据我附上的 CV 建立个人学术网站。
保留模板样式，只使用简历中真实的信息，没有的栏目直接隐藏。
请创建一个全新的公开 GitHub 仓库，并部署到 GitHub Pages。
不要覆盖我已有的网站，不要上传完整 CV 文件、家庭住址或电话号码。
完成后给我网站链接。
```

在 Claude Code 中，把 `$cv-to-homepage` 换成 `/cv-to-homepage`；也可以直接说“根据我的 CV，使用 cv-to-homepage 建站并部署”。

可提供 PDF、DOCX 或纯文本 CV；照片可选。扫描版 PDF 需要工具支持 OCR，无法读取时会请你提供可读文本。想提供可下载简历时，另行明确：“请公开这份已删去私人信息的 PDF 简历。”

## 3. 账号准备好后，以 15 分钟为目标

| 时间安排 | 你要做什么 | AI 会做什么 |
| --- | --- | --- |
| 0–3 分钟 | 打开工具、安装技能、提供 CV | 读取简历，整理公开信息 |
| 3–8 分钟 | 核对姓名、经历、论文状态 | 生成页面，隐藏缺失栏目 |
| 8–12 分钟 | 首次使用时登录 GitHub | 预览，创建全新仓库，推送网站 |
| 12–15 分钟 | 打开网站，复制链接 | 等待 Pages 构建，验证线上页面 |

这是操作目标，不是保证。首次安装工具、账号验证和 GitHub 构建排队可能需要更久。需要 GitHub 账号；[GitHub Pages 支持在免费套餐的公开仓库上使用](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site)。模型本身按你已有的 Codex / Claude 服务使用，不需要额外购买 API。

默认网址为 `https://你的用户名.github.io/`。如果对应仓库已存在，就使用全新项目仓库，网址为 `https://你的用户名.github.io/仓库名/`。**脚本不会覆盖已有仓库。公开仓库中的网页和已提交源文件都可以被他人查看。**

## 不用 AI，先试跑模板

```bash
python3 skills/cv-to-homepage/scripts/create_site.py \
  --profile examples/undergraduate.json --output ../my-homepage
python3 -m http.server 8000 --bind 127.0.0.1 --directory ../my-homepage/docs
```

打开 `http://127.0.0.1:8000`。还可以试 `examples/masters-zh.json` 或 `examples/phd.json`。这些文件仅供演示，不要当作自己的经历发布。

生成器只使用 Python 标准库，无需 npm、Ruby 或 Jekyll。CV 的理解由 AI 完成，生成器接收的是整理后的 JSON，不会自动解析原始简历。主字体使用 Google Fonts；不可访问时会回退到系统字体。

修改生成目录的 `site.json` 后运行 `python3 build.py`，重新预览。要更新线上页面，提交实际改动及重建的 `docs/`，再推送；也可以继续让 AI 帮你更新。[字段说明](skills/cv-to-homepage/references/profile-schema.md)。

## 部署命令

先运行 `gh auth login` 登录自己的 GitHub 账号，并配置 Git 提交姓名和邮箱。以下示例中的 `USERNAME` 和仓库名需要替换：

```bash
# 查看部署目标，不发布
python3 skills/cv-to-homepage/scripts/deploy.py \
  --site ../my-homepage --repo USERNAME/my-academic-homepage

# 创建全新公开仓库并部署
python3 skills/cv-to-homepage/scripts/deploy.py \
  --site ../my-homepage --repo USERNAME/my-academic-homepage --publish
```

脚本发布 `main` 分支的 `/docs`，并验证网页是否可访问。需要 GitHub CLI 的仓库创建、Pages 设置权限。账号/权限不足时会明确停止；已创建但未完成的部署见[恢复说明](skills/cv-to-homepage/references/deployment.md)，不要重复创建或强制推送。

## English quick start

Install with `python3 scripts/install.py --agent codex`, `--agent claude`, or `--agent both`. Attach your CV and ask:

> Use cv-to-homepage to create my academic homepage from this CV and deploy it to a new public GitHub Pages repository. Keep the template design, omit missing sections, and do not publish my raw CV or private contact details.

The shared skill supports Codex and Claude Code. It preserves the source site's visual design while replacing Jekyll with a small, dependency-free Python renderer. No papers or portrait are required. Content is grounded in your CV; a new repository is created only when deployment is requested. The original author's repository is protected. Claude custom-skill ZIP installation is also provided, but automatic deployment depends on shell, network, and GitHub access in that environment.

## Development & provenance

```bash
python3 -m unittest discover -s tests -v
python3 scripts/package.py
```

The distributable is `dist/cv-to-homepage.zip`. The skill is self-contained in `skills/cv-to-homepage/`. Installer paths follow [official Codex documentation](https://developers.openai.com/codex/skills/) and [official Claude Code documentation](https://code.claude.com/docs/en/skills).

See [ATTRIBUTION.md](ATTRIBUTION.md) for the pinned source revision and design changes. CC0 license retained from the original template; users' CVs and images retain their own rights.
