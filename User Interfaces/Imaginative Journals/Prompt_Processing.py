# Daniel Neamati
# 10 December 2017

def read_prompts(filename):
    '''This function reads a file that contains journal prompts and returns
    a list of those prompts without the number at the start.'''
    # Un-processed prompts
    up = open(filename, 'r')
    prompts = []

    for line in up:
        # We start by removing the space and decimal that marks
        # the start of the prompt
        current_line = line.split()
        try:
            first_char = current_line[0].split('.')
            first_char = int(first_char[0])
            current_line.pop(0) # Remove the integer marking the prompt.
            new_prompt_list = ' '.join(current_line) # Join prompt to string.
            prompts.append(new_prompt_list)
            print("Check!")
        except IndexError:
            pass
        except ValueError:
            pass
    up.close()
    return prompts

def write_prompts(filename, prompts):
    '''This function writes processed prompts (in a list format) to a file.
    This function does not return anything.'''
    # Journal Prompts
    jp = open(filename, "a")
    for item in prompts:
        jp.write(item + '\n')
        print("Written")
    jp.close()

write_prompts("Journal Prompts.txt", read_prompts("prompts.txt"))
