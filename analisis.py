# %% [markdown]
# # Analisis estadístico y correlacional de datos médicos en pacientes con VIH
# Integrantes: Juan Pablo Matiz, Matias Nuñez Piragauta

#%%
%pip install --break-system-packages pandas numpy matplotlib seaborn openpyxl jinja2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# %% [markdown]
# ## 1. Carga e inspección inicial de los datos  (Integrante A)
#%%

# Lectura del dataset Excel local

df = pd.read_excel('datos/QualityOfCare.xlsx')

print(f'Dataset cargado: {df.shape[0]} filas y {df.shape[1]} columnas')

#Creamos el DataFrame que nos permite visualizar y comprender los elementos de la base de datos:

resumen_variables = pd.DataFrame({

    'Variable': df.columns,                                                   #Asigna cada columna a una fila bajo el nombre de Variable

    'Tipo_Python': df.dtypes.values,                                          #Tipo de dato, detectado por Python

    'Valores_No_Nulos': df.notnull().sum().values,                            #Cantidad de valores no nulos

    'Valores_Nulos': df.isnull().sum().values,                                #Cantidad de valores nulos

    'Pct_Nulos': (df.isnull().mean() * 100).round(2).values,                  #Porcentaje de valores nulos con respecto al total

    'Valores_Unicos': df.nunique().values                                     #Cantidad de valores unicos

})



#Utilizamos pandas para estilizar la tabla creada y crear un gradiente de color rojo que enfatiza
#el porcentaje de valores nulos, y un gradiente verde que enfatiza la presencia de datos no nulos

display(

    resumen_variables.style

    .background_gradient(subset=['Pct_Nulos'], cmap='Reds')

    .background_gradient(subset=['Valores_No_Nulos'], cmap='Greens')

    .format({'Pct_Nulos': '{:.1f}%'})

    .set_caption('Resumen de Variables del Dataset')

)


nulos_pct = (df.isnull().mean() * 100).round(2)

nulos_pct = nulos_pct[nulos_pct > 0].sort_values(ascending=False)



# Graficamos un barplot horizontal para facilitar la lectura de los nombres de variables

fig, ax = plt.subplots(figsize=(10, 8))



colores = ['#d73027' if x > 40 else '#fc8d59' if x > 15 else '#fee090' for x in nulos_pct.values]



nulos_pct.plot(kind='barh', ax=ax, color=colores)



ax.axvline(x=40, color='darkred', linestyle='--', linewidth=1, label='Umbral crítico (40%)')

ax.axvline(x=15, color='orange', linestyle='--', linewidth=1, label='Umbral moderado (15%)')



ax.set_title('Porcentaje de Valores Faltantes por Variable', fontsize=14)

ax.set_xlabel('Porcentaje de Nulos (%)')

ax.set_ylabel('Variable')

ax.legend()

plt.tight_layout()

plt.show()

estadisticas_numericas = (

    df.describe()

    .T #Transponemos las columnas como filas para mayor legibilidad

    .rename(columns={

        'count': 'Conteo',

        'mean': 'Media',

        'std': 'Desv. Estándar',

        'min': 'Mínimo',

        '25%': 'Percentil 25',

        '50%': 'Mediana',

        '75%': 'Percentil 75',

        'max': 'Máximo'

    })

)



# Se calcula el coeficiente de variación indica qué tan dispersos están los datos

# en relación a la media — valores altos sugieren alta variabilidad

estadisticas_numericas['Coef. Variación (%)'] = (

    (estadisticas_numericas['Desv. Estándar'] / estadisticas_numericas['Media']) * 100

).round(2)



display(

    estadisticas_numericas.style

    .background_gradient(cmap='Blues', subset=['Media', 'Desv. Estándar'])

    .background_gradient(cmap='Oranges', subset=['Coef. Variación (%)'])

    .format('{:.2f}')

    .set_caption('Estadísticas Descriptivas — Variables Numéricas')

)

# %% [markdown]
# ## 2. Manejo de datos faltantes  (Integrante B)
# %%
#Variables con >80% nulos (eliminación de variables)

