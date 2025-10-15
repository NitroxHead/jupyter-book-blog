# Jupyter Book Blog Template

A modern, feature-rich blog framework powered by [Jupyter Book](https://jupyterbook.org/) that combines the best of technical documentation, academic publishing, and web development.

## Why Jupyter Book for Blogging?

After exploring various blogging platforms, I discovered that Jupyter Book offers a unique combination of features that make it ideal for technical content creators:

### 🎯 **Perfect for Technical Content**
- **Native Markdown Support** - Write posts in familiar `.md` format with powerful MyST extensions
- **Responsive Design** - Beautiful, mobile-friendly layouts that work across all devices
- **Complex Visualizations** - Seamlessly integrate charts, diagrams, mathematical equations, and interactive content
- **Deep Customization** - Full control over styling, themes, and functionality

### 🚀 **Modern Web Features**
- **Fast Static Site Generation** - Lightning-fast loading times with optimized HTML output
- **GitHub Integration** - Automated deployment via GitHub Actions
- **Search Functionality** - Built-in search across all content
- **Navigation & TOC** - Automatic table of contents and intuitive navigation

### 📊 **Advanced Content Capabilities**
- **Mathematical Notation** - Full LaTeX support with MathJax rendering
- **Interactive Diagrams** - Mermaid diagrams for flowcharts, sequence diagrams, and more
- **Code Highlighting** - Syntax highlighting for dozens of programming languages
- **Jupyter Notebook Integration** - Execute and display notebook content directly

## Features Showcase

This repository includes several example posts that demonstrate the system's capabilities:

### 📝 **Blog Post Examples**

| Post | Features Demonstrated |
|------|----------------------|
| **[Comprehensive Data Analysis](posts/comprehensive-data-analysis.md)** | Complete data science workflow with Python code, visualizations, mathematical formulas, and process diagrams |
| **[Interactive Diagrams with Mermaid](posts/mermaid-diagrams.md)** | Flowcharts, sequence diagrams, class diagrams, ER diagrams, state machines, and Gantt charts |
| **[Mathematical Concepts](posts/mathematical-concepts.md)** | LaTeX equations, statistical formulas, and mathematical notation |
| **[Code Examples](posts/code-examples.md)** | Multi-language syntax highlighting for Python, JavaScript, SQL, R, and more |
| **[Working with Images](posts/image-examples.md)** | Image handling, galleries, captions, and responsive layouts |
| **[Hello World!](posts/hello-world.md)** | Getting started guide and basic formatting examples |

### 🛠 **Automation Features**

- **Automatic Post Management** - Scripts automatically update homepage and table of contents
- **GitHub Actions Deployment** - Push to main branch and your site updates automatically
- **Date-based Organization** - Posts are automatically sorted by publication date
- **SEO Optimization** - Meta tags, structured data, and search engine friendly URLs

## Quick Start

### Prerequisites
- Python 3.8+
- Git

### Easy Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd jupyter-book-blog
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run interactive setup**
   ```bash
   python scripts/setup_blog.py
   ```
   This will guide you through customizing your blog title, author, repository URLs, and other settings.

4. **Build and serve locally**
   ```bash
   jupyter-book build .
   cd _build/html && python -m http.server 8000
   ```

5. **Visit your site**: `http://localhost:8000`

### Manual Configuration

If you prefer to configure manually:

1. **Edit blog_config.json** - Update your blog settings
2. **Apply configuration**: `python scripts/sync_config.py`
3. **Update content**:
   ```bash
   python scripts/update_toc.py        # Update table of contents
   python scripts/generate_posts.py    # Update homepage
   ```

### Adding New Posts

1. Create a new `.md` file in the `posts/` directory
2. Add YAML frontmatter at the top (recommended):
   ```yaml
   ---
   title: "Your Post Title"
   date: "2024-03-15"
   description: "A brief description of your post"
   ---
   ```

   **Supported date formats:**
   - ISO: `2024-03-15` (recommended)
   - US: `March 15, 2024`
   - EU: `15/03/2024`
   - US short: `03/15/2024`

   *Legacy format with dates in italics (`*March 15, 2024*`) is also supported for backwards compatibility.*

3. Run the update scripts:
   ```bash
   python scripts/update_toc.py        # Updates navigation
   python scripts/generate_posts.py    # Updates homepage
   ```
4. Rebuild: `jupyter-book build .`

The homepage and navigation will be updated automatically!

## Deployment

### GitHub Pages (Recommended)

The repository includes a GitHub Actions workflow that automatically:

1. **Syncs your configuration** from `blog_config.json`
2. **Updates table of contents** and homepage
3. **Builds the Jupyter Book**
4. **Deploys to GitHub Pages**

Simply push to the `main` branch and your site updates automatically.

**Important**: Make sure your `blog_config.json` is committed to your repository so GitHub Actions can use your customized settings.

### Disabling GitHub Actions

To disable automatic deployment, edit `blog_config.json`:
```json
{
  "deployment": {
    "github_actions": {
      "enabled": false
    }
  }
}
```

Set `"enabled": true` to re-enable deployment.

### Manual Deployment

For other platforms, build locally and deploy the `_build/html` directory.

## Customization

### Configuration

The blog uses a centralized configuration system:

1. **blog_config.json** - Main configuration file containing:
   - Blog title, author, and description
   - Repository and website URLs
   - Social media links
   - **Navigation structure** - Customize Quick Links and section titles
   - Homepage settings (banner, welcome text)
   - Post display options (date formats, sorting, description length)
   - Feature toggles (GitHub buttons, search, Mermaid, math)
   - Build settings (exclude patterns, notebook execution)

2. **Automated Sync** - Changes in `blog_config.json` are automatically applied to:
   - `_config.yml` (Jupyter Book configuration)
   - `_toc.yml` (Navigation structure)
   - `index.md` (Homepage content)
   - Scripts behavior

### Easy Customization Steps

1. **Run setup script**: `python scripts/setup_blog.py` (interactive)
2. **Or edit manually**: Update `blog_config.json`
3. **Apply changes**: `python scripts/sync_config.py`
4. **Rebuild**: `jupyter-book build .`

### Styling

- Add custom CSS in `_static/` directory
- Modify HTML templates
- Customize Mermaid diagram styling

### Customizing Navigation

Edit `blog_config.json` to customize the navigation structure:

```json
"navigation": {
  "quick_links": [
    {"title": "About", "file": "about"},
    {"title": "Projects", "file": "projects"},
    {"title": "Contact", "file": "contact"}
  ],
  "blog_section_title": "Blog Posts"
}
```

After editing, run `python scripts/update_toc.py` to apply changes.

### Content Organization

- Organize posts in the `posts/` directory
- Add images to `images/` with subdirectories
- Create custom navigation pages (About, Projects, etc.) in the root directory

## Why This Approach?

Traditional blogging platforms often limit technical content creators. Jupyter Book provides:

- **Academic-Quality Typesetting** - Professional mathematical and scientific notation
- **Developer-Friendly Workflow** - Git-based, markdown-driven content creation
- **Extensible Architecture** - Full control over features and functionality
- **Performance Optimized** - Fast static sites with modern web standards
- **Future-Proof** - Open source with active development community

Perfect for researchers, data scientists, developers, and anyone who needs to combine narrative content with technical visualizations.

## License

This template is open source and available under the MIT License. Feel free to fork, modify, and use for your own projects!

## Contributing

Found a bug or have a feature request? Please open an issue or submit a pull request. Contributions welcome!

---

**Built with ❤️ using [Jupyter Book](https://jupyterbook.org/)**