# %% [markdown]
# # Analisis estadístico y correlacional de datos médicos en pacientes con VIH
# Integrantes: Juan Pablo Matiz, Matias Nuñez Piragauta

# %%
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



df.drop(columns=cols_drop_high_nulls, inplace=True)

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

print(f'Variables eliminadas: {len(cols_drop_high_nulls + cols_drop_redundant + cols_drop_complex)}')

print(f'Variables restantes: {df.shape[1]}')


# Age — reemplazamos valores fuera de rango plausible con NaN

df['Age'] = df['Age'].where(

    (df['Age'] >= 1) & (df['Age'] <= 100),

    other=np.nan

)



# ViralLoad — convertimos a numérico primero, luego tratamos

df['ViralLoad'] = pd.to_numeric(df['ViralLoad'], errors='coerce')



print('Outliers tratados en Age y ViralLoad')

print(f'Nulos en Age tras tratamiento: {df["Age"].isnull().sum()}')

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


# Tratamiento  ViralLoad

# Objetivo: convertir a variable numérica

# Problema: contiene valores no numéricos (object)



df['ViralLoad'] = pd.to_numeric(df['ViralLoad'], errors='coerce')


# Verificamos valores negativos en ViralLoad

print(f'Registros con ViralLoad negativo: {(df["ViralLoad"] < 0).sum()}')

print(df[df['ViralLoad'] < 0]['ViralLoad'].describe())


df['ViralLoad_missing'] = df['ViralLoad'].isnull().astype(int)

print(f'Registros originalmente nulos en ViralLoad: {df["ViralLoad_missing"].sum()}')


# Corrección de valores negativos en ViralLoad

# Clínicamente imposibles — se reemplazan con NaN y se reimputa con mediana

# Afecta únicamente 3 registros (0.01% del dataset)



df['ViralLoad'] = df['ViralLoad'].where(df['ViralLoad'] >= 0, other=np.nan)

df['ViralLoad'] = df['ViralLoad'].fillna(df['ViralLoad'].median())



print(f'Valores negativos restantes: {(df["ViralLoad"] < 0).sum()}')


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

# %% [markdown]
# ## 5. Creación de variables  (Integrante A)

# %% [markdown]
# ## 6. Filtrado y condiciones en pandas  (Integrante B)

# %% [markdown]
# ## 7. Agrupación con groupby  (Integrante A)

# %% [markdown]
# ## 8. Visualizaciones  (Integrante B)

# %% [markdown]
# ## 9. Conclusiones finales  (Integrante A)
