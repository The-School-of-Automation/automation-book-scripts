import os

# to be replaced string and file extension filter
search = "file"
replace = "document"
type_filter = ".py"

# get all files from current directory
dir_content = os.listdir('.')
docs = [doc for doc in dir_content if os.path.isfile(doc)]
renamed = 0

print(f"{len(docs)} of {len(dir_content)} elements are files.")

# go through all the files and check if they match the search pattern
for doc in docs:
    # separate name from file extension
    doc_name, filetype = os.path.splitext(doc)

    # filter for files with the right extension
    if filetype == type_filter:
        # check if search text is in doc name
        if search in doc_name:
            
            #replace with the given text
            new_name = doc_name.replace(search, replace) + filetype
            os.rename(doc, new_name)
            renamed += 1

            print(f"Renamed file {doc} to {new_name}")

print(f"Renamed {renamed} of {len(docs)} files.")