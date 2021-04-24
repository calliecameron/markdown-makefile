-- counts words in a document
-- modified from https://pandoc.org/lua-filters.html#examples

local words = 0

local wordcount = {
  Str = function(el)
    -- we don't count a word if it's entirely punctuation
    if el.text:match("%P") then
      words = words + 1
    end
  end,

  Code = function(el)
    _,n = el.text:gsub("%S+","")
    words = words + n
  end,

  CodeBlock = function(el)
    _,n = el.text:gsub("%S+","")
    words = words + n
  end
}

function get_wordcount(doc, meta)
  -- skip metadata, just count body
  pandoc.walk_block(pandoc.Div(doc.blocks), wordcount)
end

function set_wordcount(m)
  if m.wordcount == nil then
    m.wordcount = tostring(words)
    return m
  end
end

return {{Pandoc = get_wordcount}, {Meta = set_wordcount}}
