from LexAnalyzer import Tokenizer

def main():
    filename = input("Enter the file name to be tokenized: ")
    try:
        lex = Tokenizer(".\examples\euclid.txt")
        lex.next()
        while lex.kind() != "End-of-text":
            print(lex.position(), lex.kind(), lex.value()) if lex.kind() != "" else print(lex.position(), lex.value())
            lex.next()
        print(f"End of text has been reached for {filename}")
    except FileNotFoundError as err:
        print("File was not found")
    except RuntimeError as err:
        print(err)

if __name__ == "__main__":
    main()
    