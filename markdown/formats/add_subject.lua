function Meta(meta)
    if meta["docversion"] then
        meta["subject"] = "Version: " .. pandoc.utils.stringify(meta["docversion"])
    end
    return meta
end
