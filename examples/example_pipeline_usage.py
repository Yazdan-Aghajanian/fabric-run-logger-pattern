from logger_interface import log, get_current_timestamp

def run_pipeline():
    log(stage="Init", status="Started", message="Pipeline run started")

    try:
        log(stage="ReadSource", status="Started", message="Reading source data")
        # simulate read
        data = [1,2,3]

        log(stage="Transform", status="Started", message="Applying transformation")
        result = [x * 2 for x in data]

        log(stage="WriteDelta", status="Started", message="Writing to Delta table")
        print("Writing:", result)

        log(stage="Pipeline", status="Succeeded", message="Pipeline completed")

    except Exception as e:
        log(stage="Pipeline", status="Failed", message=str(e))
        raise