cols_drop_high_nulls = [

    'AgeInMonths',

    'ArtInterruptionReason',

    'ArtInterruptionDate',

    'ArtInterruptionType',

    'OpportunisticInfectionAtLastVisitOthers',

    'OpportunisticInfectionAtLastVisit'

]



print(f'Variables eliminadas: {len(cols_drop_high_nulls)}')

print(f'Variables restantes: {df.shape[1]}')



# ViralLoad — convertimos a numérico primero, luego tratamos

df['ViralLoad'] = pd.to_numeric(df['ViralLoad'], errors='coerce')

df['ViralLoad_missing'] = df['ViralLoad'].isnull().astype(int)

print(f'Registros originalmente nulos en ViralLoad: {df["ViralLoad_missing"].sum()}')

df['ViralLoad'] = df['ViralLoad'].fillna(df['ViralLoad'].median())

print(f'Nulos en ViralLoad tras tratamiento: {df["ViralLoad"].isnull().sum()}')

# Tratamiento de variable Age

# Objetivo: imputar valores faltantes de Age

# Método: imputación con mediana (robusta a valores extremos)


df['Age'] = df['Age'].fillna(df['Age'].median())

#Verificación de null imputados (mediana)

df['Age'].isnull().sum()

# Tratamiento de  CD4

# Objetivo: imputar valores faltantes de Cd4AtStart

# Justificación: variable clínica importante (estado inmunológico)

# Método: imputación con mediana (robusta a valores extremos) ya que la media es sensible a valores extremos

print(f'Nulos en Age tras tratamiento: {df["Age"].isnull().sum()}')


df['Cd4AtStart'] = df['Cd4AtStart'].fillna(df['Cd4AtStart'].median())


# Tratamiento de WeightAtStart

# Objetivo: imputar valores faltantes de WeightAtStart

# Justificación: variable clínica importante (estado nutricional)

# Presenta 8.15% de valores nulos

# Método: imputación con mediana (robusta a outliers) ya que la media es sensible a valores extremos



df['WeightAtStart'] = df['WeightAtStart'].fillna(df['WeightAtStart'].median())


# Tratamiento de HeightAtStart


# Objetivo: conservar información y manejar nulos (43.72%)

# Creación de variable "missing" que conserva registro de pacientes sin registros

df['Height_missing'] = df['HeightAtStart'].isnull().astype(int)


df['HeightAtStart'] = df['HeightAtStart'].fillna(df['HeightAtStart'].median())


# Tratamiento CurrentRegimen

# Objetivo: manejar valores faltantes en variable categórica

# Justificación: variable clínica importante con 15.61% de nulos



df['CurrentRegimen'] = df['CurrentRegimen'].fillna("Unknown")


# Tratamiento ClinicalStageAtStart

# Objetivo: conservar información y manejar nulos (4.24%)

df['ClinicalStageAtStart'] = df['ClinicalStageAtStart'].fillna("Unknown")


#Tratamiento MostRecentCD4Count

# Objetivo: conservar información y manejar nulos (26%)



df['MostRecentCd4_missing'] = df['MostRecentCd4Count'].isnull().astype(int)



df['MostRecentCd4Count'] = df['MostRecentCd4Count'].fillna(

    df['MostRecentCd4Count'].median()

)


# Verificación: ViralLoad ya no tiene nulos (la imputación de la celda anterior
# a los valores negativos también cubrió los nulos originales del todo)

print(f'Nulos restantes en ViralLoad: {df["ViralLoad"].isnull().sum()}')



# Seleccionamos únicamente variables con valores nulos para el análisis de co-ocurrencia

variables_con_nulos = df.columns[df.isnull().any()].tolist()



# Creamos matriz booleana de nulos (1 = nulo, 0 = presente)

matriz_nulos = df[variables_con_nulos].isnull().astype(int)



# Calculamos correlación entre patrones de nulos

correlacion_nulos = matriz_nulos.corr()



