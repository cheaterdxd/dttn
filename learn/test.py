
av = 'aaaaaa\ cccc'
dest=''
for i in av:
    if(not i.isalnum() and i not in ['_','-','$']):
        dest+= '\\'
    dest+=i

print(dest)