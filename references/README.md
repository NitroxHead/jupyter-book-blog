# Bibliography & Citations Guide

This Jupyter Book blog supports academic citations and bibliography management using BibTeX format. The system is flexible and supports multiple workflows to accommodate different user needs.

## Quick Start

### Option 1: Single Global File (Simplest)

Perfect for casual bloggers or small blogs with shared references.

1. **Add your references** to `references/global.bib`:
   ```bibtex
   @article{smith2024,
       title = {Example Research Paper},
       author = {Smith, John and Doe, Jane},
       journal = {Journal of Example Research},
       year = {2024},
       volume = {42},
       pages = {123--145},
       doi = {10.1000/example.2024.001}
   }
   ```

2. **Use in your posts**:
   ```markdown
   Recent research {cite}`smith2024` shows that...

   ## References
   {bibliography}
   ```

### Option 2: Per-Post Files (Organized)

Perfect for academic researchers who want self-contained posts.

1. **Create a `.bib` file** alongside your post:
   ```
   posts/
   ├── my-research.md
   └── my-research.bib    ← References for this post only
   ```

2. **No configuration needed** - the system automatically finds matching `.bib` files

3. **Write your post**:
   ```markdown
   ---
   title: "My Research"
   date: "2024-03-26"
   ---

   # My Research

   Building on previous work {cite}`previous2023`...

   ## References
   {bibliography}
   ```

### Option 3: Topic-Based Files (Flexible)

Perfect for multi-topic blogs or collaborative projects.

1. **Organize by topic** in the `references/` directory:
   ```
   references/
   ├── global.bib              ← Common references
   ├── machine-learning.bib    ← ML-specific papers
   ├── climate-science.bib     ← Climate papers
   └── statistics.bib          ← Stats books
   ```

2. **All files are automatically discovered** - just cite any key from any file

3. **Use in posts**:
   ```markdown
   Machine learning techniques {cite}`ml_key2024` combined with
   climate models {cite}`climate_key2024`...
   ```

## Bibliography Modes

Configure in `blog_config.json` under `bibliography.mode`:

| Mode | Description | Best For |
|------|-------------|----------|
| `global` | Use only `references/global.bib` | Small blogs, shared references |
| `per-post` | Match `posts/name.md` with `posts/name.bib` | Academic posts, isolation |
| `all-files` | Use all `.bib` files in `references/` | Multi-topic blogs, large libraries |
| `auto` | **Smart detection with fallbacks** (recommended) | Mixed workflows, flexibility |

**Default: `auto`** - The system intelligently finds the right references for each post.

## Auto Mode Behavior

In `auto` mode, the system follows this priority:

```
For each post (e.g., posts/my-post.md):

1. Check frontmatter for bibliography field
   → If specified: Use that file

2. Check for matching per-post file
   → If posts/my-post.bib exists: Use it

3. Fall back to mode configuration
   → Use all .bib files in references/

4. Final fallback: references/global.bib
```

## Per-Post Overrides

You can override bibliography settings in individual posts using frontmatter:

```yaml
---
title: "My Research Paper"
date: "2024-03-26"
bibliography: "my-custom-refs.bib"    # Use specific .bib file
citation_style: "ieee"                 # Use specific citation style
---
```

## Citation Syntax

### Basic Citations

```markdown
Parenthetical: Recent work {cite}`smith2024` shows...
→ Output: Recent work (Smith, 2024) shows...

Textual: According to {cite:t}`smith2024`, the results...
→ Output: According to Smith (2024), the results...

Multiple: Several studies {cite}`smith2024,jones2023,brown2022` agree...
→ Output: Several studies (Smith, 2024; Jones, 2023; Brown, 2022) agree...
```

### Bibliography Directive

Add a bibliography section to your post:

```markdown
## References

{bibliography}
:filter: docname in docnames
```

This automatically generates a formatted reference list from all citations in your post.

## Citation Styles

### Built-in Styles

