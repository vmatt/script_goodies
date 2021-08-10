def get_path(filename):
    return os.path.normpath(os.path.dirname(os.path.realpath(__file__))) + '/' + filename
  
# Sets

def is_it_in(source,target, both_check=None):
    only_source={}
    on_both={}
    for row in source:
        if row not in target:
            only_source[row] = source[row]
        if row in target and both_check is not None:
            on_both[row] = source[row]
    return only_source, on_both
  
  # Openpyxl goodies
  
  def set_sheet_width(sh):
    for column_cells in sh.columns:
        length = max(len(as_text(cell.value)) for cell in column_cells)
        sh.column_dimensions[str(column_cells[0].column_letter)].width = length
    return sh
