local starts_with_text = ""

function unwrap(elem)
    return elem.content
end

function get_starts_with_text(doc)
    doc = doc:walk({Div = unwrap})
    if #doc.blocks > 0 and doc.blocks[1].tag ~= "Header" then
        starts_with_text = "t"
    end
end

function set_starts_with_text(meta)
    meta["starts-with-text"] = starts_with_text
    return meta
end

return {{Pandoc = get_starts_with_text}, {Meta = set_starts_with_text}}
