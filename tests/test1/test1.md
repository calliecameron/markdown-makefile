---
title: The Title
author:
- The Author
identifier:
- scheme: DOI
  text: doi:10.234234.234/33
publications:
- venue: Foo
  submitted: 2022-12-11
  accepted: 2022-12-12
  published: 2022-12-13
  urls:
  - "http://example.com"
- venue: Bar
  submitted: 2022-11-11
  rejected: 2022-11-12
notes: foo
finished: true
---

This is some text before a section. It shouldn't be indented.

# This is a section

This is some test text. This is formatted in *italics* and **bold**, with - various -- dashes---, and trailing dots...

This is a bullet list:

* This is the first paragraph of the first item.

  And the second paragraph of the first item.

* The second item only has one paragraph.

This is a numbered list:

1. This is the first paragraph of the first item.

   And the second paragraph of the first item.

2. The second item only has one paragraph.

'These quotes should be curly,' and "so should these." There should be a blank line before the next paragraph:

&nbsp;

And then there should be some text ^in\ superscript^ and ~in\ subscript~, and a footnote^[This is a footnote. It should appear at the bottom of the page.] with a star, a footnote[^2] with a dagger, and this should be `monospace`.

[^2]: Another footnote.

## Subsection

Test text test text test text.

> This is a quote block. It should be indented slightly
> and shouldn't contain a line break.
>
> This is a second paragraph in the same quote block.

> | This is a quoted line block. It should be indented slightly
> | and have a *line break* after 'slightly', and **formatting**.

> | \“These literal double curly quotes, used where smart
> | quotes gets it wrong, curl the right way even though
> | they're on different lines.\”

> | \‘These literal single curly quotes, used where smart
> | quotes gets it wrong, curl the right way even though
> | they're on different lines.\’

After this line there should be stars.

* * *

This is a new paragraph after the stars. This text is [Small Caps]{.smallcaps}. Here is a pound sign (£), a euro sign (€), and three letters with accents: ëóû.