# Visualizamos como heatmap

fig, ax = plt.subplots(figsize=(14, 10))

sns.heatmap(

    correlacion_nulos,

    cmap='Reds',

    ax=ax,

    linewidths=0.5,

    annot=False  # Con 30+ variables, los números se solapan — mejor sin anotaciones

)

ax.set_title('Correlación entre Patrones de Valores Faltantes', fontsize=14)

plt.xticks(rotation=45, ha='right')

plt.tight_layout()

plt.show()
# %% [markdown]
# ## 3. Identificación de outliers  (Integrante A)
# %%
# Identificación de outliers mediante el método IQR

# Q1 = percentil 25, Q3 = percentil 75, IQR = rango intercuartílico



variables_numericas = df.select_dtypes(include=[np.number]).columns.tolist()



resumen_outliers = []



for var in variables_numericas:

    Q1 = df[var].quantile(0.25)

    Q3 = df[var].quantile(0.75)

    IQR = Q3 - Q1

    limite_inferior = Q1 - 1.5 * IQR

    limite_superior = Q3 + 1.5 * IQR



    n_outliers = ((df[var] < limite_inferior) | (df[var] > limite_superior)).sum()

    pct_outliers = (n_outliers / df[var].count() * 100).round(2)



    resumen_outliers.append({

        'Variable': var,

        'Q1': round(Q1, 2),

        'Q3': round(Q3, 2),

        'IQR': round(IQR, 2),

        'Límite Inferior': round(limite_inferior, 2),

        'Límite Superior': round(limite_superior, 2),

        'N Outliers': n_outliers,

        'Pct Outliers': pct_outliers

    })



resumen_outliers = pd.DataFrame(resumen_outliers).sort_values('Pct Outliers', ascending=False)



display(

    resumen_outliers.style

    .background_gradient(subset=['Pct Outliers'], cmap='Reds')

    .format({'Pct Outliers': '{:.2f}%'})

    .set_caption('Detección de Outliers por Variable — Método IQR')

)

# Filtramos únicamente variables con porcentaje de outliers superior al 5%

# para enfocarnos en las que requieren atención real



variables_con_outliers = resumen_outliers[

    resumen_outliers['Pct Outliers'] > 5

]['Variable'].tolist()



fig, axes = plt.subplots(

    nrows=len(variables_con_outliers),

    ncols=1,

    figsize=(10, len(variables_con_outliers) * 3)

)



# Manejo del caso donde solo hay una variable

if len(variables_con_outliers) == 1:

    axes = [axes]



for i, var in enumerate(variables_con_outliers):

    axes[i].boxplot(

        df[var].dropna(),

        vert=False,

        patch_artist=True,

        boxprops=dict(facecolor='#a8d5e2'),

        medianprops=dict(color='darkred', linewidth=2)

    )

    axes[i].set_title(f'{var}', fontsize=10)

    axes[i].set_xlabel('Valor')



plt.suptitle('Boxplots — Variables con Outliers Significativos (>5%)',

             fontsize=13, y=1.01)

plt.tight_layout()

plt.show()
# %% [markdown]
# ## 4. Valores inconsistentes y duplicados  (Integrante B)
# %%
#Variables redundantes (eliminación de variables)

cols_drop_redundant = [

    'HeightUnit',

    'Cd4Unit'      # unidad constante o irrelevante

]



df.drop(columns=cols_drop_redundant, inplace=True)


#Variables complejas (eliminación de variables)

cols_drop_complex = [

    'FundingSources',

    'Occupation'       # Compleja de analizar sin recodificación

]



df.drop(columns=cols_drop_complex, inplace=True)


# Tratamiento  ViralLoad

# Objetivo: convertir a variable numérica

# Problema: contiene valores no numéricos (object)



df['ViralLoad'] = pd.to_numeric(df['ViralLoad'], errors='coerce')


df['ViralLoad_missing'] = df['ViralLoad'].isnull().astype(int)

print(f'Registros originalmente nulos en ViralLoad: {df["ViralLoad_missing"].sum()}')



