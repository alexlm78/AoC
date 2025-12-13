#part one
data = open('input.txt')
reports = []
safe_1 = 0
for row in data:
    appendable = []
    row_split = row.split()
    for num in row_split:
        appendable.append(int(num))
    reports.append(appendable)
data.close()
def check_if_sorted(report):
    rep_asc = report.copy()
    rep_desc = report.copy()
    rep_asc.sort()
    rep_desc.sort(reverse=True)
    if report == rep_asc:
        return True
    elif report == rep_desc:
        return True
    return False
def check_differences(report):
    for num in range(len(report) - 1):
        if abs(report[num] - report[num+1]) in [1,2,3]:
            pass
        else:
            return False
        if num == (len(report) - 2):
            return True
for report in reports:
    increase_check = check_if_sorted(report)
    difference_check = check_differences(report)
    if increase_check and difference_check:
        safe_1 += 1
print(f'The number of safe reports is equal to {safe_1}')
#part two
safe_2 = 0
def problem_dampener(report):
    list_dampened = []
    for num in range(len(report)):
        new_report = report.copy()
        new_report.pop(num)
        list_dampened.append(new_report)
    return list_dampened
for report in reports:
    increase_check = check_if_sorted(report)
    difference_check = check_differences(report)
    if increase_check and difference_check:
        safe_2 += 1
    else:
        reports_dampened = problem_dampener(report)
        for report_dam in reports_dampened:
            increase_check_dam = check_if_sorted(report_dam)
            difference_check_dam = check_differences(report_dam)
            if increase_check_dam and difference_check_dam:
                safe_2 += 1
                break
print(f'Actually the number of safe reports is equal to {safe_2} after problem dampening')