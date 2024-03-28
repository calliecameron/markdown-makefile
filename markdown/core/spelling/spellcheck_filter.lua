function Image(elem)
    return pandoc.Image(elem.caption, '', elem.title, elem.attr)
end

function Para(elem)
    if #elem.content == 3 and elem.content[1].tag == "Str" and
       elem.content[1].text == "!include" and elem.content[2].tag == "Space" and
       elem.content[3].tag == "Str" then
        return {}
    end
    return nil
end

function Div(elem)
    for _, class in ipairs(elem.classes) do
        if class == "nospellcheck" then
            return {}
        end
    end
    return nil
end

function Span(elem)
    for _, class in ipairs(elem.classes) do
        if class == "nospellcheck" then
            return {}
        end
    end
    return nil
end
