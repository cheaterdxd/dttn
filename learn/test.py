def findext():
    import glob
    list_f_response = glob.glob('/home/cheaterdxd/dttn/*',recursive=True)
    for f in list_f_response:
        print(f)
findext()