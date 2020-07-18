#!/usr/bin/env python
# coding: utf-8

# # Define the Question 
# ## Specify the Question
# 
# The data is for company X which is trying to control attrition. There are two sets of data: "Existing employees" and "Employees who have left". Following attributes are available for every employee.
# 
# Satisfaction Level
# Last evaluation
# 
# Number of projects
# 
# Average monthly hours
# 
# Time spent at the company
# 
# Whether they have had a work accident
# 
# Whether they have had a promotion in the last 5 years
# 
# Departments (column sales)
# 
# Salary
# 
# Whether the employee has left
# 
# 
# ## Metric of Success
# 
# Discover what time of employees are leaving 
# 
# Determine accurately the employees likely to leave
# 
# ## Experimental Design
# Loading libraries and data
# 
# Data Understanding 
# 
# Data Preparation

# In[1]:


#import libraries
import pandas as pd
import numpy as np

#visualization
import seaborn as sns 
from matplotlib import pyplot as plt 


# In[2]:


#load the file with the datasets 
df = pd.ExcelFile("Hash-Analytic-Python-Analytics-Problem-case-study-1.xlsx")
df


# In[3]:


sheet_names = df.sheet_names
sheet_names


# In[61]:


#load each sheet as a dataframe 
#sheet1
deliverables = df.parse("INFO")
display(deliverables.head())

#sheet2 
existing_emp = df.parse("Existing employees")
display(existing_emp.head())

#Sheet3
left_emp = df.parse("Employees who have left")
display(left_emp.head())


# # Left Employees 

# ## Data Understanding

# In[63]:


#Total rows and columns
left_emp.shape
#there exists 10 columns ans 3571 rows 


# In[65]:


#data types 
left_emp.dtypes
#There exists 2 objects,6 integers and 2 floats


# ## Data Cleaning

# In[67]:


#Consistency
left_emp.duplicated().sum()


# In[70]:


#Completeness - missing values
left_emp.isnull().sum()


# In[71]:


#Uniformity
#Create uniformity the the column names 
left_emp.columns = left_emp.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
left_emp.head()
#all the white spaces have been eliminated and the column names are all in lowercase


# In[75]:


left_emp.columns


# ## Feature Engineering

# In[79]:


# Feature Engineering
def satisfaction(df,variable_1):
  variable2_count = 0
  for ind ,row in df.iterrows():
    if row[variable_1] <= 0.25:
      df.loc[ind,'satisfaction'] = 0.25
    
    elif ((row[variable_1] > 0.25) & (row[variable_1] < 0.75)):
      df.loc[ind,'satisfaction'] = 0.50
    
    elif row[variable_1] >= 0.75:
        df.loc[ind,'satisfaction'] = 0.75
        
    else:
      df.loc[ind,'satisfaction'] = 0


# In[81]:


#mplement the function 
satisfaction(left_emp,"satisfaction_level")


# In[82]:


#view the dataframe again
left_emp.sample(5)


# ## Exploratory Data Analysis

# ### Univariate Analysis

# In[76]:


#categorical = ['dept']
plt.figure(figsize=(11,8))
sns.countplot(left_emp.dept)
plt.ylabel("Number of people in the departments")
plt.xlabel("Departments")
plt.title("Total number of people per department")
plt.show()
#sales,support and technical departments have more people


# In[78]:


#Salary
plt.figure(figsize=(11,8))
sns.countplot(left_emp.salary)
plt.ylabel("Total Salary")
plt.xlabel("Range of salary")
plt.title("Salary")
plt.show()
#the salary of majority of the employees is either low or medium


# In[88]:


#satisfaction of the employees 
plt.figure(figsize=(8,8))
plt.hist(left_emp["satisfaction_level"],bins = 30,color="purple")
plt.xlabel("Satisfaction levels")
plt.title("Satisfaction in the company")
plt.show()
#majority of the employees that have left were had a satisfaction percentage of <= 25%


# In[100]:


#Evaluation
plt.figure(figsize=(8,8))
plt.hist(left_emp["last_evaluation"],bins = 30,color="purple")
plt.xlabel("last_evaluation")
plt.title("Evaluation in the company")
plt.show()


# In[99]:


#Number of projects
plt.figure(figsize=(8,8))
plt.hist(left_emp["number_project"],bins = 30,color="purple")
plt.xlabel("number_project")
plt.title("Total number of projects per employee")
plt.show()


