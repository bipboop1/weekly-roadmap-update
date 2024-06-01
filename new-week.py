import re
from datetime import datetime, timedelta

def update_task_list(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Find the last week's tasks
    last_week_match = re.search(r'# week (\d+)\n### mon (\d{2}/\d{2}) - sun (\d{2}/\d{2})\n((?:.|\n)+?)(?=\n# week \d+|$)', content)
    
    if not last_week_match:
        print("No valid week found in the file.")
        return
    
    last_week_number = int(last_week_match.group(1))
    start_date_str = last_week_match.group(2)
    end_date_str = last_week_match.group(3)
    tasks = last_week_match.group(4)
    
    # Calculate the new week number and dates
    new_week_number = last_week_number + 1
    start_date = datetime.strptime(start_date_str, '%d/%m')
    end_date = datetime.strptime(end_date_str, '%d/%m')
    
    new_start_date = start_date + timedelta(days=7)
    new_end_date = end_date + timedelta(days=7)
    
    new_start_date_str = new_start_date.strftime('%d/%m')
    new_end_date_str = new_end_date.strftime('%d/%m')
    
    # Process tasks
    updated_tasks = []
    sublists = []

    def add_sublist(prefix, lines, depth):
        for line in lines:
            if prefix in line:
                sublist_prefix = f'**from last {"last " * depth}week**'
                sublists.append((depth, line.replace(prefix, sublist_prefix)))
                add_sublist(sublist_prefix, lines[lines.index(line)+1:], depth + 1)
            elif line.startswith('\t' * depth + '- ') or line.startswith('\t' * depth + '+ '):
                sublists.append((depth, line))
            elif line.startswith('+ [ ] **from last week**'):
                break

    lines = tasks.split('\n')
    add_sublist('**from last week**', lines, 1)

    new_tasks = []
    for depth, task in sublists:
        new_tasks.append('\t' * depth + task)
    
    # Construct the new week's tasks
    new_week_content = f"# week {new_week_number}\n### mon {new_start_date_str} - sun {new_end_date_str}\n"
    new_week_content += "+ [ ] **from last week**\n"
    for task in new_tasks:
        new_week_content += '\t' + task + '\n'

    # Append the new week to the content
    content += '\n\n' + '='*24 + '\n\n' + new_week_content.strip()
    
    with open(file_path, 'w') as file:
        file.write(content)

# Example usage
update_task_list('weekly-roadmap.md')
