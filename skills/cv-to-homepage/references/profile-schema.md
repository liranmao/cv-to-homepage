# Public profile schema

The agent extracts and reviews the CV, then writes JSON. `name` is the only required field. Omit unavailable fields; empty arrays are hidden. Unknown keys fail validation so accidentally copied private CV fields are noticed. All strings are plain text (no raw HTML/Markdown); dates and years are strings, not numbers.

```json
{
  "name": "First name Last name",
  "position": "Your position",
  "affiliation": "Your university",
  "degree": "Previous degree, Field of study",
  "email": "name@example.edu",
  "language": "en",
  "description": "A brief, factual search-engine description.",
  "about": ["A short biography grounded in the supplied CV."],
  "links": [{"label": "GitHub", "url": "https://github.com/USERNAME"}],
  "projects": [{"title": "Project title", "organization": "Course or lab", "dates": "2025–2026", "details": ["Your actual contribution."]}],
  "experience": [{"title": "Research Assistant", "organization": "Your institution", "dates": "2025–Present", "group": "Research Experience", "details": ["Your actual work."]}],
  "education": [{"title": "Degree in Field of study", "organization": "Your university", "dates": "2025–Present"}],
  "publications": [{"title": "Exact paper title", "authors": "Exact authors, in order", "venue": "Exact venue or submission status", "year": "2026", "links": [{"label": "Paper", "url": "https://doi.org/VALID-DOI"}]}],
  "awards": ["Award, awarding organization, year"],
  "skills": ["Python", "R"],
  "service": [{"title": "Teaching Assistant", "organization": "Course", "dates": "2026"}]
}
```

This is a schema illustration, not facts to reuse. Do not include nonexistent placeholder links in generated sites.

Optional top-level fields:

- `theme`: style ID from [style-library.md](style-library.md), default `classic`.
- `background`: background ID from the same reference, or `none`. Omit it to use the chosen style's default background.

- `avatar`, `cv`: local `assets/...` paths. The create command fills these from `--avatar` and `--public-cv`. Never insert an absolute computer path.
- `site_url`: actual canonical URL; deployment fills it automatically.
- `publication_note`: authorship explanation only if applicable to these papers.
- `section_order`: unique section keys, chosen from `about`, `publications`, `projects`, `experience`, `education`, `awards`, `skills`, `service`. Include every populated section. Defaults to the listed order.
- `language`: `en` (default) or `zh`; affects section labels, not translation of content.

Education, experience, projects, and service share the entry structure: required `title`; optional `organization`, `dates`, `details` (list of strings), `url` (HTTP/S), and `group` (subheading).

Publications: required `title`; optional `authors`, `venue`, `year`, `badge` (short venue label shown with an image), `notes`, `image` (local file under `assets/`), `links` (each has exactly `label` and `url`). Keep author order and supplied authorship markers. Only label published work as published when the CV supports it. No citation lookup or paper images are required to finish a site.

All outbound links use HTTP/S. No HTML, JavaScript URLs, remote images, tracking IDs, passwords, or arbitrary embeds. Email uses a separate plain-address field. The generated site loads Google Fonts for the source typography, with local serif/monospace fallbacks; remove the two imports in `assets/css/font.css` if offline-only typography is required.
