---
author:
- The Author
date: 1 January 2022
docversion: reproducible
lang: en-GB
source-md5: 2518a18c39cbd5e88b46c164d163e14a
subject: "Version: reproducible"
title: Test 4
wordcount: 768
---

-   [The Title](#the-title){#toc-the-title}
-   [The Title](#the-title-1){#toc-the-title-1}
-   [The Title Is ‘Baz’](#the-title-is-baz){#toc-the-title-is-baz}

# The Title

**23 February 2019**

 

This is some text before a section. It shouldn’t be indented.

## This is a section

This is some test text. This is formatted in *italics* and **bold**,
with - various – dashes—, and trailing dots…

‘These quotes should be curly,’ and “so should these.” There should be a
blank line before the next paragraph:

 

And then there should be some text ^in superscript^ and ~in subscript~,
and a footnote[^1] with a star, a footnote[^2] with a dagger, and this
should be `monospace`.

### Subsection

Test text test text test text.

> This is a quote block. It should be indented slightly and shouldn’t
> contain a line break.

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

This is a new paragraph after the stars. This text is [Small
Caps]{.smallcaps}. Here is a pound sign (£), a euro sign (€), and three
letters with accents: ëóû.

# The Title

**23 February 2019**

 

This is some text before a section. It shouldn’t be indented. Each
section should start on a new page (but subsections shouldn’t).

## This is a section {#this-is-a-section}

This is some test text. This is formatted in *italics* and **bold**,
with - various – dashes—, and trailing dots…

‘These quotes should be curly,’ and “so should these.” There should be a
blank line before the next paragraph:

 

And then there should be some text ^in superscript^ and ~in subscript~,
and a footnote[^3] with a star, a footnote[^4] with a dagger, and this
should be `monospace`.

### Subsection {#subsection}

Test text test text test text.

> This is a quote block. It should be indented slightly and shouldn’t
> contain a line break.

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

This is a new paragraph after the stars. This text is [Small
Caps]{.smallcaps}. Here is a pound sign (£), a euro sign (€), and three
letters with accents: ëóû.

## This is a second section

And this is *even more italic text*.

# The Title Is ‘Baz’

**23 February 2019**

 

## This is a section {#this-is-a-section}

This is some test text. This is formatted in *italics* and **bold**,
with - various – dashes—, and trailing dots…

‘These quotes should be curly,’ and “so should these.” There should be a
blank line before the next paragraph:

 

And then we do a simple include:

Text before a section in simple include.

## Section in simple include

> This is a quote block. It should be indented slightly and shouldn’t
> contain a line break.

> | This is a quoted line block. It should be indented slightly
> | and have a *line break* after ‘slightly’, and **formatting**.

Text before recursive include, with *italic*, **bold**, “curly quotes,”
and— an em dash.

Text before section in recursive include.

## Section in recursive include

Text in recursive include, with *italic*, **bold**, “curly quotes,” and—
an em dash.

### Subsection in recursive include

> | “These literal double curly quotes, used where smart
> | quotes gets it wrong, curl the right way even though
> | they’re on different lines.”

> | ‘These literal single curly quotes, used where smart
> | quotes gets it wrong, curl the right way even though
> | they’re on different lines.’

Test text test text test text. After this line there should be stars.

------------------------------------------------------------------------

And then there should be some text ^in superscript^ and ~in subscript~,
and a footnote[^5] with a star, a footnote[^6] with a dagger, and this
should be `monospace`.

Text after recursive include. Here is a pound sign (£), a euro sign (€),
and three letters with accents: ëóû.

## Second section in simple include

Test text.

Text after simple include.

### Subsection {#subsection}

This is a new paragraph. This text is [Small Caps]{.smallcaps}.

## This is a second section {#this-is-a-second-section}

And this is *even more italic text*.

[^1]: This is a footnote. It should appear at the bottom of the page.

[^2]: Another footnote.

[^3]: This is a footnote. It should appear at the bottom of the page.

[^4]: Another footnote.

[^5]: This is a footnote. It should appear at the bottom of the page.

[^6]: Another footnote.
