insert_sql_all = ""
insert_sql_template = "INSERT INTO TABLE1 (#COLS#) VALUES (#VALS#);"
newRows = [{"selection":"","name":"a","price":"123"},{"selection":"","name":"b","price":"1234"}]
# newRows = eval(str(components.table1.newRows))
for row in newRows:
  col_list = []
  val_list = []
  for col_name, value in row.items():
    if not value.isnumeric():
      value = "'"+value+"'"
    if col_name == 'selection':
      continue
    else:
      col_list.append(col_name)
      val_list.append(value)
  insert_sql = insert_sql_template.replace("#COLS#", ",".join(col_list)).replace("#VALS#",",".join(val_list))+"\n"
  insert_sql_all+=insert_sql
print(insert_sql_all)
