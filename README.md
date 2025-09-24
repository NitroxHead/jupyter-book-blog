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
| **[Comprehensive Data Analysis](book/comprehensive-data-analysis.md)** | Complete data science workflow with Python code, visualizations, mathematical formulas, and process diagrams |
| **[Interactive Diagrams with Mermaid](book/mermaid-diagrams.md)** | Flowcharts, sequence diagrams, class diagrams, ER diagrams, state machines, and Gantt charts |
| **[Mathematical Concepts](book/mathematical-concepts.md)** | LaTeX equations, statistical formulas, and mathematical notation |
| **[Code Examples](book/code-examples.md)** | Multi-language syntax highlighting for Python, JavaScript, SQL, R, and more |
| **[Working with Images](book/image-examples.md)** | Image handling, galleries, captions, and responsive layouts |
| **[Hello World!](book/hello-world.md)** | Getting started guide and basic formatting examples |

### 🛠 **Automation Features**

- **Automatic Post Management** - Scripts automatically update homepage and table of contents
- **GitHub Actions Deployment** - Push to main branch and your site updates automatically
- **Date-based Organization** - Posts are automatically sorted by publication date
- **SEO Optimization** - Meta tags, structured data, and search engine friendly URLs

## Quick Start

### Prerequisites
- Python 3.8+
- Git

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd jupyter-book-blog
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Update content and metadata**
   ```bash
   python scripts/update_toc.py        # Update table of contents
   python scripts/generate_posts.py    # Update homepage
   ```

4. **Build and serve locally**
   ```bash
   jupyter-book build .
   cd _build/html && python -m http.server 8000
   ```

5. **Visit your site**: `http://localhost:8000`

### Adding New Posts

1. Create a new `.md` file in the `book/` directory
2. Add frontmatter with date in this format: `*March 15, 2024*`
3. Run the update scripts:
   ```bash
   python scripts/update_toc.py
   python scripts/generate_posts.py
   ```
4. Rebuild: `jupyter-book build .`

The homepage and navigation will be updated automatically!

## Deployment

### GitHub Pages (Recommended)

The repository includes a GitHub Actions workflow that automatically:

1. Updates table of contents and homepage
2. Builds the Jupyter Book
3. Deploys to GitHub Pages

Simply push to the `main` branch and your site updates automatically.

### Manual Deployment

For other platforms, build locally and deploy the `_build/html` directory.

## Customization

### Configuration

Edit `_config.yml` to customize:
- Site title and author
- Theme colors and styling
- Repository links
- Analytics integration

### Styling

- Add custom CSS in `_static/` directory
- Modify HTML templates
- Customize Mermaid diagram styling

### Content Organization

- Organize posts in the `book/` directory
- Add images to `images/` with subdirectories
- Use the `examples/` directory for reference content

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