function Div(elem)
    for _, class in ipairs(elem.classes) do
        if class == "nospellcheck" then
            return elem.content
        end
    end
    return nil
end

function Span(elem)
    for _, class in ipairs(elem.classes) do
        if class == "nospellcheck" then
            return elem.content
        end
    end
    return nil
end
