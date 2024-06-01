import re
from datetime import datetime, timedelta

def read_markdown_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_markdown_file(file_path, lines):
    with open(file_path, 'w') as file:
        file.writelines(lines)

def find_last_week(lines):
    week_pattern = re.compile(r'# week (\d+)')
    date_pattern = re.compile(r'### mon (\d{2}/\d{2}) - sun (\d{2}/\d{2})')
    last_week_index = None
    last_week_number = 0
    last_week_start_date = None
    last_week_end_date = None

    for i, line in enumerate(lines):
        week_match = week_pattern.match(line)
        if week_match:
            last_week_index = i
            last_week_number = int(week_match.group(1))
        date_match = date_pattern.match(line)
        if date_match:
            last_week_start_date = datetime.strptime(date_match.group(1) + '/2024', '%d/%m/%Y')
            last_week_end_date = datetime.strptime(date_match.group(2) + '/2024', '%d/%m/%Y')

    return last_week_index, last_week_number, last_week_start_date, last_week_end_date

def copy_last_week_tasks(lines, last_week_index):
    task_lines = []
    # Skip the week header and date range lines
    i = last_week_index + 2
    while i < len(lines) and not lines[i].startswith('# week'):
        task_lines.append(lines[i])
        i += 1
    return task_lines

def create_new_week_section(last_week_number, last_week_end_date, task_lines):
    new_week_number = last_week_number + 1
    new_start_date = last_week_end_date + timedelta(days=1)
    new_end_date = new_start_date + timedelta(days=6)
    new_start_date_str = new_start_date.strftime('%d/%m')
    new_end_date_str = new_end_date.strftime('%d/%m')

    new_week_section = [
        "\n",
        "\n",
        "\n",
        "\n",
        "\n",
        "========================\n",
        "\n",
        "\n",
        "\n",
        f"# week {new_week_number}\n",
        f"### mon {new_start_date_str} - sun {new_end_date_str}\n",
        "\n",
        "+ [ ] **from last week**\n"
    ]
    new_week_section.extend(task_lines)
    new_week_section.append("\n")
    return new_week_section

def main(file_path):
    lines = read_markdown_file(file_path)
    
    last_week_index, last_week_number, last_week_start_date, last_week_end_date = find_last_week(lines)
    task_lines = copy_last_week_tasks(lines, last_week_index)
    new_week_section = create_new_week_section(last_week_number, last_week_end_date, task_lines)
    
    lines.extend(new_week_section)
    write_markdown_file(file_path, lines)

# Example usage
file_path = 'weekly-raodmap.md'
main(file_path)
