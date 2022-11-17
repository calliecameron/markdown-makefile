function Str(elem)
    if elem.text:find("'") or elem.text:find("\"") then
        print("ERROR: Markdown validation failed: found quotes that weren't converted to smart quotes. Replace them with backslash-escaped literal curly quotes (“ ” ‘ ’).")
        os.exit(1)
    end
end
