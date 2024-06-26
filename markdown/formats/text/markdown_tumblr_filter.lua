function HorizontalRule(elem)
    return pandoc.Para({
        pandoc.Str("&#x002a;"),
        pandoc.Space(),
        pandoc.Str("&#x002a;"),
        pandoc.Space(),
        pandoc.Str("&#x002a;")})
end

function Str(elem)
    return pandoc.Str(string.gsub(string.gsub(elem.text, "<", "&lt;"), ">", "&gt;"))
end
