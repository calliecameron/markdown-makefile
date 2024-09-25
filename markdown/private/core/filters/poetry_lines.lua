local lines = 0

function get_lines(elem)
    pandoc.walk_block(pandoc.Div(elem.content), {
        LineBlock = function(elem)
            lines = lines + #elem.content
        end
    })
end

function set_lines(m)
    m["poetry-lines"] = tostring(lines)
    return m
end

return {{BlockQuote = get_lines}, {Meta = set_lines}}
