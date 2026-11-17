# Análisis estadístico y correlacional de datos médicos en pacientes con VIH  
El proyecto se enfoca en el análisis exploratorio de los datos pertenecientes al dataset QualityOfCare, integrado por datos medicos de pacientes con Virus de Inmuno Deficiencia (VIH).
El dataset fue recupera de https://www.kaggle.com/datasets/iogbonna/quality-of-care-dataset-for-hiv-clients.
## Integrantes:
Juan Pablo Matiz Fresneda

## Estuctura de los datos:
## Diccionario:
## Conclusiones:

#1. **Ingreso tardio al tratamiento y deterioro inmunologico:** los bajos niveles de CD4 inicial indican que una parte importante de los pacientes comienza la atencion con un estado inmunologico avanzado. Esta conclusion se basa en la distribucion y la mediana de `Cd4AtStart`, despues de tratar los valores faltantes.

#3. **Brecha de seguimiento clinico:** la ausencia de pruebas recientes de carga viral representa un problema relevante de calidad y continuidad del seguimiento. Este hallazgo se identifica mediante el indicador de datos faltantes `ViralLoad_missing` y su proporcion dentro del total de pacientes.

#5. **El estado funcional inicial constituye una barrera para la adherencia:** los pacientes que ingresaron postrados o con mayor dependencia fisica muestran una mayor proporcion de adherencia deficiente que los pacientes activos. Esta conclusion se obtiene de la tabla cruzada normalizada entre `FunctionalStatusAtStart` y `ArvAdherenceLatestLevel`.

