import re

def translator(cpp: str) -> str:
    lines = cpp.strip().split('\n')
    py = []
    indent = 0
    tab = "    "

    for l in lines:
        original = l
        line = l.strip()

        if not line:
            py.append("")
            continue

        if line.startswith("#include") or line.startswith("using"):
            continue
        if line.startswith("int main") or line.startswith("return 0"):
            continue

        if line.startswith("}"):
            indent = max(indent - 1, 0)

        open_bracket = "{" in original
        line = line.replace("{", "").replace("}", "").strip()
        if not line:
            continue

        line = line.replace("&&", " and ")
        line = line.replace("||", " or ")

        line = line.replace("true", "True")
        line = line.replace("false", "False")

        if "++" in line:
            line = line.strip().replace("++", "").replace(";", "")
            py.append(tab * indent + f"{line} += 1")
            if open_bracket:
                indent += 1
            continue

        if "--" in line:
            line = line.strip().replace("-", "").replace(";", "")
            py.append(tab * indent + f"{line} -= 1")
            if open_bracket:
                indent += 1
            continue

        if line.startswith("cout"):
            line = line.replace("cout", "").replace(";", "")
            parts = [p.strip() for p in line.split("<<") if p.strip()]
            parts = [p for p in parts if p != "endl"]
            py.append(tab * indent + f"print({', '.join(parts)})")
            if open_bracket:
                indent += 1
            continue

        if line.startswith("if"):
            start = line.find("(")
            end = line.rfind(")")
            condition = line[start+1:end]
            py.append(tab * indent + f"if {condition}:")
            if open_bracket:
                indent += 1
            continue

        if line.startswith("else if"):
            start = line.find("(")
            end = line.rfind(")")
            condition = line[start+1:end]
            py.append(tab * indent + f"elif {condition}:")
            if open_bracket:
                indent += 1
            continue

        if line.startswith("else"):
            py.append(tab * indent + "else:")
            if open_bracket:
                indent += 1
            continue

        if line.startswith("while"):
            start = line.find("(")
            end = line.rfind(")")
            condition = line[start+1:end]
            py.append(tab * indent + f"while {condition}:")
            if open_bracket:
                indent += 1
            continue

        if line == "break;":
            py.append(tab * indent + "break")
            continue

        if line == "continue;":
            py.append(tab * indent + "continue")
            continue

        line = line.replace(";", "")
        for t in ["int", "float", "double", "char", "string", "bool"]:
            line = line.replace(t, "")

        py.append(tab * indent + line.strip())

        if open_bracket:
            indent += 1

    return "\n".join(py)


def main():
    with open("cpp_code.cpp", "r", encoding="utf-8") as f:
        cpp = f.read()
    
    py_res = translator(cpp)

    with open("result.py", "w", encoding="utf-8") as f:
        f.write(py_res)

if __name__ == "__main__":
    main()