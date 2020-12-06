# Horta.py


Horta is a python program designed to generate pseudo random growing flower patterns in a terminal window. It was made in 2020 by Lucas Bet as part of the CS50x Harvard Program.

<img src="https://imgur.com/a/S1eVbCz"/>


## Installation

Use your preferred package manager, then [pip](https://pip.pypa.io/en/stable/), to install the dependencies.

```bash
sudo apt install python3
pip3 install mmh3
pip3 install textwrap
pip3 install cursor
```

Then dowload the distribution code above and follow the usage guide.

## Usage

```python
cd "program_directory"
python3 ./horta.py "seed" "size"
```
Horta takes as input directly from the command line a seed and a size.

A seed can be any text, number or symbol, but it cannot contain blank spaces.

The size should be "small", "medium", "large" or "auto". As suggested, "auto" will detect the size of the terminal window. The program can be run without a size argument, in which case the default size will be set to "small".

The program will stop alone after a few thousand iterations determined by size or if you press CTRL+C. In both cases, a message will print out your discoveries and points for that particular seed.


## Contributing
The project is not taking contributions by now, sorry.

As more features are added in, this will be updated. Thank you.

## License
[MIT](https://choosealicense.com/licenses/mit/)
