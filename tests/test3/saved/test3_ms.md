---
author:
- The Author
author_lastname: Author
contact_address: "`\\n`{=tex}"
contact_city_state_zip: "`\\n`{=tex}"
contact_email: "`\\n`{=tex}"
contact_name: The Author
contact_phone: "`\\n`{=tex}"
date: 23 February 2019
docversion: "d824205-dirty, Sun Apr 11 18:00:41 2021 +0200"
lang: en-GB
short_title: "The Title Is 'Baz'"
subject: "Version: d824205-dirty, Sun Apr 11 18:00:41 2021 +0200"
title: "The Title Is 'Baz'"
---

# This is a section

This is some test text. This is formatted in *italics* and **bold**,
with - various -- dashes---, and trailing dots...

'These quotes should be curly,' and "so should these." There should be a
blank line before the next paragraph:

 

And then we do a simple include:

Text before a section in simple include.

# Section in simple include

> This is a quote block. It should be indented slightly and shouldn't
> contain a line break.

> | This is a quoted line block. It should be indented slightly
> | and have a *line break* after 'slightly', and **formatting**.

Text before recursive include, with *italic*, **bold**, "curly quotes,"
and--- an em dash.

Text before section in recursive include.

# Section in recursive include

Text in recursive include, with *italic*, **bold**, "curly quotes,"
and--- an em dash.

## Subsection in recursive include

> | “These literal double curly quotes, used where smart
> | quotes gets it wrong, curl the right way even though
> | they're on different lines.”

> | ‘These literal single curly quotes, used where smart
> | quotes gets it wrong, curl the right way even though
> | they're on different lines.’

Test text test text test text. After this line there should be stars.

------------------------------------------------------------------------

And then there should be some text ^in superscript^ and ~in subscript~,
and a footnote[^1] with a star, a footnote[^2] with a dagger, and this
should be `monospace`.

Text after recursive include. Here is a pound sign (£), a euro sign (€),
and three letters with accents: ëóû.

# Second section in simple include

Test text.

Text after simple include.

## Subsection

This is a new paragraph. This text is [Small Caps]{.smallcaps}.

# This is a second section

And this is *even more italic text*.

[^1]: This is a footnote. It should appear at the bottom of the page.

[^2]: Another footnote.
