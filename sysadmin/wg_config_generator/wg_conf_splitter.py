import re

with open('client_configs.conf','r') as f:
    data = f.read()
    data = data.replace('\n\n', '\n')
    configs = data.split('[Interface]')[1:]

configs[-1]=configs[-1]+"\nDummy"
rand_int = 0
for config in configs:
    config = config.strip()
    if config == '':
        continue
    config = '[Interface]\n'+config
    # removing last two lines
    config = config.split('\n')[0:-1]
    config.insert(4,'DNS = 1.1.1.1')
    config = "\n".join(config)
    file_name = re.findall(r"\#\# ([\w ]+)", config)
    if file_name:
        file_name = file_name[0].lower().replace(' ','_')
    else:
        file_name = 'unnamed_client_'+str(rand_int)
        rand_int += 1

    with open('client_configs/'+file_name+'.conf','w') as f:
        f.write(config)
    print(file_name)
