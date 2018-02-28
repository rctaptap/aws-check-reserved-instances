import boto3   
import warnings
warnings.filterwarnings('ignore', category=UnicodeWarning)
def get_count_reserved_by_family_base(instances,instance_type,platform):
    item = {}
    total = 0
    for i in instances:
        if instance_type[:2] in i['InstanceType'] and i['ProductDescription'] == platform: 
            count = get_instance_family_value(i['InstanceType'])    
            total += int(count) * int(i['InstanceCount'])
            item['instance_type'] = get_instance_family_base(i['InstanceType'])
            item['total'] = total
            item['platform'] = platform
    return item

def get_reserved_instances(client):
    list = []
    item = {}
    inst = client.describe_reserved_instances(
        Filters=[{'Name': 'state', 'Values': ['active', ]}])
    instances = inst['ReservedInstances']
    for i in instances:
        instance_type = i['InstanceType']
        platform = i['ProductDescription']
        item = get_count_reserved_by_family_base(instances,instance_type,platform)
        if item not in list:
            list.append(item)           
    return list

def get_platform_standar(item):
    if 'VpcId' in item:
        if 'Platform' in item:
            p = 'Windows (Amazon VPC)'
        else:
            p = 'Linux/UNIX (Amazon VPC)'
    else:
        if 'Platform' in item:
            p = 'Windows'
        else:
            p = 'Linux/UNIX'
    return p

def get_count_instance_by_type(instances,instance_type,platform):
    item = {}
    total = 0    
    count = 0
    for r in instances:
        for i in r['Instances']:     
            p = get_platform_standar(i)
            if instance_type[:2] in i['InstanceType'] and p == platform:  
                count = get_instance_family_value(i['InstanceType'])   
                total += int(count)
                item['instance_type'] = get_instance_family_base(i['InstanceType'])
                item['total'] = total
                item['platform'] = platform
    return item

def get_count_instance_by_family_base(instances,instance_type,platform):
    item = {}
    total = 0
    for i in instances:
        if i['instance_type'] == instance_type and i['platform'] == platform:
            total += i['total']
            item['instance_type'] = instance_type
            item['total'] = total
            item['platform'] = platform
    return item

def get_running_instances(client):
    list = []
    list_final = []
    item = {}
    item_final = {}
    instances = client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    for r in instances['Reservations']:
        for i in r['Instances']:
            if 'SpotInstanceRequestId' in i:
                continue
            platform = get_platform_standar(i)
            instance_type = i['InstanceType']
            item = get_count_instance_by_type(instances['Reservations'],instance_type,platform)
            if item not in list:
                list.append(item)  
    for instance in list:
        item_final = get_count_instance_by_family_base(list,instance['instance_type'],instance['platform'])
        if item_final not in list_final:
            list_final.append(item_final)  
    return list_final            

def get_message(value):
    message = ''
    if value < 0:
        message = 'ALERT'
    else:
        message = 'OK'    
    return message

def get_scope_reserved(instances,reserved):
    list = []
    item = {}

    for res in reserved:   
        value = 'false'
        item = {} 
        for ins in instances:                       
            if ins['instance_type'] == res['instance_type'] and ins['platform'] == res['platform']:
                total = int(ins['total']) - int(res['total'])
                item['instance_type'] = ins['instance_type']
                item['total'] = int(total)
                item['platform'] = ins['platform']
                item['message'] = get_message(total)
                value = 'true'
            else:
                if value == 'false':
                    total = -1 * int(res['total'])
                    item['instance_type'] = res['instance_type']
                    item['total'] = int(total)
                    item['platform'] = res['platform']
                    item['message'] = get_message(total)
        if item is not None:
            list.append(item)  
    
    for insf in instances:
        value = 'false'
        item = {} 
        for comp in list:
            if insf['instance_type'] == comp['instance_type'] and insf['platform'] == comp['platform']:
                value = 'false'
                break
            else:
                value = 'true'
        if value == 'true':
            item['instance_type'] = insf['instance_type']
            item['total'] = insf['total']
            item['platform'] = insf['platform']
            item['message'] = "DESIRE"
            if item is not None:
                list.append(item)  
    return list