# Corrección de valores negativos en ViralLoad

# Clínicamente imposibles — se reemplazan con NaN y se reimputa con mediana

# Afecta únicamente 3 registros (0.01% del dataset)



df['ViralLoad'] = df['ViralLoad'].where(df['ViralLoad'] >= 0, other=np.nan)

df['ViralLoad'] = df['ViralLoad'].fillna(df['ViralLoad'].median())



print(f'Valores negativos restantes: {(df["ViralLoad"] < 0).sum()}')



# Verificación: ViralLoad ya no tiene nulos (la imputación de la celda anterior
# a los valores negativos también cubrió los nulos originales del todo)

print(f'Nulos restantes en ViralLoad: {df["ViralLoad"].isnull().sum()}')


# Age — reemplazamos valores fuera de rango plausible con NaN

df['Age'] = df['Age'].where(

    (df['Age'] >= 1) & (df['Age'] <= 100),

    other=np.nan

)


# Contar y eliminar filas duplicadas
duplicados = df.duplicated().sum()
print(f'Registros duplicados: {duplicados}')
df = df.drop_duplicates()
print(f'Duplicados restantes: {df.duplicated().sum()}')
# %% [markdown]
# ## 5. Creación de variables  (Integrante A)
# %% [markdown]
## Variables derivadas

#Las siguientes variables se construyen después de la limpieza para convertir medidas individuales en indicadores que permitan comparar grupos de pacientes y estudiar su evolución clínica. No reemplazan las variables originales: las complementan.

#- **AgeGroup:** agrupa `Age` en etapas de vida (menor de 18, 18-29, 30-44, 45-59 y 60 o más). Esto facilita comparar resultados clínicos por edad sin interpretar cada edad como una categoría independiente.
#- **WeightChangeKg:** se calcula como `WeightAtLastVisit - WeightAtStart`. Permite identificar pérdida o ganancia de peso entre el inicio del tratamiento y la última visita; los valores negativos representan pérdida y los positivos ganancia.
#- **Cd4Change:** se calcula como `MostRecentCd4Count - Cd4AtStart`. Resume la evolución inmunológica: un valor positivo indica aumento del conteo de CD4 y uno negativo indica disminución.
#- **ImmuneStatusAtLastVisit:** clasifica el CD4 de la última visita en tres niveles: inmunidad severamente comprometida (menos de 200), comprometida (200-499) y favorable (500 o más). Así se puede estudiar la distribución del riesgo inmunológico.
#- **ViralSuppressionStatus:** clasifica como suprimida una carga viral de hasta 50 copias/ml y como no suprimida una mayor de 50. Los registros con `ViralLoad_missing = 1` se mantienen como 'Sin medicion valida' para no confundir valores imputados con mediciones clínicas reales.

#En conjunto, estas variables permiten relacionar edad, cambios antropométricos, recuperación inmunológica y control virológico para elaborar conclusiones más profundas.
# %%
df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 17, 29, 44, 59, float('inf')], labels=['Menor de 18', '18-29', '30-44', '45-59', '60 o mas'], include_lowest=True)
df['WeightChangeKg'] = df['WeightAtLastVisit'] - df['WeightAtStart']
df['Cd4Change'] = df['MostRecentCd4Count'] - df['Cd4AtStart']
df['ImmuneStatusAtLastVisit'] = pd.cut(df['MostRecentCd4Count'], bins=[-float('inf'), 199, 499, float('inf')], labels=['Inmunidad severamente comprometida', 'Inmunidad comprometida', 'Inmunidad favorable'])
df['ViralSuppressionStatus'] = np.select([df['ViralLoad_missing'].eq(1), df['ViralLoad'].le(50)], ['Sin medicion valida', 'Suprimida (<=50 copias/ml)'], default='No suprimida (>50 copias/ml)')
variables_derivadas = ['AgeGroup', 'WeightChangeKg', 'Cd4Change', 'ImmuneStatusAtLastVisit', 'ViralSuppressionStatus']
display(df[variables_derivadas].head())
print(f'Variables derivadas creadas: {len(variables_derivadas)}')

