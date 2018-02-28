# aws-check-reserved-instances 2018
Compare instance reservations and running instances for AWS services with the new format

# Requirements

- Python 2.7+
- aws cli
- boto3

# Execute
    $ aws-check-reserved-instances.py
 
# Report
    ===========REPORT===========
    OK	(0)	    r3.large	Linux/UNIX  
    OK	(0)	     t2.nano	Linux/UNIX (Amazon VPC)
    OK	(0)	    c3.large	Linux/UNIX  
    ALERT	(-12)	     t2.nano	Windows (Amazon VPC)
    DESIRE	(22)	    r3.large	Linux/UNIX (Amazon VPC)
    OK	(0)	    r3.large	Windows (Amazon VPC)
    ALERT	(-4)	    c4.large	Linux/UNIX (Amazon VPC)
    DESIRE	(40)	   m3.medium	Linux/UNIX (Amazon VPC)
    OK	(0)	   m2.xlarge	Windows     
    DESIRE	(8)	    m1.small	Linux/UNIX  
    OK	(0)	   m3.medium	Windows     
    DESIRE	(2)	    m4.large	Linux/UNIX (Amazon VPC)
    DESIRE	(4)	   m2.xlarge	Linux/UNIX  
    DESIRE	(18)	   m2.xlarge	Linux/UNIX (Amazon VPC)
    OK	(0)	    c3.large	Linux/UNIX (Amazon VPC)

# Concepts
## To understand what is a instance

- **Instancia**: Amazon llama así a los servidores, que pueden tener distintos tamaños, en base al CPU y RAM, y dependiendo el desempeño lo define en una familia (Ejemplo: m5.large), las familias de servidores se caracterizan por que están optimizadas para un fin específico.
    Por ejemplo la letra:
    - **m** = optimizado para cpu y memoria 
    - **c** = optimizado para cpu
    - **r** = optimizado para memoria
- **Números**: Versión de cada familia, mientras mayor el número, quiere decir que es una familia más actualizada.
- **Tamaños:** nano, micro, medium, large, xlarge, 2xlarge. 
- **Region**: Lugar donde se encuentra un conjunto de datacenters.
- **Zona de disponibilidad**: Un datacenter dentro de una región
- **Plataforma**: Existe el sistema operativo Windows o Linux
- **Red**: Existe red clásica o VPC, dependiendo donde desplegaste tu instancia

## To understand what is a reserved instance
Las instancias tienen un costo por hora, pero si estás seguro que vas a utilizar esa instancia durante por lo menos un año, puedes hacer un pago adelantado y AWS te dará un descuento.

Puedes adelantar el total (Total Upfront), o una parte y pagas menos mensualmente (Partial Upfront)

**Por ejemplo:**
- m5.large = 0.01$ por hora | 8.3$ mes | Total: $100 año

**Si reservas**
- m5.large = (Total Upfront)    $50 adelanto y 0$ mes | Total: $50
- m5.large = (Partial Upfront)  $40 adelanto y 3$ mes | Total: $76
- m5.large = (No Upfront)       $0 adelanto y 7$ mes  | Total: $84

# Consideraciones:
- Amazon te cobra el servidor este o no esté prendido.
- Si no ha especificado ninguna zona de disponibilidad, el descuento se aplicará a una instancia en ejecución de cualquier tamaño (dentro de la misma familia) en la región. Por ejemplo:
    - Reservas m4.2xlarge Linux/UNIX (Total Upfront). Las instancias que aplican:
      2 instancias m4.xlarge o 4 instancias m4.large
   











