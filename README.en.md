# CV → Personal website

[中文](README.md) | English

Give Codex or Claude your CV to build a personal website and deploy it to GitHub Pages. Undergraduates can include coursework projects and internships; graduate students can add research interests and publications.

[Choose a website style](https://liranmao.github.io/cv-to-homepage/) · [Background library](https://liranmao.github.io/cv-to-homepage/library/) · [Download the skill](https://github.com/liranmao/cv-to-homepage/releases/latest/download/cv-to-homepage.zip)

## Choose a style

Open the [style gallery](https://liranmao.github.io/cv-to-homepage/) to explore eight complete pages: Classic Academic, Paper & Ink, Swiss Grid, Terminal Notes, Field Notes, Research Blueprint, Aurora Glass, and Studio Folio.

Use the control at the top of each page to switch backgrounds. Once you have chosen a style and background, click “Copy build prompt” and send it to the AI with your CV. You can start with [Classic Academic](https://liranmao.github.io/cv-to-homepage/styles/classic/).

The [background library](https://liranmao.github.io/cv-to-homepage/library/) includes particles, paper grain, dots, grids, aurora, stars, contours, a spotlight, a color mesh, and flowing lines, with full previews, parameters, and a [source download](https://liranmao.github.io/cv-to-homepage/downloads/background-library.zip).

## Install

Send this to Codex or Claude Code:

> Install skills/cv-to-homepage from https://github.com/liranmao/cv-to-homepage. Use ~/.agents/skills/ for Codex or ~/.claude/skills/ for Claude Code.

You can also install it in your terminal:

```bash
git clone https://github.com/liranmao/cv-to-homepage.git
cd cv-to-homepage
python3 scripts/install.py --agent codex
```

For Claude Code, change `codex` in the last line to `claude`. Use `both` to install for both tools. Start a new session after installation.

For Claude on the web or Cowork, download the ZIP above and upload it through the custom skills interface. Use local Codex or Claude Code to have the AI complete GitHub deployment directly.

## Give it your CV

Upload a PDF, Word document, or plain-text CV, then send:

```text
Use $cv-to-homepage to build my personal website from my CV.
Keep the template style, fill it with my CV content, and hide missing sections.
Create a new public GitHub repository, deploy to GitHub Pages, and give me the URL when it is ready.
```

In Claude Code, replace `$cv-to-homepage` with `/cv-to-homepage`.

You can upload a photo too. To offer a downloadable CV on your website, attach a PDF you want to make public and tell the AI: “Add this PDF to the website's CV link.”

## Publish your website

Have a GitHub account ready and install Python 3.9+, Git, and [GitHub CLI](https://cli.github.com/) on your computer. The first time, run `gh auth login` and configure your Git commit name and email. The AI will build, preview, and deploy the website; you review the page content.

Your website address is `https://USERNAME.github.io/`. If you already have that site, the new one will use `https://USERNAME.github.io/REPO/`. Add the link to your CV, email signature, or social profile to share it.

## Update your content

Continue in Codex or Claude Code:

> Add this new experience to my website, preview it, and update GitHub Pages.

You can also edit `site.json` in your website directory, run `python3 build.py`, then commit and push the changes. [See the field reference](skills/cv-to-homepage/references/profile-schema.md).

To update the skill, run `git pull` in this repository, then rerun the install command with `--update`.

## Try it manually

Run these commands from this repository:

```bash
python3 skills/cv-to-homepage/scripts/create_site.py \
  --profile examples/undergraduate.json --output ../my-homepage \
  --theme editorial --background paper
python3 -m http.server 8000 --bind 127.0.0.1 --directory ../my-homepage/docs
```

Open `http://127.0.0.1:8000` to see the page. The three examples are `undergraduate.json`, `masters-zh.json`, and `phd.json`, all in `examples/`. Replace the placeholders with your own information. Use `--theme` to choose a style and `--background` to choose a background; omitting them uses Classic Academic.

To deploy manually, replace `USERNAME/REPO` with your username and a new repository name:

```bash
python3 skills/cv-to-homepage/scripts/deploy.py \
  --site ../my-homepage --repo USERNAME/REPO --publish
```

The website is published from `/docs` on the `main` branch. If deployment is interrupted, follow the [deployment guide](skills/cv-to-homepage/references/deployment.md) to finish it.

## Development

```bash
python3 -m unittest discover -s tests -v
python3 scripts/build_demo.py
python3 scripts/package.py
```

The skill files are in `skills/cv-to-homepage/`. The packaged file is `dist/cv-to-homepage.zip`.
