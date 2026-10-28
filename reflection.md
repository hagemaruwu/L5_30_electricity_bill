# Reflection notes

The repository README asks for answers to four reflection questions from the handout. However, the supplied three-page handout mentions reflection answers without listing any questions. The notes below describe the completed work; they are not presented as answers to missing official questions. Replace or organize them under the actual questions if the instructor supplies them.

## What the tools found

Pylint identified quality problems including the shared dictionary default, an unused argument, missing docstrings, inconsistent names, and an unspecified file encoding. Flake8 identified spacing, blank-line and line-length violations. Bandit found the most urgent issue: meter input was concatenated into an `os.system` command. It also flagged standard XML parsing and an unused hardcoded password.

## Why the security fixes came first

The shell-command issue had High severity and the XML parser call had Medium severity in the original Bandit report. Replacing shell execution with a direct HTTP client removed command interpretation, and validating the IP address rejects shell syntax before a connection is created. Using defusedxml protects the parser against XML entity attacks. The unused password was removed rather than moved elsewhere because the demo never used it.

## How behavior was checked

The original console output and `bills.json` were saved before editing. Both match the final program exactly. M1 is billed 708.75, M2 2661.75, M3 78.75, and M4 288.75; the total remains 3738.0. Eleven regression tests cover slab boundaries, readings, extra fees, JSON saving, repeated runs, XML entity rejection, invalid meter input, and mocked HTTP success and failure cleanup.

## What static analysis cannot establish

The final Pylint score is 10.00/10, and Bandit and Flake8 report no findings for the assigned script. Those results show that the tools' checks pass, not that the entire application is production-ready. For example, HTTP traffic is still unencrypted, reversed readings are still treated as zero consumption, and live meter communication was not tested. Runtime checks and tests are still needed alongside static analysis.
