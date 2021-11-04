
# read textfile into string
with open('syllabled_vectors.txt', 'r',encoding = 'utf-8') as txtfile:
    mytextstring = txtfile.read()

# change text into a binary array
binarray = str.encode(mytextstring)

# save the file
with open('mybin39.bin', 'wb') as binfile:
    binfile.write("adssad")