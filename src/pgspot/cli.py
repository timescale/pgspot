from argparse import ArgumentParser, BooleanOptionalAction
from textwrap import dedent
from .codes import codes
from .state import State, Counter
from .visitors import visit_sql
import sys


def run():
    parser = ArgumentParser(
        description="Spot vulnerabilities in PostgreSQL SQL scripts"
    )
    parser.add_argument(
        "-a",
        "--append",
        dest="append",
        action="store_true",
        default=False,
        help="append files before checking",
    )
    parser.add_argument(
        "--proc-without-search-path",
        metavar="PROC",
        dest="proc_without_search_path",
        action="append",
        default=list(),
        help="whitelist functions without explicit search_path",
    )
    parser.add_argument(
        "--summary-only",
        dest="summary_only",
        action="store_true",
        default=False,
        help="only print number of errors, warnings and unknowns",
    )
    parser.add_argument(
        "--plpgsql",
        action=BooleanOptionalAction,
        default=True,
        help="Analyze PLpgSQL code",
    )
    parser.add_argument(
        "--explain", dest="explain", default=None, help="Describe an error/warning code"
    )
    parser.add_argument(
        "--ignore",
        dest="ignore",
        action="append",
        default=list(),
        type=str,
        help="Ignore error or warning code",
    )
    parser.add_argument(
        "--sql-accepting",
        dest="sql_fn",
        action="append",
        default=list(),
        help="Specify one or more sql-accepting functions",
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        type=str,
        nargs="*",
        help="file to check for vulnerabilities",
    )

    args = parser.parse_args()

    counter = Counter(args)

    if args.files:
        if args.append:
            # treat all files as single unit during processing
            data = "\n".join([open(f).read() for f in args.files])
            visit_sql(State(counter), data, toplevel=True)

        else:
            linebreak = "" if args.summary_only else "\n"
            # process each file individually
            for f in args.files:
                if len(args.files) > 1:
                    print("{}: ".format(f), end=linebreak)
                data = open(f).read()

                file_counter = Counter(args)
                try:
                    visit_sql(State(file_counter), data, toplevel=True)
                except Exception as err:
                    print(linebreak, file_counter, linebreak, err)
                else:
                    print(linebreak, file_counter, linebreak)

                counter.add(file_counter)

            if len(args.files) > 1:
                print("TOTAL:", counter)

    elif args.explain:
        code = args.explain
        if code in codes:
            print(
                "{}: {}\n{}".format(
                    code, codes[code]["title"], dedent(codes[code]["description"])
                )
            )
        else:
            print("Unknown error or warning: {}".format(code))
            sys.exit(1)
        sys.exit(0)

    else:
        # read from stdin
        data = sys.stdin.read()

        visit_sql(State(counter), data, toplevel=True)

        print(counter)

    if not counter.is_clean():
        sys.exit(1)
