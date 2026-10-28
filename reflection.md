# Reflection

The handout mentions reflection questions but does not list them. These are my notes on the analysis and changes made in this lab.

## Findings

I used Pylint to check code quality, Bandit to check security issues, and Flake8 to check formatting. The initial Pylint score was 5.44/10. Bandit reported four issues, and Flake8 reported four formatting errors.

The main security issue was in `syncMeter()`. It added the meter address directly to an `os.system()` command, so input containing shell commands could be executed. Bandit also flagged the XML parser and an unused hardcoded password.

## Changes

I addressed the High and Medium severity Bandit findings first. I replaced the shell command with `HTTPConnection` and used `ip_address()` to validate the meter address. I changed the XML parser to defusedxml and removed the unused password.

For Pylint, I changed the mutable default `extras={}` to `extras=None`, removed the unused currency argument, added docstrings, used snake_case names, and specified UTF-8 when saving the JSON file. I also corrected the blank lines, spacing and long lines reported by Flake8.

## Checking the results

I compared the output before and after the changes. The bill amounts stayed the same: M1 was 708.75, M2 was 2661.75, M3 was 78.75, and M4 was 288.75. The total was still 3738.0, and the saved JSON matched the original.

The final Pylint score was 10.00/10. Bandit and Flake8 reported no issues in `electricity_bill.py`. All 11 tests passed, including checks for tariff slabs, extra fees, JSON output, invalid meter addresses and XML entities. The meter connection was mocked in the tests; I did not test it against a real meter.

## Limitations

Passing these tools does not prove that the program has no bugs. The meter helper still uses HTTP, so its traffic is not encrypted. Reversed readings are still treated as zero units, as in the original program. Static analysis needs to be used along with testing and a review of the program's requirements.
