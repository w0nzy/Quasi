# hello
test = "123"
def is_exist(name: str) -> bool:
    print(globals()[name])
def is_after(line: str,index = 2 ) -> str:
    line = line.split(" ")[index:]
    if line != []:
        return " ".join(line)
    return ""

if __name__ == "__main__": pass
