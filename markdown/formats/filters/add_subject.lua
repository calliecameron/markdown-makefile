function Meta(meta)
    if meta["version"] then
        meta["subject"] = "Version: " .. pandoc.utils.stringify(meta["version"])
    end
    return meta
end
