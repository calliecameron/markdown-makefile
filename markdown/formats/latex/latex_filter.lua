local suppress_indent = [[
\makeatletter
\@afterindentfalse
\@afterheading
\makeatother
]]

function Div(elem)
    for _, class in ipairs(elem.classes) do
        if class == "firstparagraph" then
            return {
                pandoc.RawBlock("latex", suppress_indent),
                elem,
            }
        end
    end
end

function HorizontalRule(elem)
    return pandoc.RawBlock("latex", "\\begin{center}* * *\\end{center}")
end
