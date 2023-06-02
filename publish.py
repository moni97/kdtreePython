import subprocess

# # Step 1: Update version number in setup.py
# new_version = '1.2.3'  # Replace with your desired version number
# with open('setup.py', 'r') as f:
#     setup_lines = f.readlines()
# with open('setup.py', 'w') as f:
#     for line in setup_lines:
#         if line.startswith('version='):
#             f.write(f"version='{new_version}',\n")
#         else:
#             f.write(line)

# Step 2: Build distribution
subprocess.run(['python', 'setup.py', 'sdist', 'bdist_wheel'])

# Step 3: Upload to PyPI using twine
subprocess.run(['twine', 'upload', 'dist/*'])