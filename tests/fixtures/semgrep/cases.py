"""Static fixtures, never execute this file."""
import os
import subprocess
import pickle
import requests

value = input()
# ruleid: cyber-python-eval-input
eval(value)
# ok: cyber-python-eval-input
eval('1 + 1')

# ruleid: cyber-python-shell-input
os.system(value)
# ruleid: cyber-python-shell-input
subprocess.run(value, shell=True)
# ok: cyber-python-shell-input
subprocess.run(['echo', value], shell=False)

# ruleid: cyber-python-tls-disabled
requests.get('https://example.invalid', verify=False)
# ok: cyber-python-tls-disabled
requests.get('https://example.invalid', verify=True)

# ruleid: cyber-python-pickle-input
pickle.loads(value)
# ok: cyber-python-pickle-input
pickle.loads(b'synthetic fixed bytes')
