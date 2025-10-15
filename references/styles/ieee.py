"""
IEEE Citation Style for Jupyter Book

Features:
- Numbered citations [1], [2], [3]
- References sorted by order of appearance
- Abbreviated journal names
- DOI links included when available

Usage in post frontmatter:
    ---
    citation_style: "custom:ieee"
    ---
"""

from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.formatting import toplevel
from pybtex.style.template import (
    field, tag, optional, sentence, join, words, together
)
from pybtex.plugin import register_plugin


class IEEEStyle(UnsrtStyle):
    """IEEE citation style - numbered citations in square brackets."""

    name = 'ieee'
    default_sorting_style = 'none'  # Sort by order of appearance

    def format_labels(self, sorted_entries):
        """Generate numeric labels for citations."""
        for number, entry in enumerate(sorted_entries, start=1):
            yield f"[{number}]"

    def format_article(self, entry):
        """
        Format journal articles.

        Format: Author(s), "Article Title," Journal Name, vol. X, no. Y, pp. Z-Z, Year.
        """
        template = toplevel [
            self.format_names('author'),
            ', ',
            sentence [ '"', field('title'), '"' ],
            tag('em') [ field('journal') ],
            optional [ ', vol. ', field('volume') ],
            optional [ ', no. ', field('number') ],
            optional [ ', pp. ', field('pages') ],
            ', ',
            field('year'),
            optional [ ', doi: ', self.format_doi(entry) ],
            '.'
        ]
        return template.format_data(entry)

    def format_book(self, entry):
        """
        Format books.

        Format: Author(s), Book Title, Edition. City: Publisher, Year.
        """
        template = toplevel [
            self.format_names('author'),
            ', ',
            tag('em') [ field('title') ],
            optional [ ', ', field('edition'), ' ed.' ],
            '. ',
            optional [ field('address'), ': ' ],
            field('publisher'),
            ', ',
            field('year'),
            '.'
        ]
        return template.format_data(entry)

    def format_inproceedings(self, entry):
        """
        Format conference proceedings.

        Format: Author(s), "Paper Title," in Conference Name, Year, pp. Z-Z.
        """
        template = toplevel [
            self.format_names('author'),
            ', ',
            sentence [ '"', field('title'), '"' ],
            'in ',
            tag('em') [ field('booktitle') ],
            ', ',
            field('year'),
            optional [ ', pp. ', field('pages') ],
            optional [ ', doi: ', self.format_doi(entry) ],
            '.'
        ]
        return template.format_data(entry)

    def format_misc(self, entry):
        """
        Format miscellaneous entries (websites, datasets, software, etc.).
        """
        template = toplevel [
            optional [ self.format_names('author'), ', ' ],
            sentence [ field('title') ],
            optional [ field('howpublished'), ', ' ],
            optional [ field('year') ],
            optional [ '. Available: ', field('url') ],
            optional [ '. Accessed: ', field('note') ],
            '.'
        ]
        return template.format_data(entry)

    def format_doi(self, entry):
        """Format DOI as a hyperlink."""
        if 'doi' in entry.fields:
            doi = entry.fields['doi']
            return tag('a', href=f'https://doi.org/{doi}') [ doi ]
        return None


# Register the IEEE style plugin
register_plugin('pybtex.style.formatting', 'ieee', IEEEStyle)
