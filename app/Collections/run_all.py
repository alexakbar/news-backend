import subprocess

# List file python 
python_files = ['app/Collections/add_categories.py', 'app/Collections/add_news.py']

# loop file python
for file in python_files:
    try:
        result = subprocess.run(['python3', file], capture_output=True, text=True)
        output = result.stdout
        error = result.stderr
        
        # show output
        print(f"Output from {file}:")
        print(output)
        
        # show error
        if error:
            print(f"Error from {file}:")
            print(error)
        
    except subprocess.CalledProcessError as e:
        print(f"Something Wrong {file}:")
        print(e)