# A skill to turn your CV into a personal homepage in 15 minutes

[中文](README.md) | English

**cv-to-homepage is a skill for Codex and Claude** that turns your CV into a publicly accessible personal homepage and deploys it to GitHub Pages in about 15 minutes.

The skill includes **10 website styles and 12 background effects**. Mix and match layouts and backgrounds, or let the AI pick a random combination to create a homepage you like.

[Choose a website style](https://liranmao.github.io/cv-to-homepage/) · [Background library](https://liranmao.github.io/cv-to-homepage/library/) · [Download the skill](https://github.com/liranmao/cv-to-homepage/releases/latest/download/cv-to-homepage.zip)

## Quick Start

Upload your CV (PDF, Word, or plain text), then send this prompt to Codex or Claude Code:

```text
Install skills/cv-to-homepage from https://github.com/liranmao/cv-to-homepage.
For Codex, install it in ~/.agents/skills/; for Claude Code, use ~/.claude/skills/.
Use $cv-to-homepage to build my personal website from my CV.
Choose Classic Academic (theme: classic) and Particle Network (background: particles).
Fill in the content from my CV, create a new public GitHub repository, and deploy it to GitHub Pages.
```

In Claude Code, replace `$cv-to-homepage` with `/cv-to-homepage`. To try a different combination, choose one in the [style gallery](https://liranmao.github.io/cv-to-homepage/) and replace the style and background in the prompt, or change that line to: “Please randomly choose and combine a website style and background.”

## Choose a style

Open the [style gallery](https://liranmao.github.io/cv-to-homepage/) to explore ten complete pages: Classic Academic, Paper & Ink, Swiss Grid, Terminal Notes, Field Notes, Research Blueprint, Aurora Glass, Studio Folio, Bauhaus Studio, and Sketchbook.

Use the control at the top of each page to switch backgrounds. Once you have chosen a style and background, click “Copy build prompt” and send it to the AI with your CV. You can start with [Classic Academic](https://liranmao.github.io/cv-to-homepage/styles/classic/).

The [background library](https://liranmao.github.io/cv-to-homepage/library/) includes particles, paper grain, dots, grids, aurora, stars, contours, a spotlight, a color mesh, flowing lines, geometric shapes, and pencil doodles, with full previews, parameters, and a [source download](https://liranmao.github.io/cv-to-homepage/downloads/background-library.zip).

Each style has subtle motion: paper dust, breathing dots, grid scans, floating leaves, aurora glimmers, soft rings, turning shapes, or drawing doodles. Text stays still. When the system’s reduced-motion setting is enabled, backgrounds remain static.

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

## Contribute a template

Contributions of your own website templates are welcome, along with background effects and improvements to existing styles. Submit a [Pull Request](https://github.com/liranmao/cv-to-homepage/pulls), or share an idea in [Issues](https://github.com/liranmao/cv-to-homepage/issues) first. Include a preview link or screenshot, the template source, a short description of the style, and asset sources and licenses so others can preview and reuse your work.

## Acknowledgements

Thanks to the following projects and resources:

- [Minimal Light — Yaoyao Liu](https://github.com/yaoyao-liu/minimal-light): the base theme for Classic Academic.
- [pages-themes/minimal](https://github.com/pages-themes/minimal), [orderedlist/minimal](https://github.com/orderedlist/minimal), and [al-folio](https://github.com/alshedivat/al-folio): upstream themes and design sources credited by Minimal Light.
- [particles.js — Vincent Garreau](https://github.com/VincentGarreau/particles.js): the animation library used for the particle network background.
- [video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft): a reference for the gallery's card catalog, material recipes, and some visual directions.
- [MDN Web Docs](https://developer.mozilla.org/): technical references for CSS gradients, SVG, and Canvas backgrounds.
- [tsParticles](https://github.com/tsparticles/tsparticles), [Vanta.js](https://github.com/tengbao/vanta), [css-doodle](https://css-doodle.com/), and [Codrops Ambient Canvas](https://tympanus.net/Development/AmbientCanvasBackgrounds/): additional tools and motion inspiration linked in the material library.

See [ATTRIBUTION.md](ATTRIBUTION.md) for detailed sources and [THIRD_PARTY_LICENSES.txt](THIRD_PARTY_LICENSES.txt) for third-party licenses.
