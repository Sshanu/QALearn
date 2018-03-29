import sys
import subprocess

sys.path.insert(0, r'pdfminer/tools/')
sys.path.insert(0, r'pdfminer/samples/UG-Manual.pdf')

subprocess.call("./pdf2text.sh")