# GitHub Pages deployment

Requirements: Python 3.9+, Git, GitHub CLI, a GitHub account. `gh auth login` is interactive; let the user authenticate. Never ask them to paste tokens into chat or put secrets into site files. Check `gh auth status` and `gh api user --jq .login`. Git also needs a configured author name/email for commits; use the user's chosen identity, not a guessed personal email.

The helper supports personal accounts and brand-new public repositories only. It rejects the original `liranmao/liranmao.github.io` and skill-distribution repository `liranmao/cv-to-homepage`. Organization destinations and deliberate updates to an existing user-owned site need a manual, explicitly scoped workflow.

## Confirm the destination with the user

Follow the naming step in `SKILL.md` before a new public deployment. Ask for the name they want in the website address, then show the available `OWNER/REPO`, its public visibility and the full expected Pages URL. A project repository named `my-homepage` publishes to `https://OWNER.github.io/my-homepage/`; an available and permitted `OWNER.github.io` repository publishes to `https://OWNER.github.io/`.

Check availability with read-only calls before presenting the final choice. Only a 404 establishes that the repository is absent; authentication, permission and network failures do not. The dry-run command below calculates the expected address but does not check availability or record user consent. The agent must obtain confirmation in the conversation before using `--publish` or performing equivalent writes manually. Do not add another prompt inside the noninteractive helper.

If the name becomes unavailable between confirmation and deployment, stop, suggest another name and confirm the new address. For a partial deployment, retain the confirmed destination and inspect it before resuming. Routine updates to the same confirmed site do not repeat this naming step.

## What the helper does

1. Without `--publish`, show the exact destination, visibility, source and expected URL; no network writes.
2. With `--publish`, check authentication, matching owner, and a 404 for the destination. Other errors stop the operation.
3. Rebuild `docs/`, initialize a fresh Git repository on `main`, and stage only the generated public site and necessary source files. No `git add .`, copied Git history, credentials, or original CV.
4. Create the new public repo, push, and configure Pages from `main:/docs` via `gh api`.
5. Poll for up to four minutes, then fetch the live URL and check the expected name. A timeout is reported as pending, not success.

GitHub supplies HTTPS and hosting for public repositories on its free plan. No custom domain is needed. Relative asset URLs support both `https://USERNAME.github.io/` and `https://USERNAME.github.io/REPO/`.

## Recovery after an interrupted deployment

Do not rerun the creation helper against an existing Git checkout. Inspect `git status`, `git remote -v`, `gh repo view OWNER/REPO`, `gh api repos/OWNER/REPO/pages`, and the repository's Actions status. Verify the owner/repository is exactly the authorized new destination. Resume only the missing step:

- Git author identity error: set the user's chosen identity, then stage/commit the reviewed files.
- Repo created but push failed: verify `origin`, then push `main` using normal Git authentication. No force push.
- Pages missing: configure Settings → Pages → Deploy from a branch → `main` → `/docs`, or use the equivalent API call below.
- Pages reports a different existing source/domain: do not overwrite that configuration without understanding the prior deployment.
- Permission error: explain the missing repository administration/Pages permission or offer the Settings UI. Do not expand token scopes automatically.
- Pending build: inspect the Actions tab and `gh api repos/OWNER/REPO/pages/builds/latest`, then fetch the returned `html_url` when built.

```bash
gh api --method POST repos/OWNER/REPO/pages \
  -f 'build_type=legacy' -f 'source[branch]=main' -f 'source[path]=/docs'
```

For updates requested by the user: edit `site.json` and selected assets, run `python3 build.py`, preview, inspect the diff, then stage only intended public changes and push. Keep raw input files outside the repository. Never change the original template repository.

Official references: [GitHub Pages setup](https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site), [Pages API](https://docs.github.com/en/rest/pages/pages#create-a-github-pages-site), [Codex skill discovery](https://developers.openai.com/codex/skills/), [Claude Code skills](https://code.claude.com/docs/en/skills).
