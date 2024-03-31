---
author:
- The Author
docversion: reproducible
finished: true
identifier:
- scheme: DOI
  text: "doi:10.234234.234/33"
lang: en-GB
notes: foo
poetry-lines: 8
publications:
- accepted: 2022-12-12
  published: 2022-12-13
  submitted: 2022-12-11
  urls:
  - "http://example.com"
  venue: Foo
- rejected: 2022-11-12
  submitted: 2022-11-11
  venue: Bar
source-md5: 2518a18c39cbd5e88b46c164d163e14a
subject: "Version: reproducible"
title: The Title
wordcount: 284
---

This is some text before a section. It shouldn’t be indented.

# This is a section {#__h1_1}

This is some test text. This is formatted in *italics* and **bold**, with - various – dashes—, and trailing dots…

This is a bullet list:

-   This is the first paragraph of the first item.

    And the second paragraph of the first item.

-   The second item only has one paragraph.

This is a numbered list:

1.  This is the first paragraph of the first item.

    And the second paragraph of the first item.

2.  The second item only has one paragraph.

‘These quotes should be curly,’ and “so should these.” There should be a blank line before the next paragraph:

 

And then there should be some text ^in superscript^ and ~in subscript~, and a footnote[^1] with a star, a footnote[^2] with a dagger, and this should be `monospace`.

## Subsection {#__h2_1}

Test text test text test text.

> This is a quote block. It should be indented slightly and shouldn’t contain a line break.
>
> This is a second paragraph in the same quote block.

> | This is a quoted line block. It should be indented slightly
> | and have a *line break* after ‘slightly’, and **formatting**.

> | “These literal double curly quotes, used where smart
> | quotes gets it wrong, curl the right way even though
> | they’re on different lines.”

> | ‘These literal single curly quotes, used where smart
> | quotes gets it wrong, curl the right way even though
> | they’re on different lines.’

After this line there should be stars.

------------------------------------------------------------------------

This is a new paragraph after the stars. This text is [Small Caps]{.smallcaps}. Here is a pound sign (£), a euro sign (€), and three letters with accents: ëóû.

[^1]: This is a footnote. It should appear at the bottom of the page.

[^2]: Another footnote.