def get_instance_family_value(type):
    switcher = {
        "m1.small": "1",
        "m1.medium": "2",
        "m1.large": "4",
        "m1.xlarge": "8",
        "m2.xlarge": "1",
        "m2.2xlarge": "2",
        "m2.4xlarge": "8",
        "m3.medium": "1",
        "m3.large": "2",
        "m3.xlarge": "4",
        "m3.2xlarge": "8",
        "m4.large": "1",
        "m4.xlarge": "2",
        "m4.2xlarge": "4",
        "m4.4xlarge": "8",
        "m4.10xlarge": "20",
        "m4.16xlarge": "32",
        "m5.large": "1",
        "m5.xlarge": "2",
        "m5.2xlarge": "4",
        "m5.4xlarge": "8",
        "m5.12xlarge": "24",
        "m5.24xlarge": "48",
        "c1.medium": "1",
        "c1.xlarge": "2",
        "t1.micro": "1",
        "t2.nano": "1",
        "t2.micro": "2",
        "t2.small": "4",
        "t2.medium": "8",
        "t2.large": "16",
        "t2.xlarge": "32",
        "t2.2xlarge": "64",
        "c3.large": "1",
        "c3.xlarge": "2",
        "c3.2xlarge": "4",
        "c3.4xlarge": "8",
        "c3.8xlarge": "16",
        "c4.large": "1",
        "c4.xlarge": "2",
        "c4.2xlarge": "4",
        "c4.4xlarge": "8",
        "c4.8xlarge": "16",
        "c5.large": "1",
        "c5.xlarge": "2",
        "c5.2xlarge": "4",
        "c5.4xlarge": "8",
        "c5.9xlarge": "18",
        "c5.18xlarge": "36",
        "r3.large": "1",
        "r3.xlarge": "2",
        "r3.2xlarge": "4",
        "r3.4xlarge": "8",
        "r3.8xlarge": "16",
        "r4.large": "1",
        "r4.xlarge": "2",
        "r4.2xlarge": "4",
        "r4.4xlarge": "8",
        "r4.8xlarge": "16",
        "r4.16xlarge": "32"
    }
    return switcher.get(type, "nothing")

def get_instance_family_base(type):
    switcher = {
        "m1.small": "m1.small",
        "m1.medium": "m1.small",
        "m1.large": "m1.small",
        "m1.xlarge": "m1.small",
        "m2.xlarge": "m2.xlarge",
        "m2.2xlarge": "m2.xlarge",
        "m2.4xlarge": "m2.xlarge",
        "m3.medium": "m3.medium",
        "m3.large": "m3.medium",
        "m3.xlarge": "m3.medium",
        "m3.2xlarge": "m3.medium",
        "m4.large": "m4.large",
        "m4.xlarge": "m4.large",
        "m4.2xlarge": "m4.large",
        "m4.4xlarge": "m4.large",
        "m4.10xlarge": "m4.large",
        "m4.16xlarge": "m4.large",
        "m5.large": "m5.large",
        "m5.xlarge": "m5.large",
        "m5.2xlarge": "m5.large",
        "m5.4xlarge": "m5.large",
        "m5.12xlarge": "m5.large",
        "m5.24xlarge": "m5.large",
        "c1.medium": "c1.medium",
        "c1.xlarge": "c1.medium",
        "t1.micro": "c1.medium",
        "t2.nano": "t2.nano",
        "t2.micro": "t2.nano",
        "t2.small": "t2.nano",
        "t2.medium": "t2.nano",
        "t2.large": "t2.nano",
        "t2.xlarge": "t2.nano",
        "t2.2xlarge": "t2.nano",
        "c3.large": "c3.large",
        "c3.xlarge": "c3.large",
        "c3.2xlarge": "c3.large",
        "c3.4xlarge": "c3.large",
        "c3.8xlarge": "c3.large",
        "c4.large": "c4.large",
        "c4.xlarge": "c4.large",
        "c4.2xlarge": "c4.large",
        "c4.4xlarge": "c4.large",
        "c4.8xlarge": "c4.large",
        "c5.large": "c5.large",
        "c5.xlarge": "c5.large",
        "c5.2xlarge": "c5.large",
        "c5.4xlarge": "c5.large",
        "c5.9xlarge": "c5.large",
        "c5.18xlarge": "c5.large",
        "r3.large": "r3.large",
        "r3.xlarge": "r3.large",
        "r3.2xlarge": "r3.large",
        "r3.4xlarge": "r3.large",
        "r3.8xlarge": "r3.large",
        "r4.large": "r4.large",
        "r4.xlarge": "r4.large",
        "r4.2xlarge": "r4.large",
        "r4.4xlarge": "r4.large",
        "r4.8xlarge": "r4.large",
        "r4.16xlarge": "r4.large"
    }
    return switcher.get(type, "nothing")

def get_table(instances,title):
    print('===========%s===========' % (title))
    for i in instances:
        if i is not None:
            instance_type = i['instance_type']
            platform = i['platform']
            total = i['total']            
            if title == 'REPORT':
                message = i['message']
                print('\t%12s\t(%-i)\t%12s\t%-12s' % (message,total,instance_type,platform))
            else:
                print('\t(%i)\t%12s\t%-12s' % (total,instance_type,platform))
    
ec2 = boto3.client('ec2')

ris = get_reserved_instances(ec2)
ins = get_running_instances(ec2)
comp = get_scope_reserved(ins,ris)


get_table(ris,"RESERVED")
get_table(ins,"INSTANCES")
get_table(comp,"REPORT")





