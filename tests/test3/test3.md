---
title: The Title Is 'Baz'
author:
- An Author
date: 23 February 2019 baz
identifier:
- scheme: DOI
  text: doi:10.234234.234/33
publications:
- venue: Baz
  self-published: 2022-12-12
---

# This is a section

This is some test text. This is formatted in *italics* and **bold**, with - various -- dashes---, and trailing dots...

'These quotes should be curly,' and "so should these." There should be a blank line before the next paragraph:

&nbsp;

And then we do a simple include:

!include include1

Text after simple include.

## Subsection

This is a new paragraph. This text is [Small Caps]{.smallcaps}.

# This is a second section {#quux-not-spellchecked}

And this is *even more italic text*. Foo.

```python
# Code blocks aren't spellchecked: quux
```

Inline code isn't spellchecked: `quux`.

::: quux
`div` classes aren't spellchecked.
:::

::: nospellcheck
Anything in a nospellcheck div isn't spellchecked: quux.
:::

Automatic links aren't spellchecked: <http://quux.com>. Neither are the targets or attributes of inline links: [Foo](http://quux.com "Foo"){.quux}. Neither are [span classes]{.quux}. Anything in a [nospellcheck span]{.nospellcheck} isn't spellchecked.
