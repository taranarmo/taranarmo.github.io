# Sergei Volkov — Personal Landing Page & Website

Source repository for [taranarmo.github.io](https://taranarmo.github.io/).

## 🌟 Overview

- **Source Content**: Authoring in clean Markdown with YAML frontmatter at [`content/index.md`](content/index.md).
- **Templates & Styling**: Jinja2 HTML5 semantic template in [`templates/index.html`](templates/index.html) and modern responsive CSS in [`assets/style.css`](assets/style.css).
- **CV Integration**: The [`cv/`](cv/) directory contains compiled production PDF & HTML resumes synced automatically from [CV-with-Markdown-and-Nix](https://github.com/taranarmo/CV-with-Markdown-and-Nix).
- **Reproducible Build & Dev Environment**: Managed declaratively with [Nix Flakes](flake.nix).

---

## 🚀 Quickstart & Local Development

### 1. Preview locally with Nix (Recommended)

Start the local development server at `http://localhost:8080`:

```bash
nix run
```

*(You can customize the port: `PORT=3000 nix run`)*

Or using Make:
```bash
make serve
```

### 2. Build Static Site

Compile `content/index.md` and assets directly into the repository root (`index.html` and `style.css`):

```bash
nix run .#build
# or
make build
```

Or build the pure isolated Nix derivation into `./result`:

```bash
nix build
```

---

## 📁 Repository Structure

```
.
├── content/
│   └── index.md          # Primary Markdown source with frontmatter & content
├── templates/
│   └── index.html        # HTML5 Jinja2 layout template
├── assets/
│   └── style.css         # Minimalist responsive stylesheet (Dark/Light mode)
├── scripts/
│   └── build.py          # Python static site builder
├── cv/                   # Synced CV PDFs and HTML exports (Industry, Academic, Publications)
├── index.html            # Production landing page (GitHub Pages root)
├── style.css             # Production stylesheet (GitHub Pages root)
├── flake.nix             # Nix flake definition (build, serve, devShell)
├── flake.lock            # Pinned Nix flake dependencies
└── Makefile              # Convenient make commands (build, serve, clean)
```
