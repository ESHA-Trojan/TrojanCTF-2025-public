import random
import string

def generate_junk_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

begin_content = '''#include <stdio.h>

// Define global strings
char str[] = "Can you find the flag somewhere in here?";
'''

flag = '''char str1[] = "Trojan{Y04_F0unD_M3!}";
'''

end_content = '''
int main() {
    // Use the str1 variable to prevent warnings
    (void)str1;

    // Print the string
    printf("%s\\n", str);

    return 0;
}'''

# Open a new file to write the obfuscated content
with open('strings.c', 'w') as f:
    # Write the original content
    f.write(begin_content)
    
    # Add about 10000 lines of junk
    for i in range(10000):
        junk_type = random.choice(['string', 'comment'])
        
        if junk_type == 'string':
            junk = f'char junk_{i}[] = "{generate_junk_string(random.randint(20, 100))}";\n'
        else:  # comment
            junk = f'// {generate_junk_string(random.randint(30, 120))}\n'
        
        f.write(junk)
    f.write(flag)

    # Add some more junk
    for i in range(10000, 25000):
        junk_type = random.choice(['string', 'comment'])

        if junk_type == 'string':
            junk = f'char junk_{i}[] = "{generate_junk_string(random.randint(20, 100))}";\n'
        else:  # comment
            junk = f'// {generate_junk_string(random.randint(30, 120))}\n'

        f.write(junk)

    f.write(end_content)

print("Obfuscated C file created")
