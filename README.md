# CSE 4165 Web Final Prep

A one-page study site for the UIU CSE 4165 / CSE 465 Web Programming final: JavaScript, PHP and MySQL lessons, all six past finals (Fall 2024 – Spring 2026) solved with explanations and live demos, practice problems, a quiz and a cheatsheet.

**Live site:** https://meteorboyf.github.io/Web_Final/

## Structure

- `prep-site/src/*.html` — page fragments, concatenated in filename order
- `prep-site/build.py` — builds `prep-site/index.html` (code blocks are written raw with `@@code lang title … @@end`, tables with `@@table … @@end`)
- `.github/workflows/pages.yml` — builds and deploys to GitHub Pages on every push to `main`

## Build locally

```bash
python3 prep-site/build.py
```

Then open `prep-site/index.html` in a browser.
