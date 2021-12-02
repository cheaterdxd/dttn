from .prettyAnnounce import log,bcolors
def print_Json(json_data:dict):
    log.draw_line(64,bcolors.WARNING)
    for i in list(json_data.keys()):
        log.info(f"{i:<20} - {json_data[i]:>10}")
    log.draw_line(64,bcolors.WARNING)