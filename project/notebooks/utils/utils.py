
def drop_file_from_path(path: str) -> None:
    dbutils.fs.rm(dbutils.fs.ls(path)[0].path)