from .prettyAnnounce import log,bcolors
def print_Json(json_data:dict):
    print(f"\n{bcolors.WARNING}================================================================================{bcolors.ENDC}")
    for i in list(json_data.keys()):
        log.info(f"{i:<20} - {json_data[i]:>10}")
    print(f"{bcolors.WARNING}================================================================================{bcolors.ENDC}\n")