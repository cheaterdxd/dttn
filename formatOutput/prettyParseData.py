from .prettyAnnounce import log 
def print_Json(json_data:dict):
    print("\n================================================================================")
    for i in list(json_data.keys()):
        log.info(f"{i:<20} - {json_data[i]:>10}")
    print("================================================================================\n")