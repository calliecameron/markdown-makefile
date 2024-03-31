function Div(elem)
    for _, class in ipairs(elem.classes) do
        if class == "collectionseparator" then
            return {}
        end
    end
end
