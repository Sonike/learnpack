# How computers run code

## Why this matters

Every bug you will ever chase happens inside a machine that does exactly what it is told, very fast, with no idea what you *meant*. When a program forgets everything after a crash, when a file of "plain text" shows garbage like `cafÃ©`, or when someone asks "is Python compiled or interpreted?" in an interview, the answer comes from the ideas in this lesson. You don't need to build a computer. You need a clear picture of what happens between pressing **Run** and seeing output.

## The three parts that matter: CPU, memory and storage

Strip away the case, the fans and the lights, and a computer has three parts you'll think about as a programmer.

```
   ┌──────────────┐   reads/writes    ┌──────────────────┐   loads/saves   ┌────────────────────┐
   │     CPU      │ ◄───────────────► │   Memory (RAM)   │ ◄─────────────► │ Storage (SSD/disk) │
   │ does the work│    nanoseconds    │ fast, temporary  │  microseconds+  │ slow, permanent    │
   └──────────────┘                   └──────────────────┘                 └────────────────────┘
```

- **CPU** (central processing unit): the part that actually *does* things. It runs very simple **instructions**, one after another: add these two numbers, copy this value, compare these, jump to that instruction if the comparison was true. A modern CPU runs billions of them per second. Everything a program does, from showing a web page to training a model, is built out of these tiny steps.
- **Memory**, also called **RAM** (random-access memory): the CPU's workbench. While a program runs, its instructions and its data (your variables, the list you're sorting, the text you're editing) live here. RAM is fast but **volatile**: when the power goes off, everything in it is gone.
- **Storage** (an SSD or hard disk): the filing cabinet. Files, installed programs and photos live here and survive a restart. It's much slower than RAM, so a program copies what it needs from storage into memory before working on it.

This explains a feeling you've already had. You type for an hour, the laptop dies, and the work is lost: it was only in RAM. Pressing **Save** copies it to storage. Programs work the same way: a variable in your Python program lives in memory and disappears when the program ends, unless you write it to a file (or a database, later in the course).

> **Note:** "Memory" in programming almost always means RAM, not storage. When someone says "this program uses 2 GB of memory", they mean RAM.

## Bits and bytes: everything is numbers

Inside the machine, memory and storage hold only one kind of thing: **bits**. A bit is a single 0 or 1, physically an electrical charge that is either there or not. Eight bits make a **byte**, the unit you see in file sizes (a kilobyte is about a thousand bytes, a megabyte about a million, a gigabyte about a billion).

With one bit you can tell two things apart: 0 or 1. With two bits, four: `00`, `01`, `10`, `11`. Every extra bit doubles the count, so `n` bits can hold `2ⁿ` different values.

```
bits   different values
1      2
2      4
8      256        (one byte: 0 to 255)
16     65,536
64     18,446,744,073,709,551,616
```

### Counting in binary

We count in **decimal** (base 10): ten digits, and each position is worth ten times the one to its right. `305` means 3 hundreds + 0 tens + 5 ones.

**Binary** (base 2) works the same way with two digits. Each position is worth twice the one to its right: 1, 2, 4, 8, 16, …

```
binary 1101
        │││└─ 1 × 1  =  1
        ││└── 0 × 2  =  0
        │└─── 1 × 4  =  4
        └──── 1 × 8  =  8
                       ──
                       13
```

Python can show you both directions:

```python
print(bin(13))          # 0b1101   (the 0b prefix means "binary")
print(int("1101", 2))   # 13
print(2 ** 8)           # 256      (values that fit in one byte)
```

To go from a number to binary by hand, divide by 2 over and over and write down the remainders. They come out last digit first:

```
13 ÷ 2 = 6 remainder 1   ← last digit
 6 ÷ 2 = 3 remainder 0
 3 ÷ 2 = 1 remainder 1
 1 ÷ 2 = 0 remainder 1   ← first digit
read upwards: 1101
```

That's an **algorithm**: a precise, step-by-step method that always works. You'll turn exactly this one into code in the first exercise.

> **Try it:** in the practice editor, run `print(bin(255), bin(256))`. Why does 256 need one more digit than 255?

## How text becomes numbers

If memory only holds numbers, how does it store the word `Hi`? By agreement. Everyone agrees on a table that gives each character a number, called its **code point**.

The first widely used table was **ASCII** (1960s): 128 characters covering English letters, digits, punctuation and a few control codes. `A` is 65, `a` is 97, a space is 32. Python's `ord()` gives you a character's number and `chr()` goes back:

```python
print(ord("A"))   # 65
print(ord("a"))   # 97
print(chr(72), chr(105))   # H i
```

128 characters is nowhere near enough for the world's languages, so today's standard is **Unicode**: one table with code points for over 150,000 characters, including every script in use, maths symbols and emoji. ASCII's 128 characters keep their old numbers, so `A` is still 65.

```python
print(ord("é"))    # 233
print(ord("🙂"))   # 128578
```

### UTF-8: turning code points into bytes

A code point like 128578 doesn't fit in one byte (0–255). An **encoding** is the rule for turning code points into bytes. The one you will meet almost everywhere (web pages, files, APIs) is **UTF-8**:

- ASCII characters take 1 byte, the same byte as in ASCII.
- Accented Latin letters, Greek, Arabic, Hebrew and similar take 2 bytes.
- Most Chinese, Japanese and Korean characters take 3 bytes.
- Emoji and rarer characters take 4 bytes.

