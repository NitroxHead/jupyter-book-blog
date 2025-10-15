"""
APA 7th Edition Citation Style for Jupyter Book

Features:
- Author-year citations (Smith, 2024) or (Smith & Jones, 2024)
- Alphabetical reference sorting
- Hanging indent in bibliography
- "et al." for 3+ authors in citations
- DOI as https://doi.org/...

Usage in post frontmatter:
    ---
    citation_style: "custom:apa"
    ---
"""

from pybtex.style.formatting import BaseStyle, toplevel
from pybtex.style.template import (
    field, tag, optional, sentence, join, words, together, names
)
from pybtex.style.sorting import BaseSortingStyle
from pybtex.plugin import register_plugin
from pybtex.richtext import Text


class APASortingStyle(BaseSortingStyle):
    """Sort entries alphabetically by author last name, then year."""

    def sorting_key(self, entry):
        if 'author' in entry.persons:
            author = entry.persons['author'][0].last_names[0]
        elif 'editor' in entry.persons:
            author = entry.persons['editor'][0].last_names[0]
        else:
            author = entry.fields.get('title', '')

        year = entry.fields.get('year', '9999')
        return (author.lower(), year)


class APAStyle(BaseStyle):
    """APA 7th Edition citation style."""

    name = 'apa'
    default_sorting_style = APASortingStyle

    def format_labels(self, sorted_entries):
        """Generate author-year labels for citations."""
        for entry in sorted_entries:
            if 'author' in entry.persons:
                authors = entry.persons['author']
                if len(authors) == 1:
                    label = authors[0].last_names[0]
                elif len(authors) == 2:
                    label = f"{authors[0].last_names[0]} & {authors[1].last_names[0]}"
                else:
                    label = f"{authors[0].last_names[0]} et al."
            else:
                label = entry.fields.get('title', 'Unknown')[:20]

            year = entry.fields.get('year', 'n.d.')
            yield f"{label}, {year}"

    def format_author_or_editor(self, entry):
        """Format authors or editors in APA style."""
        if 'author' in entry.persons:
            return self.format_names('author', entry)
        elif 'editor' in entry.persons:
            editors = self.format_names('editor', entry)
            return together [ editors, ' (Ed', optional [ 's' ], ')' ]
        else:
            return None

    def format_names(self, role, entry):
        """Format author/editor names in APA style: Last, F. M."""
        if role not in entry.persons:
            return None

        persons = entry.persons[role]
        if len(persons) > 20:
            # For many authors, show first 19, then ..., then last
            formatted = []
            for i in range(19):
                formatted.append(self.format_person(persons[i]))
            formatted.append('...')
            formatted.append(self.format_person(persons[-1]))
            return Text(', ').join(formatted)
        else:
            formatted = [self.format_person(person) for person in persons]
            if len(formatted) == 1:
                return formatted[0]
            elif len(formatted) == 2:
                return Text(' & ').join(formatted)
            else:
                # Oxford comma before &
                return Text(', ').join(formatted[:-1]) + Text(', & ') + formatted[-1]

    def format_person(self, person):
        """Format a single person: Last, F. M."""
        last = ' '.join(person.last_names)
        initials = '. '.join(n[0] for n in person.first_names + person.middle_names if n)
        if initials:
            return Text(f"{last}, {initials}.")
        return Text(last)

    def format_article(self, entry):
        """
        Format journal articles in APA style.

        Format: Author(s). (Year). Title. Journal, Volume(Issue), pages. https://doi.org/...
        """
        template = toplevel [
            self.format_author_or_editor(entry),
            ' (',
            field('year'),
            '). ',
            field('title'),
            '. ',
            tag('em') [ field('journal') ],
            optional [ ', ', tag('em') [ field('volume') ] ],
            optional [ '(', field('number'), ')' ],
            optional [ ', ', field('pages') ],
            '. ',
            optional [ self.format_doi(entry) ]
        ]
        return template.format_data(entry)

    def format_book(self, entry):
        """
        Format books in APA style.

        Format: Author(s). (Year). Title (Edition). Publisher. https://doi.org/...
        """
        template = toplevel [
            self.format_author_or_editor(entry),
            ' (',
            field('year'),
            '). ',
            tag('em') [ field('title') ],
            optional [ ' (', field('edition'), ' ed.)' ],
            '. ',
            field('publisher'),
            optional [ '. ', self.format_doi(entry) ]
        ]
        return template.format_data(entry)

    def format_inproceedings(self, entry):
        """
        Format conference proceedings in APA style.

        Format: Author(s). (Year). Title. In Editor (Ed.), Conference (pp. pages). Publisher.
        """
        template = toplevel [
            self.format_names('author', entry),
            ' (',
            field('year'),
            '). ',
            field('title'),
            '. In ',
            optional [ self.format_names('editor', entry), ' (Ed.), ' ],
            tag('em') [ field('booktitle') ],
            optional [ ' (pp. ', field('pages'), ')' ],
            '. ',
            optional [ field('publisher') ],
            optional [ '. ', self.format_doi(entry) ]
        ]
        return template.format_data(entry)

    def format_misc(self, entry):
        """
        Format miscellaneous entries (websites, datasets, etc.) in APA style.
        """
        template = toplevel [
            optional [ self.format_author_or_editor(entry), '. ' ],
            optional [ '(', field('year'), '). ' ],
            tag('em') [ field('title') ],
            optional [ ' [', field('howpublished'), ']' ],
            '. ',
            optional [ field('publisher'), '. ' ],
            optional [ field('url') ]
        ]
        return template.format_data(entry)

    def format_doi(self, entry):
        """Format DOI as https://doi.org/... per APA 7th edition."""
        if 'doi' in entry.fields:
            doi = entry.fields['doi']
            url = f'https://doi.org/{doi}'
            return tag('a', href=url) [ url ]
        return None


# Register the APA style plugin
register_plugin('pybtex.style.formatting', 'apa', APAStyle)
register_plugin('pybtex.style.sorting', 'apa', APASortingStyle)
