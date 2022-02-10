def log(text):
    with open("out.log", "a") as log:
        log.write(str(text) + "\n")