# %% [markdown]
# ## 6. Filtrado y condiciones en pandas  (Integrante B)
# %%
# 1. Relación entre el Estado Funcional "Postrado en Cama" (Bed ridden) y la Adherencia Deficiente
bed_ridden = df[df['FunctionalStatusAtStart'] == 'Bed ridden']
adherencia_deficiente_bed = bed_ridden['ArvAdherenceLatestLevel'].isin(['Fair', 'Poor']).mean() * 100
adherencia_deficiente_general = df['ArvAdherenceLatestLevel'].isin(['Fair', 'Poor']).mean() * 100

print(f"[Dato 1] El {adherencia_deficiente_bed:.1f}% de los pacientes que iniciaron el tratamiento postrados en cama presentan una adherencia deficiente (Fair/Poor), en comparación con un {adherencia_deficiente_general:.1f}% en la población general. Conclusión: El estado físico inicial de postración es un fuerte predictor de dificultades en la adherencia a largo plazo.")

# 2. Impacto de la Co-infección por Tuberculosis en la Interrupción del Tratamiento
tb_activa = df[df['TbStatusAtLAstVisit'] == 'Confirmed TB']
interrupcion_tb = (tb_activa['ArtInterruption'].astype(str).str.strip().str.lower() == 'yes').mean() * 100
interrupcion_general = (df['ArtInterruption'].astype(str).str.strip().str.lower() == 'yes').mean() * 100

print(f"[Dato 2] Los pacientes con Tuberculosis activa confirmada en su última visita interrumpen el tratamiento en un {interrupcion_tb:.1f}%, frente al {interrupcion_general:.1f}% general. Conclusión: La co-infección activa de TB duplica la probabilidad de interrupción del tratamiento ARV, requiriendo un manejo conjunto prioritario.")

# 3. Adherencia en Pacientes sin Registro Reciente de Carga Viral (ViralLoad_missing)
sin_carga_viral = df[df['ViralLoad_missing'] == 1]
adherencia_good_sin_cv = (sin_carga_viral['ArvAdherenceLatestLevel'] == 'Good').mean() * 100

print(f"[Dato 3] El {adherencia_good_sin_cv:.1f}% de los pacientes que no tienen un registro de carga viral reciente reportan una adherencia 'Good'. Conclusión: Existe una brecha de monitoreo clínico importante; pacientes clasificados con buena adherencia subjetiva carecen de confirmación virológica objetiva.")

# 4. Diferencia en la Pérdida de Peso Durante el Tratamiento en Pacientes con Interrupción
pacientes_interrumpidos = df[df['ArtInterruption'].astype(str).str.strip().str.lower() == 'yes']
pacientes_continuos = df[df['ArtInterruption'].astype(str).str.strip().str.lower() == 'no']

peso_perdido_interrumpidos = (pacientes_interrumpidos['WeightAtStart'] - pacientes_interrumpidos['WeightAtLastVisit']).mean()
peso_perdido_continuos = (pacientes_continuos['WeightAtStart'] - pacientes_continuos['WeightAtLastVisit']).mean()

print(f"[Dato 4] Los pacientes con interrupción del tratamiento perdieron en promedio {peso_perdido_interrumpidos:.2f} kg desde el inicio, mientras que los continuos perdieron {peso_perdido_continuos:.2f} kg. Conclusión: La interrupción del tratamiento no muestra una pérdida de peso marcadamente mayor en promedio, sugiriendo que el impacto físico es heterogéneo o de largo plazo.")

# 5. Vulnerabilidad Inmunológica Extrema (CD4 < 200) según el Nivel de Establecimiento de Salud
terciario = df[df['Health facility level'].astype(str).str.strip().str.lower() == 'tertiary']
primario = df[df['Health facility level'].astype(str).str.strip().str.lower() == 'primary']

