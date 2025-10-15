"""
Nature Journal Citation Style for Jupyter Book

Features:
- Superscript numbered citations¹ ² ³
- References sorted by order of appearance
- Author list (max 5, then et al.)
- Journal name in italics
- Compact format

Usage in post frontmatter:
    ---
    citation_style: "custom:nature"
    ---
"""

from pybtex.style.formatting.unsrt import Style as UnsrtStyle
from pybtex.style.formatting import toplevel
from pybtex.style.template import (
    field, tag, optional, sentence, join, words, together
)
from pybtex.plugin import register_plugin
from pybtex.richtext import Text


class NatureStyle(UnsrtStyle):
    """Nature journal citation style - superscript numbered citations."""

    name = 'nature'
    default_sorting_style = 'none'  # Sort by order of appearance

    def format_labels(self, sorted_entries):
        """Generate superscript numeric labels for citations."""
        for number, entry in enumerate(sorted_entries, start=1):
            # Note: Actual superscript rendering depends on Sphinx/HTML configuration
            # This returns the number which can be styled as superscript in HTML
            yield str(number)

    def format_names_nature(self, role, entry):
        """
        Format author names in Nature style.

        Shows first 5 authors, then 'et al.' if more.
        Format: Last, F. M.
        """
        if role not in entry.persons:
            return None

        persons = entry.persons[role]
        max_authors = 5

        formatted_authors = []
        for i, person in enumerate(persons[:max_authors]):
            last = ' '.join(person.last_names)
            initials = '. '.join(n[0] for n in person.first_names + person.middle_names if n)
            if initials:
                formatted_authors.append(f"{last}, {initials}.")
            else:
                formatted_authors.append(last)

        if len(persons) > max_authors:
            author_list = Text(', ').join(Text(a) for a in formatted_authors)
            return together [ author_list, Text(' et al.') ]
        else:
            if len(formatted_authors) == 1:
                return Text(formatted_authors[0])
            elif len(formatted_authors) == 2:
                return Text(' & ').join(Text(a) for a in formatted_authors)
            else:
                all_but_last = Text(', ').join(Text(a) for a in formatted_authors[:-1])
                return together [ all_but_last, Text(' & '), Text(formatted_authors[-1]) ]

    def format_article(self, entry):
        """
        Format journal articles in Nature style.

        Format: Authors. Title. Journal vol, pages (year).
        """
        template = toplevel [
            self.format_names_nature('author', entry),
            '. ',
            field('title'),
            '. ',
            tag('em') [ field('journal') ],
            ' ',
            tag('strong') [ field('volume') ],
            optional [ ', ', field('pages') ],
            ' (',
            field('year'),
            ').',
            optional [ ' ', self.format_doi(entry) ]
        ]
        return template.format_data(entry)

    def format_book(self, entry):
        """
        Format books in Nature style.

        Format: Authors. Title (Publisher, year).
        """
        template = toplevel [
            self.format_names_nature('author', entry),
            '. ',
            tag('em') [ field('title') ],
            optional [ ' (', field('edition'), ' edn)' ],
            ' (',
            field('publisher'),
            ', ',
            field('year'),
            ').',
            optional [ ' ', self.format_doi(entry) ]
        ]
        return template.format_data(entry)

    def format_inproceedings(self, entry):
        """
        Format conference proceedings in Nature style.
        """
        template = toplevel [
            self.format_names_nature('author', entry),
            '. ',
            field('title'),
            '. in ',
            tag('em') [ field('booktitle') ],
            optional [ ', ', field('pages') ],
            ' (',
            field('year'),
            ').',
            optional [ ' ', self.format_doi(entry) ]
        ]
        return template.format_data(entry)

    def format_misc(self, entry):
        """
        Format miscellaneous entries in Nature style.
        """
        template = toplevel [
            optional [ self.format_names_nature('author', entry), '. ' ],
            tag('em') [ field('title') ],
            optional [ '. ', field('howpublished') ],
            optional [ ' (', field('year'), ')' ],
            optional [ '. ', field('url') ],
            '.'
        ]
        return template.format_data(entry)

    def format_doi(self, entry):
        """Format DOI as a hyperlink."""
        if 'doi' in entry.fields:
            doi = entry.fields['doi']
            url = f'https://doi.org/{doi}'
            return tag('a', href=url) [ f'doi:{doi}' ]
        return None


# Register the Nature style plugin
register_plugin('pybtex.style.formatting', 'nature', NatureStyle)
