function Pandoc(doc, meta)
  local pandoc_data_dir = os.getenv('PANDOC_DATA_DIR')
  local source_date_epoch = os.getenv('SOURCE_DATE_EPOCH')

  if source_date_epoch ~= nil then
    os.execute("cd " .. pandoc_data_dir .. " && strip-nondeterminism -t zip -T " .. source_date_epoch .. " reference.docx")
  end
end