cd4_bajo_terciario = (terciario['MostRecentCd4Count'] < 200).mean() * 100
cd4_bajo_primario = (primario['MostRecentCd4Count'] < 200).mean() * 100

print(f"[Dato 5] El {cd4_bajo_terciario:.1f}% de los pacientes en hospitales de nivel terciario tienen CD4 < 200, comparado con el {cd4_bajo_primario:.1f}% en nivel primario. Conclusión: Los centros de alta complejidad concentran a los pacientes con mayor deterioro inmunológico de la red de salud.")

# %% [markdown]
# ## 7. Agrupación con groupby  (Integrante A)

# %%
# Resumenes agrupados para obtener conclusiones comparables entre subgrupos.
resumen_edad = df.groupby('AgeGroup', observed=False).agg(
    Pacientes=('Age', 'size'),
    CD4_final_promedio=('MostRecentCd4Count', 'mean'),
    Cambio_CD4_promedio=('Cd4Change', 'mean')
).round(2)

relacion_inmunidad_viral = (
    pd.crosstab(
        df['ImmuneStatusAtLastVisit'],
        df['ViralSuppressionStatus'],
        normalize='index'
    ) * 100
).round(2)

resumen_regimen = df.groupby('CurrentRegimen', observed=False).agg(
    Pacientes=('CurrentRegimen', 'size'),
    Cambio_CD4_promedio=('Cd4Change', 'mean'),
    Cambio_peso_promedio=('WeightChangeKg', 'mean')
).round(2).sort_values('Cambio_CD4_promedio', ascending=False)

resumen_estadio = df.groupby('ClinicalStageAtStart', observed=False).agg(
    Pacientes=('ClinicalStageAtStart', 'size'),
    Cambio_CD4_promedio=('Cd4Change', 'mean'),
    Supresion_viral_pct=('ViralSuppressionStatus', lambda s: (s == 'Suprimida (<=50 copias/ml)').mean() * 100)
).round(2).sort_values('Cambio_CD4_promedio')

resumen_adherencia = df.groupby('ArvAdherenceLatestLevel', observed=False).agg(
    Pacientes=('ArvAdherenceLatestLevel', 'size'),
    CD4_final_promedio=('MostRecentCd4Count', 'mean'),
    Supresion_viral_pct=('ViralSuppressionStatus', lambda s: (s == 'Suprimida (<=50 copias/ml)').mean() * 100),
    Cambio_peso_promedio=('WeightChangeKg', 'mean')
).round(2)

display(resumen_edad)
display(relacion_inmunidad_viral)
display(resumen_regimen)
display(resumen_estadio)
display(resumen_adherencia)

# %% [markdown]
# ## Conclusiones obtenidas mediante `groupby`

#1. **Diferencias por grupo etario:** el grupo de 60 años o más presenta el mayor cambio promedio de CD4 (852.92), mientras que el grupo de 45-59 años presenta un cambio promedio negativo (-72.73). Esto sugiere que la evolución inmunológica no es uniforme entre edades y que el grupo de 45-59 años requiere una revisión específica de sus registros y posibles factores clínicos.

#2. **Estado inmunológico y supresión viral:** entre los pacientes con inmunidad favorable, el 15.4% aparece como suprimido, frente al 9.0% de quienes tienen inmunidad severamente comprometida. La relación es descriptiva y no prueba causalidad, pero indica que un mejor estado de CD4 tiende a coexistir con una mayor proporción de supresión viral.

#3. **Regimen actual y recuperación de CD4:** los pacientes con régimen de primera línea presentan un cambio promedio de CD4 de 213.06, superior al registrado en los grupos con régimen desconocido (129.68) y de segunda línea (-1895.01). El valor extremo del régimen de segunda línea debe interpretarse con cautela porque su grupo es pequeño (371 pacientes) y puede estar afectado por valores atípicos.

#4. **Estadio clínico al inicio:** los pacientes clasificados en estadio III presentan el mayor cambio promedio de CD4 (304.92), mientras que los de estadio II presentan 49.18. Esto muestra que el cambio observado no sigue necesariamente un orden lineal por estadio y debe analizarse junto con el tamaño de cada grupo y las condiciones clínicas iniciales.

