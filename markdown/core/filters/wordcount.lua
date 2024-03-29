-- counts words in a document
-- modified from https://pandoc.org/lua-filters.html#examples

local words = 0

local wordcount = {
  Str = function(elem)
    -- we don't count a word if it's entirely punctuation
    if elem.text:match("%P") then
      words = words + 1
    end
  end,

  Code = function(elem)
    _,n = elem.text:gsub("%S+","")
    words = words + n
  end,

  CodeBlock = function(elem)
    _,n = elem.text:gsub("%S+","")
    words = words + n
  end
}

function get_wordcount(doc, meta)
  -- skip metadata, just count body
  pandoc.walk_block(pandoc.Div(doc.blocks), wordcount)
end

function set_wordcount(meta)
  if meta.wordcount == nil then
    meta.wordcount = tostring(words)
    return meta
  end
end

return {{Pandoc = get_wordcount}, {Meta = set_wordcount}}
