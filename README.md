# IoT-POWERLOGIC_PM5150
Obtener datos del Analizador de Red Schneider PowerLogic PM5110 con python y Node-RED mediante modbus TCP para integrar con un sistema IoT.

Publicar datos en MQTT y guardar datos en una BBDD usando python o Node-RED

Se usan tantos Monitores de energía Power Logic PM5150 como sean necesarios junto con una pasarela modbus TCP.

Analizador de Red Schneider PowerLogic PM5110:
- Producto https://www.se.com/ww/en/product-range/61281-powerlogic-pm5000-series/
- Manual usuario: http://pdfstream.manualsonline.com/a/a3ae7da6-b5c2-4d0d-9465-e7166dc7d750.pdf
- Lista de registros modbus: https://www.se.com/ww/en/faqs/FA234017/

Dado que estos equipos son Modbus RTU, para obtener los datos mediante Modbus TCP usamos una pasarela EGX150 de Schneider, Link 150.
- Modelo: https://www.se.com/es/es/product/EGX150/link-150---ethernet-gateway---2-ethernetport---24-v-dc-and-poe/
- User Guide: https://download.schneider-electric.com/files?p_enDocType=User+guide&p_File_Name=DOCA0110EN-04.pdf&p_Doc_Ref=DOCA0110EN

**Script python**: Recoge los datos y los guarda en una BBDD

**Node-RED**: recoge los datos y los publica en MQTT y los muestra en dashboard
- Repositorio Node-RED: https://github.com/aprendiendonodered/POWERLOGIC_PM5150

**Subflow Node-Red**: subflow reutilizable publicado en
- https://flows.nodered.org/flow/7c058a46b095af5b8bd469c7c5328454 
- https://gist.github.com/jecrespo/7c058a46b095af5b8bd469c7c5328454 

##Datos recogidos:

|Description|Register|Units|Size|Data Type|
|---|---|---|---|---|
|Current A | 3000 | A | 2 | FLOAT32 |
|Current B|3002|A|2|FLOAT32|
|Current C|3004|A|2|FLOAT32|
|Current N|3006|A|2|FLOAT32|
|Voltage A-N|3028|V|2|FLOAT32|
|Voltage B-N|3030|V|2|FLOAT32|
|Voltage C-N|3032|V|2|FLOAT32|
|Voltage N-G |3034|V|2|FLOAT32|
|Active Power A|3054|kW|2|FLOAT32|
|Active Power B|3056|kW|2|FLOAT32|
|Active Power C|3058|kW|2|FLOAT32|
|Active Power Total|3060|kW|2|FLOAT32|
|Reactive Power A|3062|kVAR|2|FLOAT32|
|Reactive Power B|3064|kVAR|2|FLOAT32|
|Reactive Power C|3066|kVAR|2|FLOAT32|
|Reactive Power Total|3068|kVAR|2|FLOAT32|
|Power Factor A|3078|—|2|4Q_FP_PF|
|Power Factor B|3080|—|2|4Q_FP_PF|
|Power Factor C|3082|—|2|4Q_FP_PF|
|Power Factor Total|3084|—|2|4Q_FP_PF|
|Frequency|3110|Hz|2|FLOAT32|
|THD Current A|21300|%|2|FLOAT32|
|THD Current B|21302|%|2|FLOAT32|
|THD Current C|21304|%|2|FLOAT32|
|THD Current N|21306|%|2|FLOAT32|
|THD Voltage A-N|21330|%|2|FLOAT32|
|THD Voltage B-N|21332|%|2|FLOAT32|
|THD Voltage C-N|21334|%|2|FLOAT32|
|THD Voltage N-G|21336|%|2|FLOAT32|
