import sys


if __name__ == '__main__':

    f1, f2 = sys.argv[1:]

    with open(f1) as fh1, open(f2) as fh2:
        data1 = list(l.strip() for l in fh1 if l.strip())
        data2 = list(l.strip() for l in fh2 if l.strip())

    exit_code = 0

    # assert lengths match
    if len(data1) != len(data2):
        print('WARNING: Files have different number non-blank lines.')
        exit_code = 1
        sys.exit(exit_code)

    # find different content
    different_content_found = False
    for (i,j) in zip(data1, data2):
        if i != j:
            different_content_found = True
            print('WRONG!')
            print(i)
            print(j)
            print('---')
            exit_code = 1
    if not different_content_found:
        print("No different content was found.")

    sys.exit(exit_code)

