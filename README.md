## Project : Word Alignment

#### Running the program

Before running the program, please ensure that the czenali.gz archive is in the same directory the main.py, requirements.txt files are in. You don't have to extract it since the program does it itself.

__1) Setting up a virtual environment:__
	
```
$ virtuanenv venv
$ source venv/bin/activate
(venv)$ pip3 install -r requirements.txt
```
### Running the program with arguments

#### 1) Run 20 iterations for top 2000 lines, with each word lowercased (and with verbose flag)
```
(venv)$ python3 main.py --verbose --iterations=20 --num_sentences=2000 --lowercase
```
__OR__
```
(venv)$ python3 main.py -v -i=20 -n=2000 -l
```

#### 2) Run the program with default settings (no verbosity, lines used = 2000, iterations = 10)
```
(venv)$ python3 main.py
```

#### 3) Run the program by providing a .gz file in the args
```
(venv)$ python3 main.py --data=czenali.cz --verbose
```

#### 4) Output the results in a file specified in the args
```
(venv)$ python3 main.py --verbose -n=2000 -i=200 --output_file=results.txt
```