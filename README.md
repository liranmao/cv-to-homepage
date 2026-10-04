# CV → 个人网站

中文 | [English](README.en.md)

把简历交给 Codex 或 Claude，生成个人网站并部署到 GitHub Pages。本科生可以放课程项目和实习经历，硕博可以放研究方向和论文。

[预览网站](https://liranmao.github.io/cv-to-homepage/) · [下载 Skill](https://github.com/liranmao/cv-to-homepage/releases/latest/download/cv-to-homepage.zip)

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
  --profile examples/undergraduate.json --output ../my-homepage
python3 -m http.server 8000 --bind 127.0.0.1 --directory ../my-homepage/docs
```

打开 `http://127.0.0.1:8000` 查看页面。三个示例分别是 `undergraduate.json`、`masters-zh.json` 和 `phd.json`，在 `examples/` 中。把占位符换成自己的信息即可。

手动部署时，将 `USERNAME/REPO` 换成自己的用户名和新仓库名：

```bash
python3 skills/cv-to-homepage/scripts/deploy.py \
  --site ../my-homepage --repo USERNAME/REPO --publish
```

网站发布目录为 `main` 分支的 `/docs`。部署中断时，可以按[部署说明](skills/cv-to-homepage/references/deployment.md)继续完成。

## 开发

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_demo.py
python3 scripts/package.py
```

Skill 文件在 `skills/cv-to-homepage/`，打包文件为 `dist/cv-to-homepage.zip`。
