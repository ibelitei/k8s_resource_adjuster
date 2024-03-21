import yaml

def adjust_resources(request_cpu, request_memory, increase_percentage):
    # Convert to float for uniform processing and calculate increase factor
    increase_factor = 1 + increase_percentage / 100.0

    # Adjust CPU
    if request_cpu.endswith('m'):
        cpu_millicores = int(request_cpu[:-1])
        limit_cpu = f"{int(cpu_millicores * increase_factor)}m"
    else:
        cpu_cores = float(request_cpu)
        limit_cpu = f"{cpu_cores * increase_factor:.1f}".rstrip('.0')

    # Adjust memory
    if request_memory.endswith('Gi'):
        memory_gib = float(request_memory[:-2])
        limit_memory = f"{memory_gib * increase_factor}Gi"
    else:
        memory_mib = int(request_memory[:-2])
        limit_memory = f"{int(memory_mib * increase_factor)}Mi"

    return limit_cpu, limit_memory

def adjust_all_resources(data, increase_percentage):
    for service_group, service_data in data.items():
        for service, resources in service_data['resources'].items():
            requests = resources['requests']
            limits = resources['limits']

            new_cpu_limit, new_memory_limit = adjust_resources(
                requests['cpu'], requests['memory'], increase_percentage
            )

            limits['cpu'] = new_cpu_limit
            limits['memory'] = new_memory_limit

    return data

def add_space_between_services(yaml_content):
    lines = yaml_content.split('\n')
    modified_lines = []
    previous_line_was_service_group = False

    for i, line in enumerate(lines):
        if not line.startswith('  ') and i > 0:
            if not previous_line_was_service_group:
                modified_lines.append('')
            previous_line_was_service_group = True
        else:
            previous_line_was_service_group = False

        modified_lines.append(line)

    return '\n'.join(modified_lines)

def main():
    # Attempt to read the original resources file
    try:
        with open('original_resources.yaml', 'r') as file:
            original_data = yaml.safe_load(file)
    except FileNotFoundError:
        print("Error: 'original_resources.yaml' not found.")
        return

    # Request the percentage increase from the user
    try:
        increase_percentage = float(input("Enter the percentage increase for resources: "))
    except ValueError:
        print("Invalid input. Please enter a valid number for the percentage increase.")
        return

    # Adjust the resources with the user-specified increase percentage
    adjusted_data = adjust_all_resources(original_data, increase_percentage)

    # Convert adjusted data to YAML string and add spaces between services
    adjusted_data_str = yaml.dump(adjusted_data, default_flow_style=False, allow_unicode=True, sort_keys=False)
    adjusted_data_str_with_spaces = add_space_between_services(adjusted_data_str)

    # Write the modified string with spaces to a new file
    with open('adjusted_resources.yaml', 'w') as file:
        file.write(adjusted_data_str_with_spaces)

if __name__ == "__main__":
    main()
