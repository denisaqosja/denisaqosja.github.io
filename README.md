# Denisa Qosja — research portfolio

A responsive academic website for GitHub Pages: profile, publications, three detailed code projects, and a downloadable public CV. Inspired by the compact academic structure of Mario Qosja’s homepage and the user’s request for a visual publication list.

The site works without a framework, runtime dependencies, accounts, or third-party assets. All essential content and navigation work without JavaScript. JavaScript adds publication filtering, citation copying, and an illustrative Doppler response slider.

## Preview

```bash
python3 scripts/build.py
python3 scripts/check.py
python3 -m http.server 8000 --directory dist
```

Open `http://localhost:8000`, or open `dist/index.html` directly. Direct file opening supports the complete site; clipboard behavior depends on browser permissions and falls back to selecting the citation.

## Publish on GitHub

The included workflow builds and checks the site, then deploys only `dist/` to GitHub Pages.

1. Create a repository named `denisaqosja.github.io` under `denisaqosja` for the account’s main website. If a repository with that name already exists, inspect and preserve its content before integrating this project.
2. Upload this project’s source, including `.github/workflows/pages.yml`, or push it using Git. Do not upload the parent directory containing private documents.
3. In the repository’s **Settings → Pages → Build and deployment**, choose **GitHub Actions** as the source.
4. Push to `main`, or run **Deploy portfolio to GitHub Pages** from the Actions tab. Wait for a successful deployment before treating the website as live.

The expected account-site address is `https://denisaqosja.github.io/`; this address is a deployment target, not a claim that it has been published. The site also supports project repositories because all local links are relative.

Publishing setup follows [GitHub’s Pages documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Update content

| File | Purpose |
| --- | --- |
| `content/profile.json` | Bio, links, work history, education, skills |
| `content/publications.json` | Publication metadata, summaries, links, BibTeX |
| `content/projects.json` | Project abstracts, repository links, descriptions, figures |
| `web/styles.css` | Typography, colors, responsive layouts, print styles |
| `web/main.js` | Publication search, citation copy, Doppler illustration |
| `scripts/build.py` | Generates the four complete HTML pages and bibliography |
| `assets/` | Local photographs, diagrams, chart, and downloadable CV |

After editing, run the build and check commands. Push source changes to `main`; the workflow generates the published HTML. Generated `dist/` and temporary files are ignored by Git.

The CV PDF is committed as an asset so GitHub does not need a LaTeX installation. To update the PDF from the same profile and publication JSON, run `python3 scripts/build_cv.py` with `pdflatex` and standard LaTeX packages available, then rebuild the website. Review both PDF pages after regeneration.

The optional `scripts/generate_figures.py` regenerates original research diagrams and charts using NumPy and Matplotlib. Figure generation is not needed for normal site builds or deployment.

## Content and verification

See [SOURCES.md](SOURCES.md) for provenance and figure interpretation. Professional history was drafted from the local English CV dated March 2026 and cross-checked against the public ORCID record. Review the current affiliation, dates, and contact details when updating the site. The public PDF is a newly typeset version: it omits residential address, phone number, and references’ contact information.

The integrity check verifies local resources, fragment links, page landmarks, image descriptions, SVG parsing, bibliography output, and PDF presence. Browser-based desktop/mobile visual verification was unavailable in the authoring session. Responsive rules are included; inspect the pages on desktop and mobile before the first public release.
