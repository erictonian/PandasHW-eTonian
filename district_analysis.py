import pandas as pd
import numpy as np
fschool = "Resources/schools_complete.csv"
fstudent = "Resources/students_complete.csv"
school_df = pd.read_csv(fschool)
student_df = pd.read_csv(fstudent)
df_main = pd.merge(student_df, school_df, how="left", on=["school_name", "school_name"])

dist_schools = school_df["school_name"].count()
dist_students = school_df["size"].sum()
dist_budget = "${:,.2f}".format(school_df["budget"].sum())
dist_math = student_df["math_score"].mean()
dist_read = student_df["reading_score"].mean()
math_pass_cond = student_df["math_score"]>= 70
math_pass_df= student_df[math_pass_cond]
math_pass_count = math_pass_df["math_score"].count()
math_pass_ratio = "{:.2%}".format(math_pass_count/dist_students)
read_pass_cond = student_df["reading_score"]>= 70
read_pass_df= student_df[read_pass_cond]
read_pass_count = read_pass_df["reading_score"].count()
read_pass_ratio = "{:.2%}".format(read_pass_count/dist_students)
dist_pass_ratio = "{:.2%}".format(((math_pass_count/dist_students)+(read_pass_count/dist_students))/2)
dist_summary_df = pd.DataFrame({"Total Schools": [dist_schools],
                               "Total Students": [dist_students],
                               "Total Budget": [dist_budget],
                               "Average Math Score": [dist_math],
                               "Average Reading Score": [dist_read],
                               "% Passing Math": [math_pass_ratio],
                               "% Passing Reading": [read_pass_ratio],
                               "Overall Passing Rate": [dist_pass_ratio]})
dist_summary_df

sort_df = df_main.groupby(['school_name'])
school_students = sort_df['student_name'].count()
school_sort = school_df.sort_values('school_name').set_index('school_name')
school_type = school_sort.loc[:, 'type']
school_budget = sort_df['budget'].mean()
avg_budget = school_budget/school_students
school_math = sort_df['math_score'].mean()
school_read = sort_df['reading_score'].mean()
m_pass_sort = df_main[df_main['math_score'] >= 70].groupby(['school_name'])
school_m_pass = m_pass_sort['math_score'].count()
school_m_ratio = school_m_pass/school_students
r_pass_sort = df_main[df_main['reading_score'] >= 70].groupby(['school_name'])
school_r_pass = r_pass_sort['reading_score'].count()
school_r_ratio = school_r_pass/school_students
school_pass_rate = (school_m_ratio + school_r_ratio)/2
school_summary_table = pd.DataFrame({"Total Students": school_students,
                                    "School Type": school_type,
                                    "Total Budget": school_budget,
                                    "Budget per Student": avg_budget,
                                    "Average Math Score": school_math,
                                    "Average Reading Score": school_read,
                                    "% Passing Math": school_m_ratio,
                                    "% Passing Reading": school_r_ratio,
                                    "Overall Passing Rate": school_pass_rate
                                    })
del school_summary_table.index.name
school_summary_table

best_pass = school_summary_table.sort_values('Overall Passing Rate', ascending=False)
best_pass.head()

worst_pass = school_summary_table.sort_values('Overall Passing Rate', ascending=True)
worst_pass.head()

sorted_9th = df_main[df_main['grade'] == "9th"].groupby(['school_name'])
math_9th = sorted_9th['math_score'].mean()
sorted_10th = df_main[df_main['grade'] == "10th"].groupby(['school_name'])
math_10th = sorted_10th['math_score'].mean()
sorted_11th = df_main[df_main['grade'] == "11th"].groupby(['school_name'])
math_11th = sorted_11th['math_score'].mean()
sorted_12th = df_main[df_main['grade'] == "12th"].groupby(['school_name'])
math_12th = sorted_12th['math_score'].mean()
math_by_grade_table = pd.DataFrame({"9th": math_9th,
                                    "10th": math_10th,
                                    "11th": math_11th,
                                    "12th": math_12th})
del math_by_grade_table.index.name
math_by_grade_table

sorted_9th = df_main[df_main['grade'] == "9th"].groupby(['school_name'])
read_9th = sorted_9th['reading_score'].mean()
sorted_10th = df_main[df_main['grade'] == "10th"].groupby(['school_name'])
read_10th = sorted_10th['reading_score'].mean()
sorted_11th = df_main[df_main['grade'] == "11th"].groupby(['school_name'])
read_11th = sorted_11th['reading_score'].mean()
sorted_12th = df_main[df_main['grade'] == "12th"].groupby(['school_name'])
read_12th = sorted_12th['reading_score'].mean()
read_by_grade_table = pd.DataFrame({"9th": read_9th,
                                    "10th": read_10th,
                                    "11th": read_11th,
                                    "12th": read_12th})
del read_by_grade_table.index.name
read_by_grade_table

bins = [0, 585, 615, 645, 675]
bin_names = ["< $590", "$590-610", "$610-630", "> $630"]
budget_sum = school_summary_table
budget_sum['Budget Group'] = pd.cut(budget_sum['Budget per Student'], bins, labels=bin_names)
budget_sum = budget_sum.groupby('Budget Group')
budget_sum[[
    'Average Math Score', 
    'Average Reading Score', 
    '% Passing Math', 
    '% Passing Reading', 
    'Overall Passing Rate']].mean()

size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]
size_sum = school_summary_table
size_sum['Size Group'] = pd.cut(size_sum['Total Students'], size_bins, labels=group_names)
size_sum = size_sum.groupby('Size Group')
size_sum[[
    'Average Math Score', 
    'Average Reading Score', 
    '% Passing Math', 
    '% Passing Reading', 
    'Overall Passing Rate']].mean()

type_sum = school_summary_table
type_sum = type_sum.groupby('School Type')
type_sum[[
    'Average Math Score', 
    'Average Reading Score', 
    '% Passing Math', 
    '% Passing Reading', 
    'Overall Passing Rate']].mean()