import argparse

def generate_fqdn_objects(input_file, device_group, output_file=None, verbose=None):
    #generates an FQDN object and prints out the command to put into Panorama CLI
    try:
        with open(input_file, 'r') as f:
            fqdn_list = [line.strip() for line in f if line.strip()]

    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
        return
    
    generated_objects = []

    for fqdn in fqdn_list:
        object = sanitize_name(fqdn)
        if verbose:
            print(f"set device-group {device_group} address {object} fqdn {fqdn}")
            generated_objects.append(object)
        else:    
            generated_objects.append(object)

    if output_file:
        try: 
            with open(output_file, 'w') as f_out:
                for object in generated_objects:
                    f_out.write(object + '\n')

                print(f"\n'[+]' Object names written to {output_file}")
        except IOError as e:
            print(f'Error writing to output file: {e}')    

def add_object_to_group(input_file, device_group, address_group, output_file=None, verbose=None):
    # Adds an object to an exisiting address group
    try:
        with open(input_file, 'r') as f:
            object_list = [line.strip() for line in f if line.strip()]

    except FileNotFoundError:
        print(f"File '{input_file}' not found.")
        return
    
    generated_objects = []

    for object in object_list:
        if verbose:
            print(f"set device-group {device_group} address-group {address_group} static {object}")
            generated_objects
        else:
            generated_objects.append(object)
    
    if output_file:
        try:
            with open(output_file, 'w') as f_out:
                for object in generated_objects:
                    f_out.write(object + '\n')
                print(f"\n'[+]' Object names written to {output_file}")
        except IOError as e:
            print(f'Error writing to output file: {e}')        





def sanitize_name(fqdn):
    # Replace non-alphanumeric characters with underscores to create a valid object name
    return fqdn.strip().lower().replace('.', '_').replace('-', '_')

def main():
    parser = argparse.ArgumentParser(description="Tool to make putting in those stupid, long lists of FQDNs into Panorama way easier because Palo Alto still refuses to let you import a text file from the GUI...")
    subparsers = parser.add_subparsers(dest="function", required=True)

    # Shared args
    common_args = argparse.ArgumentParser(add_help=False)
    common_args.add_argument("file", help="Input text file name, e.g: fqdn_list.txt")
    common_args.add_argument("device_group", help="The device group to add objects to")
    common_args.add_argument("-o", "--output", help="Writes objects to a text file")
    common_args.add_argument("-v", "--verbose", action="store_true", help="Print each command as it's generated")

    # fqdn subcommand
    fqdn_parser = subparsers.add_parser("fqdn", parents=[common_args], help="Generate FQDN address objects")

    # addrgrp subcommand
    addrgrp_parser = subparsers.add_parser("addrgrp", parents=[common_args], help="Add objects to an address group")
    addrgrp_parser.add_argument("address_group", help="Address group name to add objects to")

    # Parse args
    args = parser.parse_args()

    # Dispatch to the right function
    if args.function == "fqdn":
        generate_fqdn_objects(args.file, args.device_group, args.output, args.verbose)
    elif args.function == "addrgrp":
        add_object_to_group(args.file, args.device_group, args.address_group, args.output, args.verbose)

if __name__ == "__main__":
    main()

