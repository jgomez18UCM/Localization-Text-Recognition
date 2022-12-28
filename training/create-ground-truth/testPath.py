# Python program to explain os.path.join() method

# importing os module
import os
import pathlib
# Path
path = "/home"
textName = "test"
# Join various path components
result = os.path.join(path, "Desktop") 
print(result)
print(pathlib.Path(result).stem)


if not os.path.exists(result):
    os.mkdir(result)


line = "mimuela"
line_training_text = os.path.join(result, f'{textName}.txt')
with open(line_training_text, 'w') as output_file:
    output_file.writelines([line])
