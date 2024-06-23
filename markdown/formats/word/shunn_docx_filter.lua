function Pandoc(doc, meta)
    local pandoc_data_dir = os.getenv('PANDOC_DATA_DIR')

    os.execute("cd " .. pandoc_data_dir .. " && strip-nondeterminism -t zip reference.docx")
end