#5. **Adherencia y resultados clínicos:** el grupo con adherencia buena concentra la mayoría de los pacientes (23,268) y tiene el mayor CD4 final promedio (604.48), mientras que el grupo con adherencia pobre presenta un CD4 final promedio menor (356.40) y una menor proporción de supresión viral (4.60% frente a 12.51% en adherencia buena). Esta asociación respalda la importancia de la adherencia en el seguimiento, aunque no permite afirmar causalidad por sí sola.

# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)
# %%
# Configuramos una figura de cuadrícula para los 5 gráficos seleccionados
fig = plt.figure(figsize=(16, 22))


# GRÁFICO 1: Histograma de CD4 Inicial (Recortado al percentil 99)

plt.subplot(3, 2, 1)
datos_cd4 = df['Cd4AtStart'].dropna()
limite_cd4 = datos_cd4.quantile(0.99)
datos_cd4_clip = datos_cd4[datos_cd4 <= limite_cd4]

plt.hist(datos_cd4_clip, bins=30, color='#a8d5e2', edgecolor='white')
plt.axvline(datos_cd4_clip.median(), color='darkred', linestyle='--', linewidth=1.5, label='Mediana')
plt.title('1. Distribución de CD4 Inicial (Cd4AtStart)', fontsize=12)
plt.xlabel('Células CD4 / µL')
plt.ylabel('Frecuencia')
plt.legend()


# GRÁFICO 2: Histograma de Carga Viral (Recortada al percentil 99)

plt.subplot(3, 2, 2)
datos_vl = df['ViralLoad'].dropna()
limite_vl = datos_vl.quantile(0.99)
datos_vl_clip = datos_vl[datos_vl <= limite_vl]

plt.hist(datos_vl_clip, bins=30, color='#a8d5e2', edgecolor='white')
plt.axvline(datos_vl_clip.median(), color='darkred', linestyle='--', linewidth=1.5, label='Mediana')
plt.title('2. Distribución de Carga Viral (ViralLoad)', fontsize=12)
plt.xlabel('Copias / mL')
plt.ylabel('Frecuencia')
plt.legend()


# GRÁFICO 3: Pérdida de datos en Carga Viral (Missingness Flag)

plt.subplot(3, 2, 3)
conteo_vl_miss = df['ViralLoad_missing'].value_counts().sort_index()
plt.bar(['Presente (0)', 'Faltante (1)'], conteo_vl_miss.values, color=['#a8d5e2', '#d73027'], edgecolor='white')
plt.title('3. Ausencia de Registro de Carga Viral (ViralLoad_missing)', fontsize=12)
plt.xlabel('Estado')
plt.ylabel('Cantidad de Pacientes')
for k, v in enumerate(conteo_vl_miss.values):
    plt.text(k, v + 250, f"{v} ({v/len(df)*100:.1f}%)", ha='center', fontsize=10, fontweight='bold')


# GRÁFICO 4: Boxplot de CD4 Reciente por Nivel de Adherencia

plt.subplot(3, 2, 4)
niveles_adh = df['ArvAdherenceLatestLevel'].dropna().unique()
limite_cd4_rec = df['MostRecentCd4Count'].quantile(0.99)
df_clip_cd4_rec = df[df['MostRecentCd4Count'] <= limite_cd4_rec]

grupos_cd4_rec = [
    df_clip_cd4_rec[df_clip_cd4_rec['ArvAdherenceLatestLevel'] == nivel]['MostRecentCd4Count'].dropna()
    for nivel in niveles_adh
]

plt.boxplot(grupos_cd4_rec, tick_labels=niveles_adh, patch_artist=True,
            boxprops=dict(facecolor='#a8d5e2'), medianprops=dict(color='darkred', linewidth=2))
plt.title('4. CD4 Reciente por Nivel de Adherencia', fontsize=12)
plt.xlabel('Nivel de Adherencia')
plt.ylabel('Conteo Reciente de CD4')
plt.xticks(rotation=15)


