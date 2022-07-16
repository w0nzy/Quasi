# hello
import os

def is_after(line: str,index = 2 ) -> str:
    line = line.split(" ")[index:]
    if line != []:
        return " ".join(line)
    return ""
def get_framework_dir() -> str:
    return os.path.dirname(os.path.dirname(__file__))
if __name__ == "__main__": pass