Configure globally in `blog_config.json`:

```json
"citation_style": "author_year"
```

Available styles:
- `plain` - Numbered citations [1], [2], [3]
- `alpha` - Author-year abbreviated [Smi24], [Jon23]
- `unsrt` - Unsorted numbered [1], [2], [3]
- `author_year` - Harvard style (Smith, 2024) **← Default**

### Custom Styles

Custom citation styles can be added in `references/styles/`. See [Custom Styles Guide](styles/README.md) for details.

Use custom styles:

```yaml
---
citation_style: "custom:ieee"
---
```

## Exporting from Reference Managers

### From Zotero
1. Select references or collection
2. Right-click → Export Collection
3. Choose format: BibTeX
4. Save to `references/` or `posts/`

### From Mendeley
1. File → Export
2. Choose: BibTeX (*.bib)
3. Save to your blog directory

### From EndNote
1. File → Export
2. Output style: BibTeX Export
3. Save as `.bib` file

### From Google Scholar
1. Click "Cite" below article
2. Click "BibTeX" link at bottom
3. Copy content to your `.bib` file

## Best Practices

### Citation Keys

Use descriptive, unique keys to avoid conflicts:

✅ **Good**:
- `smith2024climate` - Topic-specific
- `jones2023ml` - Abbreviated topic
- `brown2022_statistics` - Underscore separator

❌ **Avoid**:
- `smith2024` - Too generic (conflicts likely)
- `ref1` - Not descriptive
- `paper` - Meaningless

### Organization

#### For Small Blogs (< 20 posts):
```
references/
└── global.bib    ← All references here
```

#### For Medium Blogs (20-50 posts):
```
references/
├── global.bib         ← Common references
├── machine-learning.bib
├── data-science.bib
└── tutorials.bib
```

#### For Large Blogs (50+ posts):
```
references/
├── global.bib         ← Frequently cited works
└── [topic].bib files

posts/
├── specialized-post.md
└── specialized-post.bib    ← Post-specific refs
```

### File Naming

- ✅ Use lowercase with hyphens: `machine-learning.bib`
- ✅ Match post names: `climate-analysis.md` + `climate-analysis.bib`
- ❌ Avoid spaces: `my refs.bib`
- ❌ Avoid special characters: `refs&papers.bib`

## Validation

Run the validation script to check for issues:

```bash
python scripts/validate_bibliography.py
```

This checks for:
- Duplicate citation keys across files
- Invalid BibTeX syntax
- Missing .bib files referenced in posts
- Unused references
- Orphaned citations (cited but not defined)

## Troubleshooting

### Citations Not Showing

**Problem**: Citations appear as `{cite}`key`` in output

**Solutions**:
1. Check `.bib` file exists and is in correct location
2. Verify citation key matches exactly (case-sensitive)
3. Check BibTeX syntax for errors
4. Run `python scripts/sync_config.py` to update configuration
5. Rebuild: `jupyter-book build .`

### Duplicate Key Warnings

**Problem**: Warning about duplicate citation keys

**Solutions**:
1. Use topic-specific prefixes: `ml_smith2024`, `climate_smith2024`
2. Or use per-post `.bib` files for isolation
3. Run validation script to find conflicts

### Wrong References Appearing

**Problem**: Bibliography shows wrong papers

**Solutions**:
1. Check for duplicate keys across `.bib` files
2. Use per-post `.bib` files for isolation
3. Add `:filter: docname in docnames` to bibliography directive

## Examples

See the `posts/` directory for example posts demonstrating:
- Basic citations
- Multiple citation styles
- Custom bibliography formatting
- Per-post reference files

## Further Reading

- [Jupyter Book Citations Documentation](https://jupyterbook.org/content/citations.html)
- [sphinxcontrib-bibtex Documentation](https://sphinxcontrib-bibtex.readthedocs.io/)
- [BibTeX Format Guide](http://www.bibtex.org/Format/)
- [Custom Citation Styles](styles/README.md)
