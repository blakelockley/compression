TAG = "[%d,%d]"
MIN_LEN =  6 # smallest reoccurance to compress


def compress(full_string):

    matches = {}
    limit = len(full_string)

    # find all reoccurances
    for pos in range(limit - (MIN_LEN - 1)):
        substring = full_string[pos : pos + MIN_LEN]

        for test_pos in range(pos + MIN_LEN, limit - (MIN_LEN - 1)):
            test_string = full_string[test_pos : test_pos + MIN_LEN]

            # dont overwrite earlier reoccurances
            if substring == test_string and test_pos not in matches:
                true_len = MIN_LEN

                # TODO: refactor
                while pos + true_len < limit:
                    substring = full_string[pos : pos + true_len]
                    test_string = full_string[test_pos : test_pos + true_len]

                    if substring == test_string:
                        true_len += 1
                    else:
                        break
                    
                matches[test_pos] = (pos, true_len - 1)

    i = 0
    result = ""

    # rebuild with matches
    while i < len(full_string):
        if i in matches:
            pos, length = matches[i]
            result += TAG % (pos, length)
            i += length
            continue

        ch = full_string[i]
        if ch == "[":
            result += "["

        result += ch
        i += 1

    return result


def uncompress(compressed_string):
    return compressed_string


def compare(original, compressed):
    return (1 - len(compressed) / len(original)) * 100


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("usage: %s [input_string | -f --file file-name]" % sys.argv[0])
        exit(1)

    arg = sys.argv[1]
    options = ["-f", "--file", "-c", "--compare"]

    if arg in options:
        if arg == "-f" or arg == "--file":
            with open(sys.argv[2]) as f:
                input_string = f.read()

        elif arg == "-c" or arg == "--compare":
            with open(sys.argv[2]) as f:
                original = f.read()

            with open(sys.argv[3]) as f:
                compressed = f.read()

            ratio = compare(original, compressed)
            print("compression: %.2f%%" %  ratio)
            exit(0)

    else:
        input_string = sys.argv[1]
    
    compressed_string = compress(input_string)
    print(compressed_string)