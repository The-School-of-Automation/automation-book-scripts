import os
import re

import PyPDF2

# set up the email search pattern
email_pattern = r"([a-zA-Z][a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-z]{2,5})"
pattern = re.compile(email_pattern)

# define the output file
out_file_name = "extract.csv"
out_file = open(out_file_name, "w")
out_file.write("filename, email\n")

# get all pdf files from current directory
dir_content = os.listdir(".")
pdf_files = [doc for doc in dir_content if doc.endswith("pdf")]
processed = 0

# for each pdf file, read the content
for pdf_file in pdf_files:
    print(f"Extracting email from {pdf_file}...")

    # create a reference to the file and load it using PyPDF2
    pdf_fd = open(pdf_file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_fd)

    num_pages = pdf_reader.numPages
    emails = []

    # check all pages for the email
    for page in range(num_pages):
        page_obj = pdf_reader.getPage(page)
        text = page_obj.extractText()
        text = text.replace("\n", "")

        # search for the email in the text
        email_match = pattern.search(text)

        # add the email to the emails list if not present already
        if email_match is not None:
            email = email_match.group()
            if email not in emails:
                emails.append(email)

    if len(emails) == 0:
        print(f"\t=> Email could be extracted from file {pdf_file}.")

    # close the pdf file descriptor
    pdf_fd.close()

    # write each email in the csv file
    for email in emails:
        out_file.write(f"{pdf_file}, {email}\n")

# close the output file to avoid corruption
out_file.close()