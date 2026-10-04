# Gallery design notes

The gallery separates complete website styles from reusable backgrounds. Each has a stable ID, a short description, a real preview, and a copyable selection. All previews use the same placeholder profile so differences come from layout rather than content.

The organization draws on the locally installed video-shotcraft library: its searchable card index, named variants, reference implementations, and recipe parameters. This is a website adaptation, not a video production workflow. No Remotion code, audio, or sample videos are included.

Visual directions considered from its cards:

| Reference vocabulary | Website adaptation |
| --- | --- |
| brand-ink-open, paper-title-card | Paper & Ink: paper surface, serif hierarchy, quiet accents |
| panel-grid-moves | Swiss Grid / Research Blueprint: clear divisions and alignment |
| terminal-3d | Terminal Notes: monospace labels and a dark document surface |
| spotlight-sweep-moves | Studio Folio: restrained background illumination, continuously readable content |
| glass-pill-dictation-typing | Aurora Glass: translucent surfaces and soft background color |

The source library's exact animation recipes are not reproduced. For reading-focused websites, avoid delayed text reveals, dramatic camera moves, sound, and effects that hide content. Paper dust, breathing dots, grid scans and drifting leaves give those materials restrained movement without moving text. Bauhaus adds primary-color geometry; Sketchbook uses irregular ink borders, a taped portrait and pencil doodles. All new motion pauses when the page is hidden and respects reduced-motion preferences.

## Implementation sources

- particles.js 2.0.0: vendored MIT implementation, with the retained original parameter preset.
- Other effects: original CSS, SVG and Canvas implementations, distributed under CC0.
- MDN: gradient, SVG and Canvas implementation references linked per effect in `designs.json`.
- Additional discovery links: tsParticles, Vanta, css-doodle and Codrops Ambient Canvas. These are linked references, not copied dependencies.

`scripts/build_demo.py` emits the overview, ten complete style pages, a library overview, twelve full material pages and twelve thumbnail documents. It also builds a deterministic, standalone material ZIP. The packaged skill uses the same template/assets and catalog as the previews.
