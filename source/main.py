from node_parser.parser import Parser


def main():
    try:
        with open('source\\node_parser\\test.txt', 'r') as f:
            text = f.read()
    except FileNotFoundError as e:
        print(f"Error: {e} - File not found. Make sure the file exists and the path is correct.")

    parser = Parser(text)
    result = parser.parse()
    
    with open('source\\node_parser\\result.txt', 'w') as f:
        f.write(str(result))

    
if __name__ == '__main__':
    main()