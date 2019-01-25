import string
import re

a_list = ['0[factory]', '14', '0[driver]', 'ggg', '0[phone]', '12012341234', '0[factoryId]', '15', '1[factory]', '17', '1[driver]', '11', '1[phone]', '22', '1[factoryId]', '16']

b_str = {'0[factory]': '14', '0[driver]': '▒▒ʦ▒▒', '0[phone]': '12012341234', '0[factoryId]': '15', '1[factory]': '17', '1[driver]': '11', '1[phone]': '22', '1[factoryId]': '16'}

a_dict = {'0[factory]': '14', '0[driver]': '132156', '0[phone]': '12012341234', '0[factoryId]': '15', '1[factory]': '17', '1[driver]': '11', '1[phone]': '22', '1[factoryId]': '16'}

b_list = []

for i in a_list:
    re.sub(r'\[.*', '', i)
    b_list.append(i)

print(b_list)


a = re.sub(r'\[.*','',)
# num = re.sub(r'\d[',']', "", a_list)



# data = {
#
#         'factory': a_dict['0[factory]'],
#         'driver': a_dict['0[driver]'],
#         'phone': a_dict['0[phone]'],
#         'factoryId': a_dict['0[factoryId]'],
#         # 'factory': a_dict['1[factory]'],
#
#
# }
# print(data)
#
# for key in sorted(newdict,key=lambda x:int(x[x.rfind("_")+1:])):
#     print(key)

# data = {}
#
# for i in range(0, len(a_list), 2):
#     data[a_list[i]] = a_list[i + 1]
# print(data)

# for i in range(0, len(a_list), 2):
#     str = a_list[i]
#     start = str.find('[') + 1
#     str1 = str[start:len(str) - 1]
#     list.append(str1)
    # list.append(data[str1] = a_list[i + 1])

# print(list)


# print(data)
# for i in b_str:
#     if i == 'factory':

# b_str.translate(str.maketrans('','','['))
# print(b_str)

