# aws-check-reserved-instances 2018
Compare instance reservations and running instances for AWS services with the new format

# Requirements

- [Python 2.7+](https://www.python.org/downloads/)
- [aws cli Windows](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-windows.html) | [aws cli Linux](https://docs.aws.amazon.com/cli/latest/userguide/awscli-install-linux.html)
- [boto3](https://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation)
- [git](https://git-scm.com/downloads) (Optional)

# Execute
    $ aws-check-reserved-instances.py
 
# Report
        ===========REPORT===========
	          OK	(0)	    r3.large	Linux/UNIX  
	          OK	(8)	     t2.nano	Linux/UNIX (Amazon VPC)
	          OK	(0)	    c3.large	Linux/UNIX  
	       ALERT	(-12)	     t2.nano	Windows (Amazon VPC)
	          OK	(16)	    r3.large	Linux/UNIX (Amazon VPC)
	          OK	(0)	    r3.large	Windows (Amazon VPC)
	       ALERT	(-4)	    c4.large	Linux/UNIX (Amazon VPC)
	          OK	(39)	   m3.medium	Linux/UNIX (Amazon VPC)
	          OK	(0)	   m2.xlarge	Windows     
	          OK	(8)	    m1.small	Linux/UNIX  
	          OK	(0)	   m3.medium	Windows     
	          OK	(2)	    m4.large	Linux/UNIX (Amazon VPC)
	          OK	(4)	   m2.xlarge	Linux/UNIX  
	          OK	(9)	   m2.xlarge	Linux/UNIX (Amazon VPC)
	       ALERT	(-2)	    c3.large	Linux/UNIX (Amazon VPC)
	          OK	(2)	    r4.large	Linux/UNIX (Amazon VPC)
	      DESIRE	(1)	   c1.medium	Linux/UNIX (Amazon VPC)
	      DESIRE	(8)	    r3.large	Windows     
	      DESIRE	(4)	    m1.small	Windows     
	      DESIRE	(8)	   m3.medium	Linux/UNIX  
	      DESIRE	(1)	   c1.medium	Linux/UNIX  
	      DESIRE	(3)	    m4.large	Windows (Amazon VPC)

# Concepts
## To understand what is a instance

- **Instance**: Amazon servers, which can have different sizes, based on the CPU and RAM, and depending on the performance it defines in a family (Example: m5.large), the server families are characterized because they are optimized for a specific purpose.
     For example, the letter:
    - **m** = optimized for cpu and memory
    - **c** = optimized for cpu
    - **r** = optimized for memory
- **Numbers**: Version of each family, the higher number means that it is a more updated family.
- **Sizes:** nano, micro, medium, large, xlarge, 2xlarge.
- **Region**: Place where a set of datacenters is located.
- **Availability zone**: A datacenter within a region
- **Platform**: There is a Windows or Linux operating system
- **Network**: There is a classic network or VPC, depending on where you deployed your instance

## To understand what is a reserved instance
Instances have a cost per hour, but if you are sure you are going to use that instance for at least a year, you can make an advance payment and AWS will give you a discount.

You can advance the total (Total Upfront), only a part and pay less monthly (Partial Upfront) or pay nothing and pay less monthly (No Upfront). if you don't understand how nothing is paid, review the considerations in the final part

**For example:**

    - m5.large = 0.01$ por hour | 8.3$ moth | Total: $100 year

**If you reserve**
    
    - m5.large = (Total Upfront)    pay $50 advance and 0$ moth | Total: $50
    - m5.large = (Partial Upfront)  pay $40 advance and 3$ moth | Total: $76
    - m5.large = (No Upfront)       pay $0 advance and 7$ moth  | Total: $84

# Considerations:
- Amazon charges you the server this turned on or not.
- If you have not specified any availability zones, the discount will be applied to a running instance of any size (within the same family) in the region. For example:
    - Reservations m4.2xlarge Linux (Total Upfront). Instances that apply:
       2 instances m4.xlarge or 4 instances m4.large
   
## :heart: Special Thanks :heart:
Thank you! [Andres Muñoz](https://github.com/andru255). My awe and appreciation for the friendliness of teach me python to achieve my goal.










