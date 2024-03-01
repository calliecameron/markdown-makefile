local starts_with_text = ""

function get_starts_with_text(doc)
    if #doc.blocks > 0 and doc.blocks[1].t ~= "Header" then
        starts_with_text = "t"
    end
end

function set_starts_with_text(meta)
    meta["starts-with-text"] = starts_with_text
    return meta
end

return {{Pandoc = get_starts_with_text}, {Meta = set_starts_with_text}}
