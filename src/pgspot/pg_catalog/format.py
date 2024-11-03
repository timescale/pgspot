import re

# https://www.postgresql.org/docs/current/functions-string.html#FUNCTIONS-STRING-FORMAT
#
# Format specifiers are introduced by a % character and have the form
#
# %[position][flags][width]type
# where the component fields are:
#
# position (optional)
# A string of the form n$ where n is the index of the argument to print.
# Index 1 means the first argument after formatstr. If the position is
# omitted, the default is to use the next argument in sequence.
#
# flags (optional)
# Additional options controlling how the format specifier's output is formatted.
# Currently the only supported flag is a minus sign (-) which will cause the
# format specifier's output to be left-justified. This has no effect unless the
# width field is also specified.
#
# width (optional)
# Specifies the minimum number of characters to use to display the format
# specifier's output. The output is padded on the left or right (depending on
# the - flag) with spaces as needed to fill the width. A too-small width does
# not cause truncation of the output, but is simply ignored. The width may be
# specified using any of the following: a positive integer; an asterisk (*) to
# use the next function argument as the width; or a string of the form *n$ to
# use the nth function argument as the width.
#
# If the width comes from a function argument, that argument is consumed before
# the argument that is used for the format specifier's value. If the width
# argument is negative, the result is left aligned (as if the - flag had been
# specified) within a field of length abs(width).
#
# type (required)
# The type of format conversion to use to produce the format specifier's output.
# The following types are supported:
# s formats the argument value as a simple string. A null value is treated as
#   an empty string.
# I treats the argument value as an SQL identifier, double-quoting it if
#   necessary. It is an error for the value to be null (equivalent to quote_ident).
# L quotes the argument value as an SQL literal. A null value is displayed as
#   the string NULL, without quotes (equivalent to quote_nullable).
#
# In addition to the format specifiers described above, the special sequence %%
# may be used to output a literal % character.


def parse_format_string(fmt_string):
    ret = []
    current_index = 1
    for i in re.findall(
        r"(%(([1-9])$)?[-]?([1-9][0-9]*|[*]|[*][1-9]$)?([sIL]))", fmt_string
    ):
        # i[0] is the full match
        # i[1] is the position specifier
        # i[2] is the position specifier index
        # i[3] is the width specifier
        # i[4] is the type specifier
        if i[2]:
            ret.append((i[4], int(i[2])))
        else:
            # width may consume a function argument
            if i[3] == "*":
                current_index += 1
            ret.append((i[4], current_index))
            current_index += 1

    return ret
