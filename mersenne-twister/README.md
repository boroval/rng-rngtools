## Pseudorandom number generator [![Build Status](https://travis-ci.org/boo1ean/mersenne-twister.png?branch=master)](https://travis-ci.org/boo1ean/mersenne-twister)

Mersenne Twister pseudorandom number generator.

[Origin source](https://gist.github.com/banksean/300494) (generator interface was changed)

Algorithm - http://en.wikipedia.org/wiki/Mersenne_twister

## Installation

    $ npm install mersenne-twister

## Usage

```javascript
var MersenneTwister = require('mersenne-twister');
var generator = new MersenneTwister();

// Generates a random number on [0,1) real interval (same interval as Math.random)
generator.random();

// [0, 4294967295]
generator.random_int();

// [0,1]
generator.random_incl();

// (0,1)
generator.random_excl();

// [0,1) with 53-bit resolution
generator.random_long();

// [0, 2147483647]
generator.random_int31();
```

## Seeding

If you want to use a specific seed in order to get a repeatable random sequence, pass an integer into the constructor:

```javascript
var generator = new MersenneTwister(123);
``` 

and that will always produce the same random sequence.

Also you can do it on existing generator instance:

```javascript
generator.init_seed(123);
```

## License

See source



COMANDS TO RNGtools:

python rng_tool.py -rw -n 15000000000 -f file01.bin -sf file01.sf
node rngtool.js -rw -n 15000000000 -f file01.bin -sf file01.sf

python rng_tool.py -rw -s 0xFFFFFFFF -n 1000000 -f file02.bin
node rng_tool.py -rw -s 0xFFFFFFFF -n 1000000 -f file02.bin

python rng_tool.py -rw aes -r 90 -n 100000 -f file03.txt
node rng_tool.py -r 90 -n 100000 -f file03.txt
