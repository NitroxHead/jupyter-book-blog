# Custom Citation Styles Guide

This directory contains custom citation styles for your Jupyter Book blog. Citation styles control how references appear in your bibliographies and how citations are formatted in your text.

## Available Custom Styles

| Style | Description | Citation Format | Reference Format |
|-------|-------------|-----------------|------------------|
| `ieee` | IEEE numbered style | [1], [2], [3] | Numbered, sorted by appearance |
| `apa` | APA 7th edition | (Smith, 2024) | Alphabetical, hanging indent |
| `nature` | Nature journal style | Superscript¹ ² ³ | Numbered, sorted by appearance |

## Using Custom Styles

### Global Configuration

In `blog_config.json`:

```json
{
  "bibliography": {
    "citation_style": "custom:ieee"
  }
}
```

Then run:
```bash
python scripts/sync_config.py
jupyter-book build .
```

### Per-Post Override

In your post frontmatter:

```yaml
---
title: "My Research Paper"
date: "2024-03-26"
citation_style: "custom:nature"
---
```

## Built-in Styles (No Custom File Needed)

Jupyter Book/pybtex includes these built-in styles:

- `plain` - Numbered citations [1], [2], references sorted alphabetically
- `alpha` - Author-year label [Smi24], [Jon23]
- `unsrt` - Numbered unsorted [1], [2], references in order of citation
- `author_year` - Parenthetical (Smith, 2024)

Use built-in styles without the `custom:` prefix:

```json
"citation_style": "author_year"
```

## Creating Custom Styles

Custom styles use the pybtex Python API. Here's how to create your own:

### 1. Choose a Base Style

Start with an existing pybtex style:

```python
from pybtex.style.formatting.unsrt import Style as UnsrtStyle
# or
from pybtex.style.formatting.plain import Style as PlainStyle
# or
from pybtex.style.formatting import alpha import Style as AlphaStyle
```

### 2. Create Your Style Class

```python
class MyCustomStyle(UnsrtStyle):
    """My custom citation style."""

    def format_labels(self, sorted_entries):
        """Generate citation labels."""
        for number, entry in enumerate(sorted_entries, start=1):
            yield str(number)  # or your custom format
```

### 3. Customize Formatting Methods

Override methods to control how each entry type appears:

```python
def format_article(self, entry):
    """Format journal articles."""
    template = toplevel [
        sentence [ field('author') ],
        sentence [ '"', field('title'), '"' ],
        sentence [
            tag('em') [ field('journal') ],
            optional [ ', vol. ', field('volume') ],
            optional [ ', no. ', field('number') ],
            optional [ ', pp. ', field('pages') ],
            ', ',
            field('year')
        ],
    ]
    return template.format_data(entry)
```

### 4. Register the Plugin

```python
from pybtex.plugin import register_plugin

register_plugin('pybtex.style.formatting', 'mycustom', MyCustomStyle)
```

### 5. Install the Style

**Option A: Drop-in (Simple)**

Place your `.py` file in `references/styles/` and it will be auto-discovered.

**Option B: Package (Advanced)**

Create a proper Python package with `setup.py`:

```python
from setuptools import setup

setup(
    name='my-citation-styles',
    entry_points={
        'pybtex.style.formatting': [
            'mycustom = my_styles:MyCustomStyle',
        ],
    },
)
```

## Example: IEEE Style

See `ieee.py` in this directory for a complete working example.

**Features:**
- Numbered citations [1], [2], [3]
- References sorted by order of appearance
- Abbreviated journal names
- DOI links included

**Usage:**
```yaml
---
citation_style: "custom:ieee"
---
```

## Example: APA Style

See `apa.py` for APA 7th edition formatting.

**Features:**
- Author-year citations (Smith, 2024)
- Hanging indent in references
- "et al." for 3+ authors
- DOI as https://doi.org/...

**Usage:**
```yaml
---
citation_style: "custom:apa"
---
```

## Example: Nature Style

See `nature.py` for Nature journal style.

**Features:**
- Superscript citations¹ ² ³
- Numbered references
- Author list (max 5, then et al.)
- Journal name in italics

**Usage:**
```yaml
---
citation_style: "custom:nature"
---
```

## Template Engine Basics

Pybtex uses a template-based formatting system. Common template elements:

### Basic Fields

```python
field('author')    # Author names
field('title')     # Article/book title
field('year')      # Publication year
field('journal')   # Journal name
field('volume')    # Volume number
field('pages')     # Page range
field('doi')       # Digital Object Identifier
```

### Formatting Tags

```python
tag('em') [ field('journal') ]        # Italic text
tag('strong') [ field('title') ]      # Bold text
tag('a', href=...) [ field('url') ]   # Hyperlink
```

### Optional Fields

```python
optional [ ', vol. ', field('volume') ]   # Only if volume exists
optional [ ', pp. ', field('pages') ]     # Only if pages exist
```

### Sentences and Groups

```python
sentence [ field('author'), field('title') ]  # Period at end
together [ 'pp. ', field('pages') ]           # No separation
```

### Joining

```python
join [ ' and ' ] [ field('author') ]   # Join authors with 'and'
```

## Testing Your Style

1. **Create a test post**:
   ```markdown
   ---
   title: "Style Test"
   citation_style: "custom:mystyle"
   ---

   Test citation {cite}`example2024`.

   ## References
   {bibliography}
   ```

2. **Build and check**:
   ```bash
   jupyter-book build .
   ```

3. **View the output** in `_build/html/posts/test-post.html`

## Common Customizations

### Change Citation Format

```python
def format_labels(self, sorted_entries):
    """Custom citation labels."""
    for entry in sorted_entries:
        # Numbered: yield "1", "2", "3"
        yield str(sorted_entries.index(entry) + 1)

        # Alpha: yield "Smi24", "Jon23"
        author = entry.persons['author'][0]
        yield f"{author.last_names[0][:3]}{entry.fields['year'][2:]}"
```

### Limit Author List

```python
from pybtex.richtext import Text, Tag

def format_authors(self, authors):
    """Format author list with et al. for many authors."""
    if len(authors) > 3:
        # Show first 3 authors + et al.
        names = [self.format_author(author) for author in authors[:3]]
        return Text(', ').join(names) + Text(', et al.')
    else:
        names = [self.format_author(author) for author in authors]
        return Text(', ').join(names)
```

### Add DOI Links

```python
optional [
    tag('a', href=join('https://doi.org/', field('doi'))) [
        'https://doi.org/', field('doi')
    ]
]
```

## Debugging

### Enable Verbose Output

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Plugin Registration

```bash
python3 -c "from pybtex.plugin import find_plugin; print(find_plugin('pybtex.style.formatting', 'mystyle'))"
```

### Validate BibTeX Rendering

```bash
pybtex -f html -s mystyle references/global.bib
```

## Further Reading

- [Pybtex Formatting API](https://docs.pybtex.org/api/formatting.html)
- [Pybtex Style Design Guide](https://docs.pybtex.org/api/styles.html)
- [sphinxcontrib-bibtex Documentation](https://sphinxcontrib-bibtex.readthedocs.io/)
- [BibTeX Entry Types](http://www.bibtex.org/Entry-Types/)

## Contributing Styles

If you create a useful custom style, consider:

1. Adding it to this directory
2. Documenting its features
3. Providing test cases
4. Sharing with the community

Have a style to share? Open an issue or pull request!
