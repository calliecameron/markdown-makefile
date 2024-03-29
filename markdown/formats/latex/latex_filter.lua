local remove_indent = [[
\makeatletter
\@afterindentfalse
\@afterheading
\makeatother
]]

function HorizontalRule(elem)
    return {
        pandoc.RawBlock("latex", "\\begin{center}* * *\\end{center}"),
        pandoc.RawBlock("latex", remove_indent),
    }
end

function Para(elem)
    -- paragraph containing only &npsb;
    if #elem.content == 1 and elem.content[1].tag == "Str" and
       elem.content[1].text == "\u{A0}" then
        return {
            elem,
            pandoc.RawBlock("latex", remove_indent),
        }
    end
end
