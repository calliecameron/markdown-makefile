function Image(elem)
    return pandoc.Image(elem.caption, '', elem.title, elem.attr)
end
