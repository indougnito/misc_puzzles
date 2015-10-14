from RetentionModel import RetentionModel

filepath = 'accdata.csv'
model = RetentionModel(filepath)

#####################################
# A) what is the overall 7-day ui retention for September?

model.computeRetentionForDay(0) # 0-day retention is 100% by definition
model.computeRetentionForDay(7)

sum_0_day = 0
sum_7_day = 0
for day in model.data[2014][9]:
    if day is 'user_activity':
        continue # i've got this hokey 'user_activity' field, which we can just ignore...
    sum_0_day += model.data[2014][9][day]['retention'][0]
    sum_7_day += model.data[2014][9][day]['retention'][7]
rate_7_day = float(sum_7_day) / float(sum_0_day) * 100

# Day7 retention for September is 6156 out of 37983 users, or 16.2072506121%.
print 'Day7 retention for September is ' + \
      str(sum_7_day) + \
      ' out of ' + \
      str(sum_0_day) + \
      ' users, or ' + \
      str(rate_7_day) + \
      '%.'

#####################################
# B) what is the 7-day ui retention from sept 8 - sept 10 for android?

model.computeRetentionForDay(0, os='android')
model.computeRetentionForDay(7, os='android')

sum_0_day = 0
sum_7_day = 0
for day in [8, 9, 10]:
    if day is 'user_activity':
        continue
    sum_0_day += model.data[2014][9][day]['retention'][0]
    sum_7_day += model.data[2014][9][day]['retention'][7]
rate_7_day = float(sum_7_day) / float(sum_0_day) * 100

# Day7 retention for android between Sept 8 and Sept 10 is 34 out of 1681 users, or 2.02260559191%.
print 'Day7 retention for android between Sept 8 and Sept 10 is ' + \
      str(sum_7_day) + \
      ' out of ' + \
      str(sum_0_day) + \
      ' users, or ' + \
      str(rate_7_day) + \
      '%.'

#####################################
# C) what is the 7-day ui retention for September for IOS 1.7.5?

model.computeRetentionForDay(0, os='IOS', version='1.7.5')
model.computeRetentionForDay(7, os='IOS', version='1.7.5')

sum_0_day = 0
sum_7_day = 0
for day in model.data[2014][9]:
    if day is 'user_activity':
        continue
    sum_0_day += model.data[2014][9][day]['retention'][0]
    sum_7_day += model.data[2014][9][day]['retention'][7]
rate_7_day = float(sum_7_day) / float(sum_0_day) * 100

# Day7 retention for IOS 1.7.5 during September is 2890 out of 9902 users, or 29.1860230257%
print 'Day7 retention for IOS 1.7.5 during September is ' + \
      str(sum_7_day) + \
      ' out of ' + \
      str(sum_0_day) + \
      ' users, or ' + \
      str(rate_7_day) + \
      '%.'