# In[98]:


#Average hours
plt.figure(figsize=(8,8))
plt.hist(left_emp["average_montly_hours"],bins = 30,color="purple")
plt.xlabel("average_montly_hours")
plt.title("Average monthly hours per employee")
plt.show()


# In[97]:


#Duration of time in the company
plt.figure(figsize=(8,8))
plt.hist(left_emp["time_spend_company"],bins = 30,color="purple")
plt.xlabel("time_spend_company")
plt.title("Years spent in the company")
plt.show()


# In[96]:


#Work Accident
plt.figure(figsize=(8,8))
plt.hist(left_emp["work_accident"],color="purple")
plt.xlabel("work_accident")
plt.title("Work accident in the company")
plt.show()


# In[95]:


#promotion in the past 5 years
plt.figure(figsize=(8,8))
plt.hist(left_emp["promotion_last_5years"],bins = 30,color="purple")
plt.xlabel("promotion_last_5years")
plt.title("Promotion in the last 5 years")
plt.show()


# ### Bivariate Analysis

# In[114]:


# Department vs Satisfaction
plt.figure(figsize=(15,15))
left_emp.groupby('dept')["satisfaction"].value_counts().unstack(0).plot.bar()
plt.title("Department vs Satisfaction")
plt.xlabel("Satisfaction")
plt.ylabel("Count")
plt.show()
# Majority of the unsatisfied employees are in the sales,technical and support team
#this could be attributed by the high number of employees in these departments


# In[109]:


#Which Department has more employees
plt.figure(figsize=(6,6))
left_emp.groupby("dept")["emp_id"].count()


# In[110]:


#Relationship between the number of projects and salary
plt.figure(figsize=(6,6))
left_emp.groupby('salary')['number_project'].value_counts().unstack(0).plot.bar()
plt.title("Salary vs Number of Projects")
plt.xlabel("Number of projects")
plt.show()

#From this graph, we can see that majority of the people who leave either have low or medium payments
#They are also overworked with very poor wages
#Majority of the higher earners remain in the business. The few who leave, we can make the assumption that they either opt to retire, have received better opportunities etc


# In[111]:


#Employee duration in the company vs the salary they earn
plt.figure(figsize=(6,6))
left_emp.groupby('time_spend_company')['salary'].value_counts().unstack(0).plot.bar()
plt.title("Salary vs Time spent in the company")
plt.xlabel("Salary")
plt.show()
#Majority that have left have been in the company for more than 3 years and still had to bare with poor wages


# In[112]:


#Number of projects Vs Promotion in the last 5 years 
left_emp.groupby(['number_project'])['promotion_last_5years'].value_counts().unstack(0).plot.bar()
plt.title("Number of projects vs Promotion in the last 5 years")
plt.xlabel("Promotion in the last 5 years")
plt.show()
#Previous employees barely received any promotions


# In[113]:


#Could the employees could cause them not to receive promotions
left_emp.groupby(['work_accident'])['promotion_last_5years'].value_counts().unstack(0).plot.bar()
plt.title("Work accident vs Promotion in the last 5 years")
plt.xlabel("Promotion in the last 5 years")
plt.show()

#The company looks like they have lost the best employees 
#This assumption is based on the fact thatthey have never been involved in any accident


# ### Multivariate Analysis

# In[107]:


#correlation in the columns
plt.figure(figsize=(11,6))
corr = left_emp.corr()
display(corr)
sns.heatmap(corr,annot = True)
plt.title("Correlation of the Variables (Left_Employees)")
plt.show()
# For the heatmap below, it actually means than if there is a negative relationship between two variable, one varaible increases while the other decreases
#For positive correlation, both variable increase 


# In[ ]:





# # Existing Employees 

# ## Data Understanding 

# In[5]:


#data types 
# total rows and columns 
existing_emp.info()

#there exists float64(2), int64(6), object(2) 
#10 columns and 11428 rows


# In[6]:


#Check if the id is duplicated
existing_emp["Emp ID"].nunique()

#all the ids are unique 


# In[7]:


#summary of the data
existing_emp.describe()


# ##  Data Cleaning 

# In[8]:


# Validity
#Check presence of outliers in the dataset 
# create a dataframe with numerical values 
df_num = existing_emp.select_dtypes(["float64", "int64"])
#print 
df_num.head()


# In[9]:


#Consistency
existing_emp.duplicated().sum()


# In[10]:


#Completeness
existing_emp.isnull().sum()
# all the columns are complete


# In[11]:


#Uniformity
existing_emp.columns = existing_emp.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
existing_emp.head()

#all  the column heads have all being put in lowercase and where there was anyy spaces, its being replaced 


# ##  Exploratory Data Analysis

# ### Univariate Analysis
# 

# In[12]:


#categorical = ['dept']
plt.figure(figsize=(11,8))
sns.countplot(existing_emp.dept)
plt.ylabel("Number of people in the departments")
plt.xlabel("Departments")
plt.title("Total number of people per department")
plt.show()


# Majority of the employeed are in the sales department followed by the technical department.

# In[77]:


#Salary
plt.figure(figsize=(11,8))
sns.countplot(existing_emp.salary)
plt.ylabel("Total Salary")
plt.xlabel("Range of salary")
plt.title("Salary")
plt.show()
#the salary of majority of the employees is either low or medium


# From the diagram above, we can make the assumption that most of the people whose salary is high have top positions in the company hence the small number.
# 
# The number of people earning low salary ==  number of people earning medium salary

# In[14]:


#satisfaction of the employees 
plt.figure(figsize=(8,8))
plt.hist(existing_emp["satisfaction_level"],bins = 30,color="maroon")
plt.xlabel("Satisfaction levels")
plt.title("Satisfaction in the company")
plt.show()


# Majority of the current employees have a satifaction level of greater than 50%

# In[15]:


#Evaluation
plt.figure(figsize=(8,8))
plt.hist(existing_emp["last_evaluation"],bins = 30,color="maroon")
plt.xlabel("last_evaluation")
plt.title("Evaluation in the company")
plt.show()


# In[16]:


#Number of projects
plt.figure(figsize=(8,8))
plt.hist(existing_emp["number_project"],bins = 30,color="maroon")
plt.xlabel("number_project")
plt.title("Total number of projects per employee")
plt.show()


# Most of the current employees work either 3 0r 4 projects 

# In[17]:


#Average hours
plt.figure(figsize=(8,8))
plt.hist(existing_emp["average_montly_hours"],bins = 30,color="maroon")
plt.xlabel("average_montly_hours")
plt.title("Average monthly hours per employee")
plt.show()


# In[18]:


#Time spent in the company
plt.figure(figsize=(8,8))
plt.hist(existing_emp["time_spend_company"],bins = 30,color="maroon")
plt.xlabel("time_spend_company")
plt.title("Years spent in the company")
plt.show()


# In[19]:


#Work Accident
plt.figure(figsize=(8,8))
plt.hist(existing_emp["work_accident"],color="maroon")
plt.xlabel("work_accident")
plt.title("Work accident in the company")
plt.show()


# In[20]:


#promotion in the past 5 years
plt.figure(figsize=(8,8))
plt.hist(existing_emp["promotion_last_5years"],bins = 30,color="maroon")
plt.xlabel("promotion_last_5years")
plt.title("Promotion in the last 5 years")
plt.show()


# Most of the employees have not been given any promotions in the last 5 years 

# ### Bivariate Analysis

# Since we have an understanding of all the variables, we shall compare different variables to check if they could cause attrition 

# Department vs Satisfaction
# 
# Lets find out which department has more satisfied employees.

# In[21]:


#checking the satisfaction levels of the employees 
existing_emp["satisfaction_level"].unique()


# #### Feature Engineering

# In[22]:


# Feature Engineering
def satisfaction(df,variable_1):
  variable2_count = 0
  for ind ,row in df.iterrows():
    if row[variable_1] <= 0.25:
      df.loc[ind,'satisfaction'] = 0.25
    
    elif ((row[variable_1] > 0.25) & (row[variable_1] < 0.75)):
      df.loc[ind,'satisfaction'] = 0.50
    
    elif row[variable_1] >= 0.75:
        df.loc[ind,'satisfaction'] = 0.75
        
    else:
      df.loc[ind,'satisfaction'] = 0


# In[23]:


#execute the function
satisfaction(existing_emp,"satisfaction_level")


# In[24]:


#confirm the function has been implemented correctly
existing_emp.sample(10)


# In[25]:


# Department vs Satisfaction
plt.figure(figsize=(15,15))
existing_emp.groupby('dept')["satisfaction"].value_counts().unstack(0).plot.bar()
plt.title("Department vs Satisfaction")
plt.xlabel("Satisfaction")
plt.ylabel("Count")
plt.show()


# Sales department has the highest number of satisfied employees followed by the technical department and Support department.
# 
# This could be attributed by the fact that they have the highest number of employees.
# 
# So we shall check how many employees are in each department to see if this could be the cause of the above result

# In[45]:


#Which Department has more employees
plt.figure(figsize=(6,6))
existing_emp.groupby("dept")["emp_id"].count()

# Sales ,support , technical has the highest numbers of employees hance the high numbers on the satisfaction levels 
#ASSUMPTION - This 3 departments have the highest number of employees stilldue to some not experiencing growth maybe if tasks are unevenly distributed


# In[48]:


#Relationship between the number of projects and salary
plt.figure(figsize=(6,6))
existing_emp.groupby('salary')['number_project'].value_counts().unstack(0).plot.bar()
plt.title("Salary vs Number of Projects")
plt.xlabel("Number of projects")
plt.show()
# There is presence of exploitation in the company since majority of the people with the many projects have very low salary
#We can conclude that, if presence of better opportunities arise, they are willing to take them


# In[53]:


#Employee duration in the company vs the salary they earn
plt.figure(figsize=(6,6))
existing_emp.groupby('time_spend_company')['salary'].value_counts().unstack(0).plot.bar()
plt.title("Salary vs Time spent in the company")
plt.xlabel("Salary")
plt.show()
#Based on the employees duration they have in the company,theyy are still being paid too little 


# In[56]:


#Number of projects Vs Promotion in the last 5 years 
existing_emp.groupby(['number_project'])['promotion_last_5years'].value_counts().unstack(0).plot.bar()
plt.title("Number of projects vs Promotion in the last 5 years")
plt.xlabel("Promotion in the last 5 years")
plt.show()
#Majority of the employees do not receive any promotion hence they might opt to leave and seek for career growth elsewhere 


# In[59]:


#Could the employees could cause them not to receive promotions
existing_emp.groupby(['work_accident'])['promotion_last_5years'].value_counts().unstack(0).plot.bar()
plt.title("Work accident vs Promotion in the last 5 years")
plt.xlabel("Promotion in the last 5 years")
plt.show()
#from the graph, we can see that majority of the employees have been ethical (well behaved) yet they do not receive any promotions.


# ### Multivariate Analysis
# 

# In[60]:


# Correlation 
corr = existing_emp.corr()
display(corr)
plt.figure(figsize=(11,8))
sns.heatmap(corr,annot = True,linewidths=.5)


# The heatmap above shows that if there is a negative correlation one variable increases the other decreases
# 
# The number of projects and satisfaction levels have a negative correlation of -0.093. Meaning, when the number of projects increases, the employees satisfaction decreases.
# 
# 

# # Assumptions

# 

# # Conclusion

# ## Findings

# From the analysis conducted above, I have concluded that Company X is losing majority of there employees due to the wages . This could mean that the company has not reviewed their salary structure which should be reviewed every 18 - 24 months. The rationale behind this is to catch isssues before they become large enough to affect employee engagement and the organizations ability to attract and retain talent.
# Moreover, addressing salary structure is less expensive compared to expenses endured for the recruiting process.
# Company X could also lose its employees due to poor leadership which does not drive employees career development. In this case, we can see that majority of them have not received promotion for over 5 years and are still being under-paid.
# If often seen that good employees get most of the work load due to the trust the leaders have in them. However, Company X should ensure than the number of projects are equally distributed among the employees. If not they should be awarded with incentives or increase in their salary 

# ## Way forward

# 1) Company X needs to review the salary of there employees
# 
# 2) They should add a culture to motivate employees by giving them incentives. Example, they could call out best performing employees for each department per quarter, they could give bonuses. 
# 
# 3) Employ more workforce if the workload is too much for the available employees
# 
# 4) Include activities like Team building. This builds trust among the employees and their superiors as well as amaong the employees themselves. It also creates an environment for everyone to solve internal conflicts they were facing.