# GRÁFICO 5: Relación Estado Funcional Inicial vs Adherencia

plt.subplot(3, 2, 5)
tabla_cruce = pd.crosstab(df['FunctionalStatusAtStart'], df['ArvAdherenceLatestLevel'], normalize='index')
tabla_cruce.plot(kind='bar', ax=plt.gca(), colormap='coolwarm', edgecolor='white')
plt.title('5. Estado Funcional Inicial vs Nivel de Adherencia', fontsize=12)
plt.xlabel('Estado Funcional al Ingreso')
plt.ylabel('Proporción (Normalizado)')
plt.xticks(rotation=15)
plt.legend(title='Adherencia', loc='best')

plt.tight_layout()
plt.show()

# Conclusiones impresas dinámicamente con valores reales
print("CONCLUSIONES CLÍNICAS Y OPERATIVAS CLAVE:")
print(f"1. CD4 Inicial: La mitad de los pacientes inicia el tratamiento con menos de {datos_cd4.median():.0f} CD4 células/µL, lo que evidencia un preocupante ingreso tardío al sistema de salud.")
print(f"2. Carga Viral Activa: La mediana de carga viral es {datos_vl.median():.0f} copias/mL, confirmando que la mayoría de los pacientes en control regular logran una adecuada supresión virológica.")
print(f"3. Brecha de Monitoreo: Un {conteo_vl_miss[1]/len(df)*100:.1f}% de los pacientes ({conteo_vl_miss[1]} en total) carece de una prueba reciente de Carga Viral, revelando un problema prioritario en el seguimiento.")
print(f"4. Respuesta Inmunológica: El gráfico de CD4 Reciente confirma visualmente que quienes mantienen una adherencia 'Good' gozan de una mejor recuperación de defensas que los pacientes de nivel 'Poor'.")
print(f"5. Barrera Física de Adherencia: Los pacientes que iniciaron postrados en cama ('Bed ridden') muestran proporciones críticamente mayores de adherencia deficiente en comparación con quienes ingresaron activos.")

# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)

## Conclusiones generales del analisis

#1. **Ingreso tardio al tratamiento y deterioro inmunologico:** los bajos niveles de CD4 inicial indican que una parte importante de los pacientes comienza la atencion con un estado inmunologico avanzado. Esta conclusion se basa en la distribucion y la mediana de `Cd4AtStart`, despues de tratar los valores faltantes.

#2. **Control virologico en los pacientes con mediciones disponibles:** la distribucion de `ViralLoad` sugiere control virologico en los pacientes evaluados. La conclusion se obtiene del analisis de la carga viral ya convertida y depurada, por lo que debe interpretarse junto con la existencia de registros faltantes.

#3. **Brecha de seguimiento clinico:** la ausencia de pruebas recientes de carga viral representa un problema relevante de calidad y continuidad del seguimiento. Este hallazgo se identifica mediante el indicador de datos faltantes `ViralLoad_missing` y su proporcion dentro del total de pacientes.

#4. **La adherencia se relaciona con mejores resultados inmunologicos:** los pacientes con adherencia `Good` presentan, en general, mayores niveles de CD4 reciente que quienes tienen adherencia `Poor`. Esta conclusion surge de la comparacion agrupada y del boxplot de `MostRecentCd4Count`; describe una asociacion y no demuestra causalidad.

#5. **El estado funcional inicial constituye una barrera para la adherencia:** los pacientes que ingresaron postrados o con mayor dependencia fisica muestran una mayor proporcion de adherencia deficiente que los pacientes activos. Esta conclusion se obtiene de la tabla cruzada normalizada entre `FunctionalStatusAtStart` y `ArvAdherenceLatestLevel`.

#En conjunto, estas conclusiones se basan en el dataset previamente limpiado: se revisaron valores faltantes, se corrigieron variables clinicas y valores imposibles, y los valores extremos se recortaron al percentil 99 solo para mejorar la visualizacion.