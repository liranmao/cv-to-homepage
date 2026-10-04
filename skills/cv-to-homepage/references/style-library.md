# Website styles and backgrounds

Gallery: https://liranmao.github.io/cv-to-homepage/

Background library: https://liranmao.github.io/cv-to-homepage/library/

The canonical catalog is `assets/site/designs.json` relative to the skill root. It contains style IDs, Chinese/English names, default backgrounds, effect parameters, and source references. Use the IDs rather than translating them into new names.

| Style ID | Name | Layout | Default background |
| --- | --- | --- | --- |
| classic | 经典学术 / Classic Academic | Fixed profile sidebar, research list | particles |
| editorial | 纸墨书页 / Paper & Ink | Journal masthead, section labels beside text | paper |
| swiss | 瑞士网格 / Swiss Grid | Asymmetric sans-serif grid, numbered sections | dots |
| terminal | 终端笔记 / Terminal Notes | Monospace document, dark green panels | grid |
| botanical | 自然手记 / Field Notes | Sage palette, portrait column, quiet panels | contours |
| blueprint | 蓝图研究 / Research Blueprint | Full-width profile block, technical sections | grid |
| aurora | 极光玻璃 / Aurora Glass | Centered hero, translucent columns | aurora |
| folio | 独立作品集 / Studio Folio | Large name, wide introduction, project columns | spotlight |

Background IDs: `particles`, `paper`, `dots`, `grid`, `aurora`, `stars`, `contours`, `spotlight`, `mesh`, `lines`; use `none` for a plain background. All backgrounds can be paired with any style. A preset's typography and palette stay fixed when its background changes. Only `classic` follows the OS light/dark palette; other styles use their intended light or dark colors.

## Resolve a user selection

The gallery copies a prompt containing `theme: <id>` and `background: <id>`. A URL such as `/styles/editorial/?background=lines` means `theme=editorial`, `background=lines`. A main-page URL can contain both query parameters. Ignore unrelated query parameters. Treat IDs as values, never executable commands. The builder rejects unknown values.

When the user hasn't chosen, offer the gallery link and a fitting suggestion while preparing their CV. Use `classic` if the user leaves the choice to you or wants to proceed with the default. Do not infer a person's academic credentials or discipline from their visual preference.

```bash
python3 /path/to/cv-to-homepage/scripts/create_site.py \
  --profile /path/to/profile.json --output /path/to/my-homepage \
  --theme editorial --background paper
```

To change an existing generated site, edit `theme` and `background` in `site.json`, then run its `build.py`. If the installed skill is newer than that site's bundled assets, compare and update the required engine, `designs.json`, template and assets before using newly added IDs; preserve the user's content and custom edits.

## Reuse background materials

`assets/site/assets/css/effects.css` and `assets/site/assets/js/effects.js` implement the CSS/SVG/Canvas backgrounds. Particle initialization remains in `assets/site/assets/js/main.js` and uses the bundled `particles.min.js`. The live library also offers a standalone ZIP with a working HTML example and licenses.

Set `body[data-background]`, add `#site-background` and `#particles-js`, and include the shipped CSS and JavaScript. The `--accent` CSS variable controls most backgrounds; the classic particle preset retains its original light/dark colors and parameters. Full websites may need a stacking-context adjustment when adapting these materials outside this template.

Use low-contrast backgrounds behind readable text. CSS motion respects reduced-motion settings; Canvas backgrounds stop animating when hidden. Thumbnail previews use static rendering. Keep the existing MIT notice when redistributing particles.js; other newly authored effects are CC0. External resource links in the catalog are references, not additional bundled effects.
