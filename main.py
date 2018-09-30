from collections import defaultdict, namedtuple

TAG = "[%d,%d]"
MIN_LEN =  6 # smallest reoccurance to compress

def compress(original, show_debug = True):

    Match = namedtuple("Match", ["pos", "length"])

    substrings = defaultdict(list) #substring -> [pos]
    matches = {} #reoccurance -> (original_pos, len)

    start = 0
    while start <= len(original) - MIN_LEN:

        step = MIN_LEN
        substring = original[start : start + step]
        longest_match = Match(None, 0)

        for pos in substrings[substring]:

            # can we find a longer substring from this pos
            while pos + step <= start:

                if step > longest_match.length:
                    longest_match = Match(pos, step)

                # check one longer than earlier occurance
                teststring = original[pos : pos + step + 1]
                nextstring = original[start : start + step + 1]

                # add a longer substring of our earlier match
                substrings[teststring].append(pos)

                if nextstring != teststring:
                    break

                step += 1

        if longest_match.pos != None:
            matches[start] = longest_match
            start += longest_match.length 

        else:
            # no match found - add new substring
            substrings[substring].append(start)
            # continue from next char
            start += 1


    index = 0
    result = ""
    
    # rebuild with matches
    while index < len(original):
        if index in matches:
            # TODO: refactor - this dosen't look python - probably a better way
            pos, length = matches[index]
            result += TAG % (pos, length)
            index += length
            continue

        # escape tag indicator from original string
        ch = original[index]
        if ch == "[":
            result += "["

        result += ch
        index += 1

    if show_debug:
        result += "\n\n" + "-" * 37 + "DEBUG" + "-" * 38 + "\n"

        for (index, (pos, length)) in matches.items():
            tag = TAG % (pos, length)

            reoccurance = original[pos : pos + length]
            reoccurance = reoccurance.replace("\n", "\\n")

            result += "%s: %s\n" % (tag, reoccurance)

    return result



def uncompress(compressed_string):
    # TODO: implement
    return compressed_string


def compare(original, compressed):
    return (1 - len(compressed) / len(original)) * 100


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("usage: %s [input_string | -f --file file-name | "
        "-c --compare original compressed | -d --debug]" % sys.argv[0])
        exit(1)

    arg = sys.argv[1]

    # TODO: implement options with argparse
    options = ["-f", "--file", "-c", "--compare"]

    show_debug = "-d" in sys.argv or "--debug" in sys.argv

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
        print(input_string)

    compressed_string = compress(input_string, show_debug)
    print(compressed_string)