function has_nospellcheck(elem)
    for _, class in ipairs(elem.classes) do
        if class == "nospellcheck" then
            return true
        end
    end
    return false
end

function forbid_nospellcheck(elem)
    if has_nospellcheck(elem) then
        io.stderr:write("The 'nospellcheck' class is only allowed on divs and span; found on type '" .. elem.tag .. "'\n")
        os.exit(1)
    end
end

function CodeBlock(elem)
    forbid_nospellcheck(elem)
    return {}
end

function Div(elem)
    if has_nospellcheck(elem) then
        return {}
    end
    return elem.content
end

function Figure(elem)
    forbid_nospellcheck(elem)
    return pandoc.Figure(elem.content, elem.caption, {})
end

function Header(elem)
    forbid_nospellcheck(elem)
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

function Table(elem)
    forbid_nospellcheck(elem)
end

function Code(elem)
    forbid_nospellcheck(elem)
    return {}
end

function Image(elem)
    forbid_nospellcheck(elem)
    return pandoc.Image(elem.caption, "", elem.title, {})
end

function Link(elem)
    forbid_nospellcheck(elem)
    if pandoc.utils.stringify(elem.content) == elem.target then
        return {}
    end
    return pandoc.Link(elem.content, "", elem.title, {})
end

function SmallCaps(elem)
    return elem.content
end

function Span(elem)
    if has_nospellcheck(elem) then
        return {}
    end
    return elem.content
end
