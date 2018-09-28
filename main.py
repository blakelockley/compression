START_BYTE  = '['
END_BYTE    = ']'
MIN_LEN     =  5 # smallest reoccurance to compress


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
            result += "[%d,%d]" % (pos, length)
            i += length
            continue
        
        result += full_string[i]
        i += 1

    return result


def uncompress(compressed_string):
    return compressed_string


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("usage: %s <input_string>" % sys.argv[0])
        exit(1)

    input_string = sys.argv[1]
    compressed_string = compress(input_string)

    print(input_string)
    print(compressed_string)

    ratio = (1 - len(compressed_string) / len(input_string)) * 100
    print("compression: %.2f%%" %  ratio)