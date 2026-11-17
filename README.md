# Análisis estadístico y correlacional de datos médicos en pacientes con VIH  
El proyecto se enfoca en el análisis exploratorio de los datos pertenecientes al dataset QualityOfCare, integrado por datos medicos de pacientes con Virus de Inmuno Deficiencia (VIH).
El dataset fue recupera de https://www.kaggle.com/datasets/iogbonna/quality-of-care-dataset-for-hiv-clients.
## Integrantes:
Juan Pablo Matiz Fresneda
Matías Núñez Piragauta

## Estuctura de los datos:
Las variables se pueden agrupar de la siguiente manera:

- **Datos demográficos y sociales:** edad, sexo, estado civil, nivel educativo y ocupación.
- **Datos del centro de atención:** nivel y tipo de institución, fuente de financiamiento y punto de entrada a la atención.
- **Fechas y tratamiento:** confirmación del VIH, ingreso al programa, inicio del tratamiento antirretroviral y régimen inicial.
- **Estado clínico e inmunológico:** estado funcional, estadio clínico, conteo de CD4 inicial y conteo de CD4 más reciente.
- **Seguimiento y resultados:** carga viral, adherencia al tratamiento, interrupciones o cambios del tratamiento y estado de tuberculosis.
- **Calidad de los datos:** algunas variables contienen valores faltantes; durante el análisis se revisaron y trataron esos valores, además de verificar registros duplicados e inconsistencias.

Las columnas combinan distintos tipos de datos: variables numéricas —como edad, peso, carga viral y conteos de CD4—, categóricas —como sexo, estado funcional y nivel de adherencia— y fechas relacionadas con el diagnóstico y la atención.
## Diccionario:
- **Health facility level**: Nivel de la institución de salud donde se registró el paciente.
- **FacilityType**: Tipo de centro de atención (hospital, clínica u otra estructura sanitaria).
- **FundingSources**: Fuente de financiamiento del servicio o programa de atención.
- **Age**: Edad del paciente en años al inicio del tratamiento.
- **Sex**: Sexo del paciente registrado en la base de datos.
- **MaritalStatus**: Estado civil del paciente.
- **EducationLevel**: Nivel educativo alcanzado por el paciente.
- **Occupation**: Ocupación del paciente.
- **DateOfConfirmedHIV**: Fecha en que se confirmó la infección por VIH.
- **DateOfEnrollment**: Fecha de inscripción o ingreso al programa.
- **CareEntryPoint**: Punto de entrada del paciente al sistema de atención.
- **DateArtStarted**: Fecha en que inició el tratamiento antirretroviral.
- **RegimenAtStart**: Regimen terapéutico inicial.
- **WeightAtStart**: Peso del paciente al inicio del tratamiento.
- **HeightAtStart**: Altura del paciente al inicio del tratamiento.
- **FunctionalStatusAtStart**: Estado funcional al inicio del tratamiento; indica si el paciente estaba activo o postrado.
- **ClinicalStageAtStart**: Estadio clínico del VIH al inicio de la atención.
- **Cd4Unit**: Unidad de medida del conteo de CD4.
- **Cd4AtStart**: Conteo inicial de linfocitos CD4, indicador del estado inmunológico base.
- **AdherenceCouncelingCompleted**: Confirmación de si se completó la consejería de adherencia.
- **InitialTbScreeningDone**: Indicador de si se realizó la evaluación inicial de tuberculosis.
- **ArtSubstitution**: Cambio de tratamiento por sustitución.
- **ArtSwitch**: Cambio de régimen terapéutico.
- **ArtInterruption**: Indicador de interrupción del tratamiento antirretroviral.
- **PatientDead**: Estado vital del paciente.
- **ViralLoad**: Carga viral del paciente; refleja el nivel de replicación del virus.
- **ViralLoad_missing**: Variable creada para indicar si la carga viral está ausente.
- **ArvAdherenceLatestLevel**: Nivel de adherencia al tratamiento antirretroviral más reciente.
- **MostRecentCd4Count**: Conteo más reciente de CD4 durante el seguimiento clínico.
- **TbStatusAtLAstVisit**: Estado de tuberculosis reportado en la última visita.
## Conclusiones:
#1. **Ingreso tardio al tratamiento y deterioro inmunologico:** los bajos niveles de CD4 inicial indican que una parte importante de los pacientes comienza la atencion con un estado inmunologico avanzado. Esta conclusion se basa en la distribucion y la mediana de `Cd4AtStart`, despues de tratar los valores faltantes.

#2. **Control virológico en los pacientes con mediciones disponibles:**
La distribución de la carga viral sugiere que la mayoría de los pacientes con registro disponible presenta control virológico, aunque esta conclusión debe interpretarse con precaución porque aún existe una proporción relevante de datos faltantes. En otras palabras, la evidencia disponible apunta a un buen desempeño terapéutico en parte de la cohorte, pero no se puede generalizar a todos los pacientes sin considerar los registros incompletos

#3. **Brecha de seguimiento clinico:** la ausencia de pruebas recientes de carga viral representa un problema relevante de calidad y continuidad del seguimiento. Este hallazgo se identifica mediante el indicador de datos faltantes `ViralLoad_missing` y su proporcion dentro del total de pacientes.

#4. **Adherencia y respuesta inmunológica:**
Los pacientes con adherencia "Good" muestran, en general, niveles de CD4 reciente más altos que quienes presentan adherencia "Poor". Esto indica una asociación positiva entre una buena adherencia y una mejor recuperación inmunológica, aunque el análisis descriptivo no demuestra causalidad directa. La adherencia parece ser un factor clave para sostener la respuesta inmune y el control clínico del paciente.

#5. **El estado funcional inicial constituye una barrera para la adherencia:** los pacientes que ingresaron postrados o con mayor dependencia fisica muestran una mayor proporcion de adherencia deficiente que los pacientes activos. Esta conclusion se obtiene de la tabla cruzada normalizada entre `FunctionalStatusAtStart` y `ArvAdherenceLatestLevel`.

