#!/usr/bin/python3
# This script parses information ix_clients.yml in the root of repository
# to extract info for further processing

import yaml
from jinja2 import Environment, FileSystemLoader
from sys import argv

def main(client_file, template_dir, output_dir):
    # Open the client YAML file and load its contents
    with open(client_file, 'r') as f:
        clients = yaml.safe_load(f)['clients']

        # Process each client entry
        for client in clients:
            # Extract IPv4 and IPv6 addresses
            client['ipv4'] = client['ip'][0]
            client['ipv6'] = client['ip'][1]

            # Determine if the speed is in Gigabits (>= 1000 Mbps)
            speed_in_G = client['speed'] >= 1000
            # Format the speed string based on the unit (G for Gigabits, M for Megabits)
            formatted_speed = '%.12g' % (client["speed"]/1000
                    if speed_in_G
                    else client["speed"])
            unit = "G" if speed_in_G else "M"
            client['speed_string'] = f'{formatted_speed}{unit}'

    # Set up the Jinja2 environment with the argument specified template directory
    env = Environment(loader=FileSystemLoader(template_dir))

    # List all template files in the directory
    template_names = env.list_templates()
    print(f'Found templates: {", ".join(template_names)}')

    # Process each template
    for name in template_names:
        print(f'Processing {name}... ', end='')

        # Load the template
        template = env.get_template(name)

        # Render the template with the clients data
        output = template.render(clients=clients)

        # Extract the output file name from the first line of the rendered template
        first_line = output[:output.find('\n')]
        output_file = first_line[1:].strip()

        # Define the output file path
        output_path = output_dir + output_file

        # Write the rendered output to the file
        with open(output_path, 'w') as f:
            f.write(output)
            print(f'Successfully wrote to {output_path}')

if __name__ == '__main__':
    # Ensure the script is called with the correct number of arguments
    if len(argv) != 4:
        print('Usage: parse.py <client file> <template dir> <output dir>')
        exit(1)

    # Call the main function with the provided arguments
    main(*argv[1:])
