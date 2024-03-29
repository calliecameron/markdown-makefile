function CodeBlock(elem)
    return {}
end

function Div(elem)
    for _, class in ipairs(elem.classes) do
        if class == "nospellcheck" then
            return {}
        end
    end
    return elem.content
end

function Figure(elem)
    return pandoc.Figure(elem.content, elem.caption, {})
end

function Header(elem)
    return pandoc.Header(elem.level, elem.content, {})
end

function Para(elem)
    if #elem.content == 3 and elem.content[1].tag == "Str" and
       elem.content[1].text == "!include" and elem.content[2].tag == "Space" and
       elem.content[3].tag == "Str" then
        return {}
    end
    return nil
end

function Code(elem)
    return {}
end

function Image(elem)
    return pandoc.Image(elem.caption, "", elem.title, {})
end

function Link(elem)
    if pandoc.utils.stringify(elem.content) == elem.target then
        return {}
    end
    return pandoc.Link(elem.content, "", elem.title, {})
end

function SmallCaps(elem)
    return elem.content
end

function Span(elem)
    for _, class in ipairs(elem.classes) do
        if class == "nospellcheck" then
            return {}
        end
    end
    return elem.content
end
