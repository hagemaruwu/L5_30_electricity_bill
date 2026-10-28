# Identified issues and fixes

Aditya Raj | SRN: PES2UG24CS033

I used the original file at commit `a48c8e9` for the line numbers below. High, Medium and Low are the severity ratings from Bandit.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| B605: shell command injection | Security, High | 61–63 | `os.system` concatenates meter input into a shell command. Shell metacharacters could execute another command. | I replaced the shell command with `HTTPConnection`, validated the address with `ip_address`, added a five-second timeout and status check, and closed the connection in `finally`. |
| B314: unsafe XML parsing | Security, Medium | 18 | Standard ElementTree parsing can expose untrusted input to XML entity attacks. | I used `defusedxml.ElementTree.fromstring` and checked that entity declarations are rejected. |
| B405: unsafe XML parser import | Security, Low | 3 | Bandit flags importing the standard parser for untrusted XML. | I changed the import to defusedxml and included it in `requirements.txt`. |
| B105: hardcoded password | Security, Low | 13 | An unused password literal is stored in source code. | I removed the constant because the program never used it. |
| W0102: mutable default argument | Quality / potential bug | 42 | `extras={}` creates one dictionary shared by calls. The original function does not mutate it, but the default is unsafe for future changes. | I changed the default to `None` and created the dictionary inside the function. |
| W0613: unused argument | Quality | 50 | `currency` is accepted but never read. | I removed the argument and updated the call without changing the output. |
| W1514: unspecified encoding | Portability | 57 | JSON output uses the platform's implicit text encoding. | I added `encoding="utf-8"` when opening the output file. |
| C0103: inconsistent identifiers | Maintainability | 17, 22, 29, 34, 42, 50, 56, 61, 67 | Functions, arguments and local variables use camelCase instead of Python snake_case. | I used snake_case names and updated their uses. I renamed the module-level list to `BILLS`. |
| C0114 / C0116: missing documentation | Maintainability | 1, 17, 22, 29, 42, 50, 56, 61, 66 | The module and its functions have no docstrings. | I added short module and function docstrings. |
| E302: missing blank line | Formatting | 22 | Only one blank line separates top-level function definitions. | I added the missing blank line. |
| E203: whitespace before colon | Formatting | 44 | The dictionary contains `"meter" :`. | I removed the extra space. |
| E501: line too long | Formatting | 72 | A print statement exceeds Flake8's default 79-character limit. | I split the print statement across lines and shortened two docstrings that exceeded the limit. |
| E225: missing operator whitespace | Formatting | 76 | `total=sum(...)` lacks spaces around `=`. | I added spaces: `total = sum(...)`. |

## Other changes

I also made these changes and checked them with tests:

- I added the `if __name__ == "__main__"` guard so importing the module does not run the demo or write a file.
- I cleared the bill collection when starting `main()` so repeated demos do not duplicate bills.
- I kept the original reversed-reading warning and zero-unit behavior, tariff slabs, fixed charge, tax, and extra fee calculation.

## Results

| Check | Before | After |
|---|---|---|
| Pylint | 5.44/10 | 10.00/10 |
| Bandit | 4 findings: 1 High, 1 Medium, 2 Low | 0 findings |
| Flake8 | 4 findings | 0 findings |
| Demo console output | Baseline saved | Exact match |
| Generated bills JSON | Baseline saved | Exact match |
| Regression tests | Not present | 11 tests pass |

I ran the tools on `electricity_bill.py` without disabling any checks. The final Flake8 report is empty because it found no errors.

## Limitations

The meter helper still uses the original HTTP protocol; removing shell injection does not encrypt traffic. It now accepts literal IPv4/IPv6 addresses rather than arbitrary hostnames or shell syntax. I used a mocked meter connection in the tests, not a real meter. The demo still treats reversed readings as zero consumption and overwrites `bills.json`, matching the assignment's original behavior. Clean static analysis is not proof that every possible bug or security weakness has been removed.