In Python, a `str` is text (a sequence of characters). `.encode("utf-8")` turns it into `bytes`, the raw numbers that would be stored or sent:

```python
word = "café"
data = word.encode("utf-8")
print(len(word))    # 4   characters
print(len(data))    # 5   bytes: é takes two
print(list(data))   # [99, 97, 102, 195, 169]
print(len("🙂".encode("utf-8")))   # 4
```

That's why "how long is this text?" has two honest answers: characters (what a person counts) and bytes (what the disk or network counts). A database column limited to 255 *bytes* can hold fewer than 255 Chinese characters.

When the reader uses a different encoding from the writer, you get **mojibake**: `café` written as UTF-8 but read as an older Western encoding shows up as `cafÃ©`. The two bytes of `é` (195 and 169) are read as two separate characters. When you see that, think "encoding mismatch", not "corrupted file".

## What a program is

A **program** is a list of instructions for the CPU, stored as a file. The CPU only understands its own **machine code**: instructions encoded as bytes, different for different CPU families (the chip in most Windows laptops speaks a different machine code from the chip in a recent Mac or a phone). Nobody writes machine code by hand any more. We write **source code** in a programming language that people can read:

```python
total = 2 + 3
print(total)   # 5
```

Something has to translate that into steps the CPU can run. There are two broad approaches.

### Compiled vs interpreted

- A **compiler** translates the whole program ahead of time into machine code and saves it as a separate file you can run directly. C, C++, Rust and Go work like this. You compile once; the result runs fast, but only on the kind of machine it was compiled for.
- An **interpreter** is itself a program that reads your code and carries it out as it goes, without producing a machine-code file. You run the interpreter and hand it your source code.

### So which is Python?

Both, in a way, and this is a classic interview question. When you run `python3 hello.py`:

1. The Python interpreter (a program, itself written in C, called **CPython**) reads your source file.
2. It **compiles** your code into **bytecode**: a simpler set of instructions designed for Python, not for any real CPU.
3. A part of the interpreter called the **Python virtual machine** then **interprets** that bytecode, one instruction at a time, doing the real work on the CPU.

```
hello.py  ──compile──►  bytecode  ──interpret──►  CPU does the work
(source)                (for Python's virtual machine)
```

You can peek at the bytecode with the standard library's `dis` module:

```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
# Prints lines like:
#   LOAD_FAST   a
#   LOAD_FAST   b
#   BINARY_OP   + (add)
#   RETURN_VALUE
# (the exact names and layout change between Python versions)
```

So the precise answer is: **Python is compiled to bytecode, and that bytecode is interpreted.** In everyday speech people call Python "interpreted", because you never run a separate compile step yourself. You may also see `__pycache__` folders with `.pyc` files appear next to your code: that's Python saving bytecode so it doesn't have to recompile unchanged files next time.

This design is why Python is easy to start with (no build step, runs anywhere Python is installed) and slower than C for heavy number crunching (each bytecode instruction costs many machine instructions). For most software, the time you save writing it matters far more.

### What happens, line by line

The interpreter runs your file **from top to bottom**, one statement at a time. Each line can change what's in memory, and later lines see those changes:

```python
price = 4        # memory now holds a name "price" pointing at 4
price = price * 2   # read 4, multiply, store 8 under "price"
print(price)     # 8
```

If a line fails, Python stops there and prints an **error message** (a "traceback"). Lines after it never run. Python Tutor, linked below, draws memory step by step as each line runs; use it whenever a program surprises you.

## Common mistakes

**Confusing memory with storage.** "I set the variable, why is it gone when I run the program again?" Variables live in RAM for one run. To keep data between runs, save it to a file.

**Thinking a text file is "just text".** Every text file is bytes plus an encoding. If you open a file and get an error like this:

```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 3: invalid continuation byte
```

read it left to right: Python tried to decode (bytes → text) as UTF-8, and byte `0xe9` (233, a hexadecimal number) at position 3 isn't valid UTF-8. The file was saved in a different encoding. The fix is to open it with the right one, not to delete characters.

**Mixing up characters and bytes.** `len("日本")` is 2, but it takes 6 bytes in UTF-8. When a limit is in bytes, measure bytes.

**Expecting `0.1 + 0.2` to be exact.** Decimal fractions often have no exact binary form, the way 1/3 has no exact decimal form. You'll see this properly in "Values, variables and types"; for now, know that it's binary at work, not a bug in Python.

## Recap

- The **CPU** runs simple instructions very fast; **RAM** holds the running program and its data and is wiped at power-off; **storage** keeps files permanently.
- Everything is stored as **bits**. 8 bits make a **byte**, and `n` bits hold `2ⁿ` values. Binary is base 2: positions worth 1, 2, 4, 8, …
- Text is numbers by agreement: **Unicode** gives each character a **code point**, and **UTF-8** turns code points into 1–4 bytes. Characters ≠ bytes.
- A **program** is instructions. **Compilers** translate ahead of time; **interpreters** run code as they read it.
- Python **compiles your source to bytecode, then interprets the bytecode**, top to bottom, stopping at the first error.

Next, in the exercises, you'll write the binary conversion by hand and measure how many bytes different text takes.
