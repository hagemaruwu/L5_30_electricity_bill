# Reflection Questions and Answers

Aditya Raj | SRN: PES2UG24CS033

Questions generated with AI as permitted by the instructor; answers are based on this lab.

## 1. What is the purpose of Pylint, Bandit and Flake8, and what did they find in this program?

I used Pylint to check code quality, Bandit to check security issues, and Flake8 to check formatting. Pylint flagged problems such as the mutable default argument, unused currency argument, missing docstrings and inconsistent names. Bandit found four security issues involving shell execution, XML parsing and a hardcoded password. Flake8 found four formatting errors involving spacing, blank lines and line length.

## 2. Which issues did you fix first, and how did you fix them?

I fixed the High and Medium severity Bandit findings first. The original `syncMeter()` added user input directly to an `os.system()` command, which could allow command injection. I replaced it with `HTTPConnection` and validated the address using `ip_address()`. I also replaced the standard XML parser with defusedxml and removed the unused hardcoded password. These changes addressed all four Bandit findings.

## 3. What code-quality and formatting changes did you make, and how did you check that the program still worked?

I changed `extras={}` to `extras=None` and created the dictionary inside the function. I removed the unused currency argument, used snake_case names, added docstrings and specified UTF-8 for JSON output. I corrected the spacing, blank lines and long lines reported by Flake8.

I compared the program output and saved JSON before and after the changes. Both matched. The amounts remained 708.75 for M1, 2661.75 for M2, 78.75 for M3 and 288.75 for M4, giving a total of 3738.0. All 11 regression tests passed. The final Pylint score was 10.00/10, and Bandit and Flake8 reported no issues in the assigned script.

## 4. Can static analysis guarantee that a program is correct and secure?

No. Static analysis checks source code for known patterns, but it cannot confirm every runtime behavior or business rule. For example, the meter helper still uses unencrypted HTTP, and reversed readings are still treated as zero units. The meter connection was mocked in the tests, so I did not verify communication with a real meter. Static analysis should be combined with testing and a review of the requirements.
