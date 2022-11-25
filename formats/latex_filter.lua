-- Customise horizontal rules in latex to '* * *'

local rule = "\\begin{center}* * *\\end{center}"

function HorizontalRule (elem)
    return pandoc.RawBlock("latex", rule)
end
